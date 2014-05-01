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

    turn_on = lambda s, name: _turn(s, name, True)
    turn_off = lambda s, name: _turn(s, name, False)
