# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2012-2020 GEM Foundation
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

import ast
import sys
import time
import logging
import operator
from contextlib import contextmanager
import numpy
from scipy.spatial import cKDTree, distance

from openquake.baselib.python3compat import raise_
from openquake.hazardlib import site
from openquake.hazardlib.geo.utils import (
    KM_TO_DEGREES, angular_distance, fix_lon, get_bounding_box, cross_idl,
    get_longitudinal_extent, BBoxError, spherical_to_cartesian)

U32 = numpy.uint32
MAX_DISTANCE = 2000  # km, ultra big distance used if there is no filter
et_id = operator.attrgetter('et_id')


@contextmanager
def context(src):
    """
    Used to add the source_id to the error message. To be used as

    with context(src):
        operation_with(src)

    Typically the operation is filtering a source, that can fail for
    tricky geometries.
    """
    try:
        yield
    except Exception:
        etype, err, tb = sys.exc_info()
        msg = 'An error occurred with source id=%s. Error: %s'
        msg %= (src.source_id, err)
        raise_(etype, msg, tb)


def getdefault(dic_with_default, key):
    """
    :param dic_with_default: a dictionary with a 'default' key
    :param key: a key that may be present in the dictionary or not
    :returns: the value associated to the key, or to 'default'
    """
    try:
        return dic_with_default[key]
    except KeyError:
        return dic_with_default['default']


def unique_sorted(items):
    """
    Check that the items are unique and sorted
    """
    if len(set(items)) < len(items):
        raise ValueError('Found duplicates in %s' % items)
    elif items != sorted(items):
        raise ValueError('%s is not ordered' % items)
    return items


# used for the maximum distance parameter in the job.ini file
def floatdict(value):
    """
    :param value:
        input string corresponding to a literal Python number or dictionary
    :returns:
        a Python dictionary key -> number

    >>> floatdict("200")
    {'default': 200}

    >>> text = "{'active shallow crust': 250., 'default': 200}"
    >>> sorted(floatdict(text).items())
    [('active shallow crust', 250.0), ('default', 200)]
    """
    value = ast.literal_eval(value)
    if isinstance(value, (int, float, list)):
        return {'default': value}
    dic = {'default': max(value.values())}
    dic.update(value)
    return dic


class MagDepDistance(dict):
    """
    A dictionary trt -> [(mag, dist), ...]
    """
    @classmethod
    def new(cls, value):
        """
        :param value: string to be converted
        :returns: MagDepDistance dictionary

        >>> md = MagDepDistance.new('50')
        >>> md
        {'default': [(1.0, 50), (10.0, 50)]}
        >>> md.max()
        {'default': 50}
        >>> md.interp(dict(default=[5.0, 5.1, 5.2])); md.ddic
        {'default': {'5.00': 50.0, '5.10': 50.0, '5.20': 50.0}}
        """
        items_by_trt = floatdict(value.replace('?', '-1'))
        self = cls()
        for trt, items in items_by_trt.items():
            if isinstance(items, list):
                self[trt] = unique_sorted(items)
                for mag, dist in self[trt]:
                    if mag < 1 or mag > 10:
                        raise ValueError('Invalid magnitude %s' % mag)
            else:  # assume scalar distance
                assert items == -1 or items >= 0, items
                self[trt] = [(1., items), (10., items)]
        return self

    def interp(self, mags_by_trt):
        """
        :param mags_by_trt: a dictionary trt -> magnitudes as strings
        :returns: a dictionary trt->mag->dist
        """
        ddic = {}
        for trt, mags in mags_by_trt.items():
            xs, ys = zip(*getdefault(self, trt))
            if len(mags) == 1:
                ms = [numpy.float64(mags)]
            else:
                ms = numpy.float64(mags)
            dists = numpy.interp(ms, xs, ys)
            ddic[trt] = {'%.2f' % mag: dist for mag, dist in zip(ms, dists)}
        self.ddic = ddic

    def __call__(self, trt, mag=None):
        if not self:
            return MAX_DISTANCE
        elif mag is None:
            return getdefault(self, trt)[-1][1]
        elif hasattr(self, 'ddic'):
            return self.ddic[trt]['%.2f' % mag]
        else:
            xs, ys = zip(*getdefault(self, trt))
            return numpy.interp(mag, xs, ys)

    def max(self):
        """
        :returns: a dictionary trt -> maxdist
        """
        return {trt: self[trt][-1][1] for trt in self}

    def suggested(self):
        """
        :returns: True if there is a ? for any TRT
        """
        return any(self[trt][-1][1] == -1 for trt in self)

    def get_bounding_box(self, lon, lat, trt=None, mag=None):
        """
        Build a bounding box around the given lon, lat by computing the
        maximum_distance at the given tectonic region type and magnitude.

        :param lon: longitude
        :param lat: latitude
        :param trt: tectonic region type, possibly None
        :param mag: magnitude, possibly None
        :returns: min_lon, min_lat, max_lon, max_lat
        """
        if trt is None:  # take the greatest integration distance
            maxdist = max(self(trt, mag) for trt in self)
        else:  # get the integration distance for the given TRT
            maxdist = self(trt, mag)
        a1 = min(maxdist * KM_TO_DEGREES, 90)
        a2 = min(angular_distance(maxdist, lat), 180)
        return lon - a2, lat - a1, lon + a2, lat + a1

    def get_affected_box(self, src):
        """
        Get the enlarged bounding box of a source.

        :param src: a source object
        :returns: a bounding box (min_lon, min_lat, max_lon, max_lat)
        """
        maxdist = self(src.tectonic_region_type)
        try:
            bbox = get_bounding_box(src, maxdist)
        except Exception as exc:
            raise exc.__class__('source %s: %s' % (src.source_id, exc))
        return (fix_lon(bbox[0]), bbox[1], fix_lon(bbox[2]), bbox[3])

    def get_dist_bins(self, trt, nbins=51):
        """
        :returns: an array of distance bins, from 10m to maxdist
        """
        return .01 + numpy.arange(nbins) * self(trt) / (nbins - 1)


def split_sources(srcs):
    """
    :param srcs: sources
    :returns: a pair (split sources, split time) or just the split_sources
    """
    from openquake.hazardlib.source import splittable
    sources = []
    split_time = {}  # src.id -> time
    for src in srcs:
        if not splittable(src):
            sources.append(src)
            continue
        t0 = time.time()
        if not src.num_ruptures:  # not set yet
            src.num_ruptures = src.count_ruptures()
        mag_a, mag_b = src.get_min_max_mag()
        min_mag = src.min_mag
        if mag_b < min_mag:  # discard the source completely
            continue
        if min_mag:
            splits = []
            for s in src:
                s.min_mag = min_mag
                mag_a, mag_b = s.get_min_max_mag()
                if mag_b < min_mag:
                    continue
                s.num_ruptures = s.count_ruptures()
                if s.num_ruptures:
                    splits.append(s)
        else:
            splits = list(src)
        try:
            split_time[src.id] = time.time() - t0
        except AttributeError as exc:  # missing .id, should never happen
            raise AttributeError('%s: %s' % (exc, src.source_id))
        sources.extend(splits)
        has_samples = hasattr(src, 'samples')
        has_scaling_rate = hasattr(src, 'scaling_rate')
        grp_id = getattr(src, 'grp_id', 0)  # 0 in hazardlib
        if len(splits) > 1:
            for i, split in enumerate(splits):
                split.source_id = '%s:%s' % (src.source_id, i)
                split.et_id = src.et_id
                split.grp_id = grp_id
                split.id = src.id
                if has_samples:
                    split.samples = src.samples
                if has_scaling_rate:
                    s.scaling_rate = src.scaling_rate
        elif splits:  # single source
            [s] = splits
            s.source_id = src.source_id
            s.et_id = src.et_id
            s.grp_id = grp_id
            s.id = src.id
            if has_samples:
                s.samples = src.samples
            if has_scaling_rate:
                s.scaling_rate = src.scaling_rate
    return sources, split_time


class SourceFilter(object):
    """
    Filter objects have a .filter method yielding filtered sources
    and the IDs of the sites within the given maximum distance.
    Filter the sources by using `self.sitecol.within_bbox` which is
    based on numpy.
    """
    def __init__(self, sitecol, integration_distance):
        if sitecol is None:
            integration_distance = {}
        self.sitecol = sitecol
        self.integration_distance = (
            integration_distance
            if isinstance(integration_distance, MagDepDistance)
            else MagDepDistance(integration_distance))
        self.slc = slice(None)

    def split_in_tiles(self, hint):
        """
        Split the SourceFilter by splitting the site collection in tiles
        """
        if hint == 1:
            return [self]
        out = []
        for tile in self.sitecol.split_in_tiles(hint):
            sf = self.__class__(tile, self.integration_distance)
            sf.slc = slice(tile.sids[0], tile.sids[-1] + 1)
            out.append(sf)
        return out

    # not used right now
    def reduce(self, factor=100):
        """
        Reduce the SourceFilter to a subset of sites
        """
        idxs = numpy.arange(0, len(self.sitecol), factor)
        sc = object.__new__(site.SiteCollection)
        sc.array = self.sitecol[idxs]
        sc.complete = self.sitecol.complete
        return self.__class__(sc, self.integration_distance)

    def get_rectangle(self, src):
        """
        :param src: a source object
        :returns: ((min_lon, min_lat), width, height), useful for plotting
        """
        min_lon, min_lat, max_lon, max_lat = (
            self.integration_distance.get_affected_box(src))
        return (min_lon, min_lat), (max_lon - min_lon) % 360, max_lat - min_lat

    def get_close_sites(self, source):
        """
        Returns the sites within the integration distance from the source,
        or None.
        """
        source_indices = list(self.filter([source]))
        if source_indices:
            return self.sitecol.filtered(source_indices[0][1])

    def split(self, sources, mon):
        """
        :yields: pairs ([split], sites)
        """
        for src in sources:
            with mon:
                split, dt = split_sources(src)
            for s in split:
                with mon:
                    sites = self.get_close_sites(s)
                if sites is not None:
                    yield [s], sites

    # used in the rupture prefiltering: it should not discard too much
    def close_sids(self, rec, trt):
        """
        :param rec:
           a record with fields mag, minlon, minlat, maxlon, maxlat, hypo
        :param trt:
           tectonic region type string
        :returns:
           the site indices within the maximum_distance of the hypocenter,
           plus the maximum size of the bounding box
        """
        if self.sitecol is None:
            return []
        elif not self.integration_distance:  # do not filter
            return self.sitecol.sids
        if not hasattr(self, 'kdt'):
            self.kdt = cKDTree(self.sitecol.xyz)
        xyz = spherical_to_cartesian(*rec['hypo'])
        dlon = get_longitudinal_extent(rec['minlon'], rec['maxlon'])
        dlat = rec['maxlat'] - rec['minlat']
        delta = max(dlon, dlat) / KM_TO_DEGREES
        maxradius = self.integration_distance(trt) + delta
        sids = U32(self.kdt.query_ball_point(xyz, maxradius, eps=.001))
        sids.sort()
        return sids

    # used for debugging purposes
    def get_cdist(self, rec):
        """
        :returns: array of N euclidean distances from rec['hypo']
        """
        xyz = spherical_to_cartesian(*rec['hypo']).reshape(1, 3)
        return distance.cdist(self.sitecol.xyz, xyz)[:, 0]

    def filter(self, sources):
        """
        :param sources: a sequence of sources
        :yields: sources with indices
        """
        if self.sitecol is None:  # nofilter
            for src in sources:
                yield src, None
            return
        for src in sources:
            try:
                box = self.integration_distance.get_affected_box(src)
            except BBoxError:  # too large, don't filter
                src.nsites = len(self.sitecol)
                yield src, self.sitecol.sids
                continue
            indices = self.sitecol.within_bbox(box)
            if len(indices):
                src.nsites = len(indices)
                yield src, indices

    def within_bbox(self, srcs):
        """
        :param srcs: a list of source objects
        :returns: the site IDs within the enlarged bounding box of the sources
        """
        if self.sitecol is None:  # for test_case_1_ruptures
            return [0]
        lons = []
        lats = []
        for src in srcs:
            try:
                box = self.integration_distance.get_affected_box(src)
            except BBoxError as exc:
                logging.error(exc)
                continue
            lons.append(box[0])
            lats.append(box[1])
            lons.append(box[2])
            lats.append(box[3])
        if cross_idl(*(list(self.sitecol.lons) + lons)):
            lons = numpy.array(lons) % 360
        else:
            lons = numpy.array(lons)
        bbox = (lons.min(), min(lats), lons.max(), max(lats))
        if bbox[2] - bbox[0] > 180:
            raise BBoxError(
                'The bounding box of the sources is larger than half '
                'the globe: %d degrees' % (bbox[2] - bbox[0]))
        return self.sitecol.within_bbox(bbox)

    def __getitem__(self, slc):
        if slc.start is None and slc.stop is None:
            return self
        sitecol = object.__new__(self.sitecol.__class__)
        sitecol.array = self.sitecol[slc]
        sitecol.complete = self.sitecol.complete
        return self.__class__(sitecol, self.integration_distance)


nofilter = SourceFilter(None, {})
