# The MIT License (MIT)
#
# Copyright (c) 2016 Fabio Franco Uechi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
"""
Appengine Datastore backend.
"""
import ndb

from flagon import errors
from flagon.backends import Backend


class FeatureToggle(ndb.Model):

    enabled = ndb.BooleanProperty(indexed=False)
    strategy_id = ndb.StringProperty('strategyId', indexed=False)
    strategy_params_names = ndb.StringProperty('strategyParamsNames', indexed=False, repeated=True)
    strategy_params_values = ndb.StringProperty('strategyParamsValues', indexed=False, repeated=True)


class DatastoreBackend(Backend):
    """Appengine Datastore Backend for flagon"""

    def __init__(self):
        pass

    @ndb.non_transactional
    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """

        if FeatureToggle.get_by_id(name) is None:
            return False
        else:
            return True

    @ndb.non_transactional
    def is_active(self, name):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """

        ft = FeatureToggle.get_by_id(name)
        if ft is None:
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        else:
            return ft.enabled

    @ndb.non_transactional
    def _turn(self, name, value):
        """
        Turns a feature off.

        :param name: name of the feature.
        :param value: Value to turn name to.
        :raises: UnknownFeatureError
        """
        ft = FeatureToggle.get_by_id(name)
        if ft is None:
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)

        ft.active = bool(value)
        ft.put()

    turn_on = lambda s, name: s._turn(name, True)
    turn_off = lambda s, name: s._turn(name, False)
