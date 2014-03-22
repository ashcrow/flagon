import warnings

warnings.warn('TogglzFileBackend is not safe for multi-write environments')

from flagon import errors
from flagon.backends import Backend

try:
    from configobj import ConfigObj
except ImportError, ie:
    print "You must install configobj for TogglzFileBackend"
    print "http://www.voidspace.org.uk/python/configobj.html#installing"
    raise ie


class TogglzFileBackend(Backend):
    """
    Support for using Togglz's FileBasedStateRepository
    (see http://www.togglz.org/documentation/repositories.html).

    Currently only on/off functionality is supported.
    """

    def __init__(self, filename):
        self._filename = filename
        self._read_file()

    def _read_file(self):
        self._store = ConfigObj(self._filename)

    def _write_file(self):
        self._store.write()

    def exists(self, name):
        return name.upper() in self._store.keys()

    def is_active(self, name):
        name = name.upper()
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        if self._store[name] == 'true':
            return True
        return False

    def turn_on(self, name):
        name = name.upper()
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self._store[name] = 'true'
        self._write_file()

    def turn_off(self, name):
        # TODO: Copy paste --- :-(
        name = name.upper()
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self._store[name] = 'false'
        self._write_file()
