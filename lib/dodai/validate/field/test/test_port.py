#
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
from dodai.validate.field.port import IsValidPort


class TestValidatePort(unittest.TestCase):

    def setUp(self):
        self._validate = IsValidPort.load(self.sections)

    @property
    def sections(self):
        if not hasattr(self, '_sections_') or not self._sections_:
            self._sections_ = {
                'blue': {
                    'port': '12345',
                },
                'red': {
                    'port': '6553555'
                },
                'orange': {
                    'port': 'foo'
                }
            }
        return self._sections_

    def test_is_valid(self):
        self.assertTrue(self._validate('blue'))

    def test_not_valid(self):
        with self.assertRaises(ValueError):
            self._validate('red')
            self._validate('oragne')
