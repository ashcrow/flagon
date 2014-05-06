
from . import TestCase

from flagon.backends import Backend


class TestBackend(TestCase):
    """
    Test the parent backend class.
    """

    def setUp(self):
        """
        Set up some items we can reuse.
        """
        self.backend = Backend()

    def test_exists(self):
        """
        Verify Backend.exists raises.
        """
        self.assertRaises(NotImplementedError, self.backend.exists, 'input')

    def test_is_active(self):
        """
        Verify Backend.is_active raises.
        """
        self.assertRaises(NotImplementedError, self.backend.is_active, 'input')

    def test_turn_on(self):
        """
        Verify Backend.turn_on raises.
        """
        self.assertRaises(NotImplementedError, self.backend.turn_on, 'input')

    def test_turn_off(self):
        """
        Verify Backend.turn_off raises.
        """
        self.assertRaises(NotImplementedError, self.backend.turn_off, 'input')

    def test_toggle(self):
        """
        Verify Backend.toggle raises.
        """
        self.assertRaises(NotImplementedError, self.backend.toggle, 'input')

    def test_is_off(self):
        """
        Verify Backend.is_off raises.
        """
        self.assertRaises(NotImplementedError, self.backend.is_off, 'input')
