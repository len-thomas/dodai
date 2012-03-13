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

from dodai.test.base import RandomProject
from dodai.parse import Parse
from collections import OrderedDict

class TestParse(RandomProject):

    def test_parsed_section_names(self):
        parse_data = Parse(self.project.name)
        data = parse_data()

        # Reverse
        for key in self.project.data:
            self.assertIn(key, data)

    def test_parsed_section_keys(self):
        parse_data = Parse(self.project.name)
        data = parse_data()
        for section in self.project.data:
            for key in self.project.data[section]:
                self.assertIn(key, data[section])

    def test_paarse_section_values(self):
        parse_data = Parse(self.project.name)
        data = parse_data()
        for section in self.project.data:
            for key in self.project.data[section]:
                val = "{0}".format(self.project.data[section][key])
                self.assertEqual(val, data[section][key])
