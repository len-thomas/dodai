# Copyright (C) 2012 Leonard Thomas
#
# This file is part of Dodai.
#
# Dodai is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dodai is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dodai.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from dodai.validate.ignore import ShouldIgnore

class TestShouldIgnore(unittest.TestCase):

    DATA = {
        'green': {
            'foo': 'bar',
            'ignore': 'True'
        },
        'blue': {
            'foo': 'bar',
            'ignore': 'false'
        },
        'yellow': {
            'foo': 'bar'
        },
        'red': {
            'foo': 'bar',
            'ignore': 'yes'
        },
        'orange': {
            'foo': 'bar',
            'ignore': 'no'
        },
        'purple': {
            'foo': 'bar',
            'ignore': 'maybe'
        }
    }

    def setUp(self):
        self.should_ignore = ShouldIgnore(self.DATA)

    def test_green(self):
        self.assertTrue(self.should_ignore('green'))

    def test_blue(self):
        self.assertFalse(self.should_ignore('blue'))

    def test_yellow(self):
        self.assertFalse(self.should_ignore('yellow'))

    def test_red(self):
        self.assertTrue(self.should_ignore('red'))

    def test_orange(self):
        self.assertFalse(self.should_ignore('orange'))

    def test_purple(self):
        self.assertFalse(self.should_ignore('purple'))
