import warnings

warnings.warn('JSONFileBackend is not safe for multi-write environments')

try:
    import json
except ImportError:
    import simplejson as json

from flagon import errors
from flagon.backends import Backend


class JSONFileBackend(Backend):

    def __init__(self, filename):
        self._filename = filename

    def _read_file(self):
        with open(self._filename, 'r') as json_file:
            return json.load(json_file)

    def _write_file(self, data):
        with open(self._filename, 'w') as json_file:
            json.dump(json_file)

    def exists(self, name):
        return name in self._read_file().keys()

    def is_active(self, name):
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        if self._read_file()[name]['active']:
            return True
        return False

    def turn_on(self, name):
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        data = self._read_file()
        data[name]['active'] = True
        self._write_file(data)

    def turn_off(self, name):
        # TODO: Copy paste --- :-(
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        data = self._read_file()
        data[name]['active'] = False
        self._write_file(data)
