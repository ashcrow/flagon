"""
Backend sources for managing feature flags.
"""


class Backend(object):
    """
    Parent class for all backends.
    """

    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        """
        raise NotImplementedError('exists must be implemented.')

    def is_active(self, name):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        """
        raise NotImplementedError('is_active must be implemented.')

    def turn_on(self, name):
        """
        Turns a feature on.

        :param name: name of the feature.
        """
        raise NotImplementedError('turn_on must be implemented.')

    def turn_off(self, name):
        """
        Turns a feature off.

        :param name: name of the feature.
        """
        raise NotImplementedError('turn_off must be implemented.')

    def toggle(self, name):
        """
        Toggles a feature.

        :param name: name of the feature.
        """
        if self.is_active(name):
            self.turn_off(name)
        else:
            self.turn_on(name)

    def is_off(self, name):
        """
        Checks if a feature is off.

        :param name: name of the feature.
        """
        return not self.is_active(name)
