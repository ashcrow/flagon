import memcache

from flagon import errors
from flagon.backends import Backend

class MemcachedBackend(Backend):
    """Memcache Backend for flagon"""
    def __init__(self, hostname="127.0.0.1", port="11211"):
        self.hostname = "%s:%s" % (hostname, port)
        self.server   = memcache.Client([self.hostname])

    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        if self.server.get(name) is None:
            return False
        else:
            return True

    def is_active(self, name):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        if self.server.get(name)['active']:
            return True
        return False

    def _turn(self, name, value):
        """
        Turns a feature off.

        :param name: name of the feature.
        :param value: Value to turn name to.
        :raises: UnknownFeatureError
        """
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self.server.set(name, {'active': bool(value)})

    turn_on = lambda s, name: s._turn(name, True)
    turn_off = lambda s, name: s._turn(name, False)
