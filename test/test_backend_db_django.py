
import os

if not os.environ.get('DJANGO_SETTINGS_MODULE', None):
    from unittest import SkipTest
    raise SkipTest('Django environment not set up.')


from django.test import TestCase
from flagon.backends.db_django import DjangoORMBackend
from flagon.backends.db_django.models import FlagonFeature


class TestBackendDBDjango(TestCase):
    """
    Test the DjangoORMBackend class.
    """

    def setUp(self):
        """
        Set up some items we can reuse.
        """
        self.backend = DjangoORMBackend()

    def test_exists(self):
        """
        Verify Backend.exists returns proper info.
        """
        assert self.backend.exists('exists') is False
        # Create it and verify it now exists
        FlagonFeature(name='exists', active=True).save()
        assert self.backend.exists('exists')

    def test_is_active(self):
        """
        Verify Backend.is_active returns if the features is active.
        """
        FlagonFeature(name='active', active=True).save()
        FlagonFeature(name='notactive', active=False).save()
        assert self.backend.is_active('active')
        assert self.backend.is_active('notactive') is False

    def test_turn_on(self):
        """
        Verify Backend.turn_on turns a feature on.
        """
        FlagonFeature(name='wasoff', active=False).save()
        assert self.backend.is_active('wasoff') is False
        self.backend.turn_on('wasoff')
        assert self.backend.is_active('wasoff')

    def test_turn_off(self):
        """
        Verify Backend.turn_off turns a feature off.
        """
        FlagonFeature(name='wason', active=True).save()
        assert self.backend.is_active('wason')
        self.backend.turn_off('wason')
        assert self.backend.is_active('wason') is False

    def test_toggle(self):
        """
        Verify Backend.toggle flips the feature to it's reverse status.
        """
        FlagonFeature(name='toggle', active=True).save()
        assert self.backend.is_active('toggle')
        self.backend.toggle('toggle')
        assert self.backend.is_active('toggle') is False
        self.backend.toggle('toggle')
        assert self.backend.is_active('toggle')

    def test_is_off(self):
        """
        Verify Backend.is_off returns if the feature is off.
        """
        FlagonFeature(name='isnotoff', active=True).save()
        FlagonFeature(name='isoff', active=False).save()
        assert self.backend.is_off('isnotoff') is False
        assert self.backend.is_off('isoff')
