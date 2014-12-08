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
Redis backend.
"""
import redis

from flagon import errors
from flagon.backends import Backend


class RedisBackend(Backend):

    def __init__(self, host, port, db):
        """
        Creates an instance of the RedisBackend.

        :rtype: RedisBackend
        """
        # https://pypi.python.org/pypi/redis/2.10.1
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        self._server = redis.Redis(
            connection_pool=pool,
            charset='utf-8',
            errors='strict',
            decode_responses=False)

    def set(self, name, key, value):
        """
        Sets a value for a feature. This is a proposed name only!!!

        :param name: name of the feature.
        :rtype: bool
        """
        self._server.hset(name, key, value)

    def exists(self, name, key):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        return self._server.hexists(name, key)

    def is_active(self, name, key):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """
        if not self._server.hexists(name, key):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        if self._server.hget(name, key) == 'True':
            return True
        return False

    def _turn(self, name, key, value):
        """
        Turns a feature off.

        :param name: name of the feature.
        :param value: Value to turn name to.
        :raises: UnknownFeatureError
        """
        # TODO: Copy paste --- :-(
        if not self._server.hexists(name, key):
            raise errors.UnknownFeatureError('Unknown feature: %s %s' % (
                name, key))
        self._server.hset(name, key, value)

    turn_on = lambda s, name: s._turn(name, 'active', True)
    turn_off = lambda s, name: s._turn(name, 'active', False)
