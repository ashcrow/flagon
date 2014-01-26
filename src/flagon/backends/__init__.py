"""
Backend sources for managing feature flags.
"""


class Backend(object):

    def exists(self, name):
        raise NotImplementedError('exists must be implemented.')

    def is_on(self, name):
        raise NotImplementedError('is_on must be implemented.')

    def turn_on(self, name):
        raise NotImplementedError('turn_on must be implemented.')

    def turn_off(self, name):
        raise NotImplementedError('turn_off must be implemented.')

    def toggle(self, name):
        if self.is_on(name):
            self.turn_off(name)
        else:
            self.turn_on(name)

    def is_off(self, name):
        return not self.is_on(name)
