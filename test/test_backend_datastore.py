# The MIT License (MIT)
#
# Copyright (c) 2016 Fabio Franco Uechi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from . import TestCase
from flagon.backends.datastore import DatastoreBackend, FeatureToggle

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestAppengineDatastoreBackend(TestCase):
    """
    Test the mongo database backend class.
    """

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.backend = DatastoreBackend()

        FeatureToggle(id='input', enabled=True).put()
        FeatureToggle(id='isoff', enabled=False).put()

        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_exists(self):
        """
        Verify Backend.exists raises.
        """
        assert self.backend.exists('input') is True
        assert self.backend.exists('notthere') is False

    def test_is_active(self):
        """
        Verify Backend.is_active raises.
        """
        assert self.backend.is_active('input') is True
        assert self.backend.is_active('isoff') is False

    def test_turn_on(self):
        """
        Verify Backend.turn_on raises.
        """
        self.backend.turn_on('isoff')
        assert self.backend.is_active('isoff') is True

    def test_turn_off(self):
        """
        Verify Backend.turn_off raises.
        """
        self.backend.turn_off('input')
        assert self.backend.is_active('input') is False

    def test_toggle(self):
        """
        Verify Backend.toggle raises.
        """
        self.backend.toggle('input')
        assert self.backend.is_active('input') is False

    def test_is_off(self):
        """
        Verify Backend.is_off raises.
        """
        assert self.backend.is_off('isoff') is True
