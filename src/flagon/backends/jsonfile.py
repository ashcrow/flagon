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
        """
        Creates an instance of the JSONFileBackend.

        :param filename: Name of the file to read/write.
        :type filename: str
        :rtype: JSONFileBackend
        """
        self._filename = filename

    def _read_file(self):
        """
        Reads the json file and returns the data.

        :rtype: dict
        """
        with open(self._filename, 'r') as json_file:
            return json.load(json_file)

    def _write_file(self, data):
        """
        Dumps the data in passed to the method into a json file.

        :param data: data to write to the file.
        :type data: dict
        """
        with open(self._filename, 'w') as json_file:
            json.dump(json_file)

    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        return name in self._read_file().keys()

    def is_active(self, name):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        if self._read_file()[name]['active']:
            return True
        return False

    def turn_on(self, name):
        """
        Turns a feature on.

        :param name: name of the feature.
        :raises: UnknownFeatureError
        """
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        data = self._read_file()
        data[name]['active'] = True
        self._write_file(data)

    def turn_off(self, name):
        """
        Turns a feature off.

        :param name: name of the feature.
        :raises: UnknownFeatureError
        """
        # TODO: Copy paste --- :-(
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        data = self._read_file()
        data[name]['active'] = False
        self._write_file(data)
