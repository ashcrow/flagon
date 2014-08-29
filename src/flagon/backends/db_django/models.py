from django.db import models


class FlagonParams(models.Model):
    """
    Parameters for a feature.
    """
    key = models.CharField(max_length=255)
    value = models.TextField()
    type = models.CharField(
        max_length=30,
        choices=(('bool', 'bool'), ('int', 'int'), ('str', 'str')))

    def __repr__(self):
        return unicode("%s=%s(%s)" % (self.key, self.type, self.value))

    __str__ = __repr__


class FlagonFeature(models.Model):
    """
    A feature.
    """
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    strategy = models.CharField(max_length=255, blank=True, null=True)
    params = models.ForeignKey(FlagonParams, null=True, blank=True)

    def __repr__(self):
        return unicode(self.name)

    __str__ = __repr__
