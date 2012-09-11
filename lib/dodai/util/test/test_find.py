# Copyright (C) 2011  Leonard Thomas
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
from dodai.util import find
import os
import sys
import platform

class TestBasicFind(unittest.TestCase):

    def setUp(self):
        self.project = 'test'

    def test_find_home_directory(self):
        directory = find.home_direcotry()
        self.assertTrue(os.path.exists(directory))

    def test_find_home_directory_with_project(self):
        directory = find.home_direcotry(self.project)
        self.assertTrue(directory.endswith(self.project))

    def test_find_system_config_directory(self):
        directory = find.system_config_directory()
        self.assertTrue(os.path.exists(directory))

    def test_find_system_config_directory_with_project(self):
        directory = find.system_config_directory(self.project)
        self.assertTrue(directory.endswith(self.project))

    def test_find_project_config_directory(self):
        directory = find.project_config_directory(False)
        self.assertTrue(os.path.exists(directory))

    def test_find_project_config_directory_with_config(self):
        directory = find.project_config_directory()
        self.assertTrue(directory.endswith('config'))

    def test_find_config_directories(self):
        directories = find.config_directories(self.project)
        self.assertEqual(len(directories), 3)

    def test_find_system_encoding(self):
        encoding = find.system_encoding()
        system = platform.system()
        if system in ('Linux', 'Darwin'):
            self.assertEqual(encoding, 'utf-8')
        else:
            self.assertGreater(len(encoding), 0)



class TestFindConfigFiles(unittest.TestCase):

    @property
    def project(self):
        if not hasattr(self, '_project_') or not self._project_:
            self._project_ = "__test__dodai__"
        return self._project_

    @property
    def filenames(self):
        if not hasattr(self, '_filenames_') or not self._filenames_:
            self._filenames_ = []
            directory = find.home_direcotry(self.project)
            names = ['cfg', 'connection.txt', 'databases.ini']
            for name in names:
                self._filenames_.append(os.path.join(directory, name))
        return self._filenames_

    @property
    def custom_filenames(self):
        if (not hasattr(self, '_custom_filenames_')
                                        or not self._custom_filenames_):
            directory = find.home_direcotry(self.project)
            self._custom_filenames_ = []
            names = ['__test_dodai_filename__', '__another_test_dodai_file']
            for name in names:
                self._custom_filenames_.append(os.path.join(directory, name))
        return self._custom_filenames_

    def setUp(self):

        # make sure the test directory is deleted
        self._clean_up()

        directory = find.home_direcotry(self.project)
        os.mkdir(directory)

        all_files = self.filenames + self.custom_filenames

        for path in all_files:
            with open(path, 'w') as f:
                pass

    def tearDown(self):
        self._clean_up()

    def _clean_up(self):
        directory = find.home_direcotry(self.project)
        if os.path.exists(directory):
            if os.path.isdir(directory):
                for root, dirs, files in os.walk(directory, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(directory)
            else:
                os.remove(directory)


    def test_find_config_file_object(self):
        obj = find.ConfigFiles(find.config_directories(self.project),
                               find.system_encoding())
        results = self.filenames + self.custom_filenames
        files = obj(self.custom_filenames)
        for name in files:
            self.assertTrue(name.name in results)
