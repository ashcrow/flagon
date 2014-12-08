# The MIT License (MIT)
#
# Copyright (c) 2014 Steve Milner
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
