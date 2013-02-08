# Copyright (C) 2012  Leonard Thomas
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

import os
import sys
from dodai.util import find

class UtilFixture(object):

    PROJECT = "__test__dodai__"
    CONFIG_FILES = ('cfg', 'connection.txt', 'databases.ini',)
    CUSTOM_CONFIG_FILES = ('test_custom_dodai', 'another_test',)
    BOGUS_FILES = ('bogus_file_one', 'bogus_file_two',)

    def __init__(self, directory):
        self.directory = directory
        self._filenames_ = []
        self._custom_filenames_ = []
        self._bogus_filenames_ = []
        self._all_filenames_ = []
        self._good_filenames_ = []

    @classmethod
    def load(cls):

        directory = find.home_directory(cls.PROJECT)
        obj = cls(directory)
        obj.build()
        return obj

    @property
    def filenames(self):
        if not self._filenames_:
            for name in self.CONFIG_FILES:
                self._filenames_.append(os.path.join(self.directory, name))
        return self._filenames_

    @property
    def custom_filenames(self):
        if not self._custom_filenames_:
            for name in self.CUSTOM_CONFIG_FILES:
                self._custom_filenames_.append(os.path.join(self.directory,
                                                            name))
        return self._custom_filenames_

    @property
    def bogus_filenames(self):
        if not self._bogus_filenames_:
            for name in self.BOGUS_FILES:
                self._bogus_filenames_.append(os.path.join(self.directory,
                                                           name))
        return self._bogus_filenames_

    @property
    def all_filenames(self):
        if not self._all_filenames_:
            self._all_filenames_ = self.filenames + self.custom_filenames +\
                                                    self.bogus_filenames
        return self._all_filenames_

    @property
    def good_filenames(self):
        if not self._good_filenames_:
            self._good_filenames_ = self.filenames + self.custom_filenames
        return self._good_filenames_

    def _clean_up(self):
        if os.path.exists(self.directory):
            if os.path.isdir(self.directory):
                for root, dirs, files in os.walk(self.directory,
                                                 topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(self.directory)
            else:
                os.remove(self.directory)

    def build(self):
        self._clean_up()
        os.mkdir(self.directory)

        for path in self.all_filenames:
            with open(path, 'w') as f:
                pass

    def destroy(self):
        self._clean_up()
