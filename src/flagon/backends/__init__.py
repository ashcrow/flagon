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
        """
        raise NotImplementedError('exists must be implemented.')

    def is_on(self, name):
        """
        Checks if a feature is on.
        """
        raise NotImplementedError('is_on must be implemented.')

    def turn_on(self, name):
        """
        Turns a feature on.
        """
        raise NotImplementedError('turn_on must be implemented.')

    def turn_off(self, name):
        """
        Turns a feature off.
        """
        raise NotImplementedError('turn_off must be implemented.')

    def toggle(self, name):
        """
        Toggles a feature.
        """
        if self.is_on(name):
            self.turn_off(name)
        else:
            self.turn_on(name)

    def is_off(self, name):
        """
        Checks if a feature is off.
        """
        return not self.is_on(name)
