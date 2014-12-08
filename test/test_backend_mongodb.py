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

from flagon.backends.mongodb import MongoDBBackend

import mock


class TestMongoDBBackend(TestCase):
    """
    Test the mongodb backend class.
    """

    def setUp(self):
        """
        Set up some items we can reuse.
        """
        with mock.patch('flagon.backends.mongodb.pymongo.MongoClient') as _mc:
            self._mc = _mc
            self._mc()['flagon']['features'].find().count.return_value = 1
            self.backend = MongoDBBackend()

    def test_exists(self):
        """
        Verify Backend.exists raises.
        """
        assert self.backend.exists('input') is True

        self._mc()['flagon']['features'].find().count.return_value = 0
        assert self.backend.exists('notthere') is False

    def test_is_active(self):
        """
        Verify Backend.is_active raises.
        """
        self._mc()['flagon']['features'].find_one.return_value = {
            '_id': '',
            'name': 'input',
            'active': True}
        assert self.backend.is_active('input') is True

        self._mc()['flagon']['features'].find_one.return_value = {
            '_id': '',
            'name': 'isoff',
            'active': False}
        assert self.backend.is_active('isoff') is False

    def test_turn_on(self):
        """
        Verify Backend.turn_on raises.
        """
        self.backend.turn_on('input')
        assert self._mc()['flagon']['features'].update.call_count == 1

    def test_turn_off(self):
        """
        Verify Backend.turn_off raises.
        """
        self.backend.turn_off('input')
        assert self._mc()['flagon']['features'].update.call_count == 1

    def test_toggle(self):
        """
        Verify Backend.toggle raises.
        """
        self.backend.toggle('input')
        assert self._mc()['flagon']['features'].update.call_count == 1

    def test_is_off(self):
        """
        Verify Backend.is_off raises.
        """
        self._mc()['flagon']['features'].find_one.return_value = {
            '_id': '',
            'name': 'input',
            'active': False}
        assert self.backend.is_off('input') is True
