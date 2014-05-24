from django.db import models

from flagon import errors
from flagon.backends import Backend


class FlagonParams(models.Model):
    """
    Parameters for a feature.
    """
    key = models.CharField(max_length=255)
    value = models.TextField()
    type = models.CharField(max_length=30)


class FlagonFeature(models.Model):
    """
    A feature.
    """
    name = models.CharField(max_length=255)
    active = models.BooleanField()
    strategy = models.CharField(max_length=255, null=True)
    params = models.ForeignKey(FlagonParams)


class DjangoORMBackend(Backend):

    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        try:
            FlagonFeature.objects.get(name=name)
            return True
        except FlagonFeature.DoesNotExist:
            return False

    def is_active(self, name):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """
        try:
            feature = FlagonFeature.objects.get(name=name)
            return feature.active
        except FlagonFeature.DoesNotExist:
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)

    def _turn(self, name, value):
        """
        Turns a feature on or off

        :param name: name of the feature.
        :param value: Value to turn name to.
        :raises: UnknownFeatureError
        """
        try:
            feature = FlagonFeature.objects.get(name=name)
            feature.active = bool(value)
            feature.save()
        except FlagonFeature.DoesNotExist:
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)

    turn_on = lambda s, name: _turn(s, name, True)
    turn_off = lambda s, name: _turn(s, name, False)
