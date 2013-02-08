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
# along with Dodai.  If not, see <http://www.gnu.org/licenses/>

import unittest
from test.parse.fixture import ParseIniFixture
from dodai.parse.ini import ParseIni


class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._fixture = ParseIniFixture.load()

    @classmethod
    def tearDownClass(cls):
        cls._fixture.destroy()

    def test_parse_ini_section_names(self):
        parse_data = ParseIni(self._fixture.name)
        data = parse_data()

        for key in self._fixture.data:
            self.assertIn(key, data)

    def test_parse_ini_section_keys(self):
        parse_data = ParseIni(self._fixture.name)
        data = parse_data()
        for section in self._fixture.data:
            for key in self._fixture.data[section]:
                self.assertIn(key, data[section])

    def test_parse_ini_section_values(self):
        parse_data = ParseIni(self._fixture.name)
        data = parse_data()
        for section in self._fixture.data:
            for key in self._fixture.data[section]:
                val = "{0}".format(self._fixture.data[section][key])
                self.assertEqual(val, data[section][key])

    def test_parse_ini_with_additional_data(self):
        test_data = {
            'test_dodai__section_one': dict(name='Hello'),
            'test_dodai__section_two': dict(name='Again')
        }
        parse_data = ParseIni(self._fixture.name)
        data = parse_data(dictionary=test_data)
        for section in test_data:
            for key in test_data[section]:
                val = "{0}".format(test_data[section][key])
                self.assertEqual(val, data[section][key])
