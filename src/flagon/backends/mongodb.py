import pymongo

from flagon import errors
from flagon.backends import Backend


class MongoDBBackend(Backend):
    """MongoDB Backend for flagon"""

    def __init__(
            self,
            connection_str='mongodb://localhost:27017/',
            database='flagon',
            collection='features'):
        """
        Creates an instance of the MongoDBBackend.
        """
        self._connection = pymongo.MongoClient(connection_str)
        print self._connection
        self._db = self._connection[database]
        self._collection = self._db[collection]

    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        if self._collection.find({'name': name}).count() == 0:
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
        if self._collection.find_one({'name': name})['active']:
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
        instance = self._collection.find_one({'name': name})
        self._collection.update(
            {'_id': instance['_id']}, {'$set': {'active': bool(value)}})

    turn_on = lambda s, name: s._turn(name, True)
    turn_off = lambda s, name: s._turn(name, False)
