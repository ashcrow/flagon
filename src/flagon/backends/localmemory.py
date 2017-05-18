# The MIT License (MIT)
#
# Copyright (c) 2014 Steve Milner
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
Local memory backend.
"""
import warnings

warnings.warn('LocalMemoryBackend is not safe for '
              'multi-thread/process environments')

from flagon import errors
from flagon.backends import Backend


class LocalMemoryBackend(Backend):

    def __init__(self, data):
        """
        Creates an instance of the LocalMemoryBackend.

        :param data: The initial data structure for features.
        :type filename: dict
        :rtype: LocalMemoryBackend
        """
        self._store = data

    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        return name in self._store.keys()

    def is_active(self, name):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        if self._store[name]['active']:
            return True
        return False

    def _turn(self, name, value):
        """
        Turns a feature off.

        :param name: name of the feature.
        :param value: Value to turn name to.
        :raises: UnknownFeatureError
        """
        # TODO: Copy paste --- :-(
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self._store[name] = bool(value)

    turn_on = lambda s, name: s._turn(name, True)
    turn_off = lambda s, name: s._turn(name, False)
