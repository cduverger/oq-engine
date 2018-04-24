# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2015-2018 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.
import numpy
from openquake.baselib import sap, datastore
from openquake.calculators.extract import extract


def make_figure(losses_by_rlzi, loss_types):
    """
    :param losses_by_event: composite array (eid, rlzi, losses)
    :param loss_types: list of loss types
    """
    # NB: matplotlib is imported inside since it is a costly import
    import matplotlib.pyplot as plt
    R = len(losses_by_rlzi)
    L = len(loss_types)
    fig = plt.figure()
    for rlz in losses_by_rlzi:
        rlzi = int(rlz[4:])  # strip rlz-
        losses = losses_by_rlzi[rlz]
        print('%s, num_events=%d' % (rlz, len(losses)))
        for lti, lt in enumerate(loss_types):
            if numpy.isnan(losses[lt]).all():
                continue
            ax = fig.add_subplot(R, L, rlzi * L + lti + 1)
            ax.set_xlabel('%s, loss_type=%s' % (rlz, lt))
            ax.hist(losses[lt], 7, rwidth=.9)
            ax.set_title('loss=%.5e$\pm$%.5e' %
                         (losses[lt].mean(), losses[lt].std(ddof=1)))
    return plt


@sap.Script
def plot_losses(calc_id):
    """
    losses_by_event plotter
    """
    # read the hazard data
    dstore = datastore.read(calc_id)
    losses_by_rlzi = dict(extract(dstore, 'losses_by_event'))
    oq = dstore['oqparam']
    plt = make_figure(losses_by_rlzi, oq.loss_dt().names)
    plt.show()

plot_losses.arg('calc_id', 'a computation id', type=int)
