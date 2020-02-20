# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2020, GEM Foundation
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
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.

import logging
import toml
from openquake.baselib import sap
from openquake.commonlib.writers import write_csv
from openquake.commonlib.logictree import SourceModelLogicTree


@sap.script
def ltcsv(fname):
    """
    Convert logic tree source model file from XML into CSV
    """
    smlt = SourceModelLogicTree(fname)
    dic, _ = smlt.__toh5__()
    out = write_csv(fname[:-4] + '.csv', dic['branches'],
                    comment=toml.loads(dic['branchsets']))
    logging.info('Saved %s', out)


ltcsv.arg('fname', 'path to the source model logic tree')
