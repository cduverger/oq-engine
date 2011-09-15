# -*- coding: utf-8 -*-

# Copyright (c) 2010-2011, GEM Foundation.
#
# OpenQuake is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with OpenQuake.  If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.


"""
Set up some system-wide loggers
TODO(jmc): init_logs should take filename, or sysout
TODO(jmc): support debug level per logger.

"""
import logging
import sys
import socket

import kombu
import kombu.entity
import kombu.messaging

from openquake import flags
from openquake.utils import config
from openquake.signalling import AMQPMessageConsumer


FLAGS = flags.FLAGS

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

# This parameter sets where bin/openquake and the likes will send their
# logging.  This parameter has not effect on the workers.  To have a similar
# effect on the workers use the celeryd --logfile parameter.
flags.DEFINE_string('logfile', '',
    'Path to the log file. Leave empty to log to stderr.')

# TODO: get rid of this
LOG = logging.getLogger()

LOGGING_AMQP_FORMAT = '%(asctime)s %(loglevel)-5s %(processName)s' \
    ' [%(name)s] - Job %(job_id)s - %(message)s'
LOGGING_STDOUT_FORMAT = '%(levelname)-5s %(processName)s' \
    ' [%(name)s] - %(message)s'


def init_logs(log_type='console', level='warn'):
    """
    Initialize Python logging.

    The function might be called multiple times with different log levels.
    """

    if log_type == 'console':
        init_logs_stdout(level)
    else:
        init_logs_amqp(level)


def init_logs_stdout(level):
    """Load logging config, and set log levels based on flags"""

    logging_level = LEVELS.get(level, 'warn')

    # Add the logging handler to the root logger.  This will be a file or
    # stdout depending on the presence of the logfile parameter.
    #
    # Note that what we are doing here is just a simplified version of what the
    # standard logging.basicConfig is doing.  An important difference is that
    # we add our handler every time init_logs() is called, whereas basicConfig
    # does nothing if there is at least one handler (any handler) present.
    # This allows us to call init_logs multiple times during the unittest, to
    # reinstall our handler after nose (actually its logcapture plugin) throws
    # it away.
    found = False
    for hdlr in LOG.handlers:
        if (isinstance(hdlr, logging.FileHandler)
            or isinstance(hdlr, logging.StreamHandler)):
            found = True

    if not found:
        filename = FLAGS.get('logfile', '')
        if filename:
            hdlr = logging.FileHandler(filename, 'a')
        else:
            hdlr = logging.StreamHandler()

        hdlr.setFormatter(
            logging.Formatter(LOGGING_STDOUT_FORMAT, None))
        LOG.addHandler(hdlr)

    LOG.setLevel(logging_level)


def init_logs_amqp(level):
    """Init Python and Java logging to log to AMQP"""

    logging_level = LEVELS.get(level, 'warn')

    # loggers are organized in a hierarchy with the root logger at the
    # top; by default log messages are handled first by the logger
    # that receives the .info/.warn/etc. call and then in turn by all
    # its ancestor (up to the root logger)
    #
    # setting .propagate to False avoids log messages coming from
    # amqplib being propagated up the logger chain up to the root
    # logger, which then tries to use the AMQP appender to log and
    # (potentially) causes an infinite loop
    amqp_log = logging.getLogger("amqplib")
    amqp_log.propagate = False

    # initialize Python logging
    LOG.setLevel(logging_level)


class AMQPHandler(logging.Handler):  # pylint: disable=R0902
    """
    Logging handler that sends log messages to AMQP.

    Transmitted log records are represented as json-encoded dictionaries
    with values of LogRecord object enclosed. Those values should be enough
    to reconstruct LogRecord upon receiving.

    :param level: minimum logging level to be sent.
    """

    #: Routing key for a record is generated by formatting the record
    #: with this format. All the same keys as for usual log records
    #: are available, but very few make sense being in routing key.
    #: Using format "%(name)s" makes log records be routed by logger
    #: name (like "oq.job.123" for job logger).
    ROUTING_KEY_FORMAT = "%(name)s"

    # pylint: disable=R0913
    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self, level=level)
        self.routing_key_formatter = logging.Formatter(self.ROUTING_KEY_FORMAT)
        self.connection = None
        self.channel = None

    def _connect(self):
        """Create a new connection to the AMQP server"""
        if self.connection and self.channel:
            return self.channel

        cfg = config.get_section("amqp")
        self.connection = kombu.BrokerConnection(hostname=cfg['host'],
                                                 userid=cfg['user'],
                                                 password=cfg['password'],
                                                 virtual_host=cfg['vhost'])
        self.channel = self.connection.channel()
        self.exchange = kombu.entity.Exchange(cfg['exchange'], type='topic',
                                              channel=self.channel)
        self.producer = kombu.messaging.Producer(self.channel, self.exchange,
                                                 serializer='json')

    def emit(self, record):
        # exc_info objects are not easily serializable
        # so we can not support "logger.exception()"
        assert not record.exc_info
        data = vars(record).copy()
        # instead of 'msg' with placeholders putting formatted message
        # and removing args list to guarantee serializability no matter
        # what was in args
        data['msg'] = record.getMessage()
        data['args'] = ()
        data['hostname'] = socket.getfqdn()

        channel = self._connect()
        routing_key = self.routing_key_formatter.format(record)
        self.producer.publish(data, routing_key)


class AMQPLogSource(AMQPMessageConsumer):
    """
    Receiving part of logging-over-AMQP solution.

    Works in pair with :class:`AMQPHandler`: receives its log messages
    with respect to provided routing key -- logger name. Relogs all received
    log records.
    """
    def message_callback(self, record_data, msg):
        """
        Create log record and handle it.

        Never stops :meth:`consumers's execution
        <openquake.signalling.AMQPMessageConsumer.run>`.
        """
        record = object.__new__(logging.LogRecord)
        record.__dict__.update(record_data)
        logger = logging.getLogger(record.name)
        if logger.isEnabledFor(record.levelno):
            logger.handle(record)
