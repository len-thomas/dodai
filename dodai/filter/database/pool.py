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

from dodai.validate.database import IsValidDatabaseConnectionSection


class DatabasePool(object):
    """ Object takes in a config dictionary
    """

    def __init__(self, sections, is_valid_database_connection_section):
        self._sections = sections
        self._is_valid_database_connection_section =\
                                        is_valid_database_connection_section


    @classmethod
    def load(cls, sections, log=None, raise_errors=True, prefix=None):
        is_valid_database_connection_section = \
                    IsValidDatabaseConnectionSection(
            sections, log, raise_errors, prefix)
        return cls(sections, is_valid_database_connection_section)




    def process(self):

        for section in self._sections.keys():
            if self._is_valid_database_connection_section(section):
                pass
