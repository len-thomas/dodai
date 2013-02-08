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

import unittest
from dodai.util import find
import os
import sys
import platform
import tempfile
from test.util.fixture import UtilFixture

class TestBasicFind(unittest.TestCase):

    def setUp(self):
        self.project = 'test'

    def test_find_tmp_directory(self):
        with tempfile.NamedTemporaryFile() as f:
            should_be = os.path.dirname(f.name)
        value = find.tmp_directory()
        self.assertEqual(should_be, value)

    def test_find_home_directory(self):
        directory = find.home_directory()
        self.assertTrue(os.path.exists(directory))

    def test_find_home_directory_with_project(self):
        directory = find.home_directory(self.project)
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

    @classmethod
    def setUpClass(cls):
        cls._fixture = UtilFixture.load()

    @classmethod
    def tearDownClass(cls):
        cls._fixture.destroy()

    def test_find_config_file_object_one(self):
        error_message = "The file '{0}' should have been loaded by the "\
                        "dodai.util.find.ConfigFile object."

        obj = find.ConfigFiles(find.config_directories(self._fixture.PROJECT),
                               find.system_encoding())
        files = obj(self._fixture.custom_filenames)
        for name in files:
            msg = error_message.format(name)
            self.assertTrue(name.name in self._fixture.good_filenames, msg=msg)

    def test_find_config_file_object_two(self):
        error_message = "The file '{0}' should have been loaded by the "\
                        "dodai.util.find.ConfigFile object"

        obj = find.ConfigFiles(find.config_directories(self._fixture.PROJECT),
                               find.system_encoding())
        files = obj(self._fixture.custom_filenames)

        loaded_files = []
        for name in files:
            loaded_files.append(name.name)

        for name in self._fixture.good_filenames:
            msg = error_message.format(name)
            self.assertTrue(name in loaded_files, msg=msg)

    def test_find_config_file_object_three(self):
        error_message = "The file '{0}' should NOT have been loaded by the "\
                        "dodai.util.find.ConfigFile object"

        obj = find.ConfigFiles(find.config_directories(self._fixture.PROJECT),
                               find.system_encoding())
        files = obj(self._fixture.custom_filenames)

        loaded_files = []
        for name in files:
            loaded_files.append(name.name)

        for name in self._fixture.bogus_filenames:
            msg = error_message.format(name)
            self.assertFalse(name in loaded_files, msg=msg)

    def test_find_config_files_one(self):
        error_message = "The file '{0}' should have been loaded by the "\
                        "dodai.util.find.config_files function."

        files = find.config_files(self._fixture.PROJECT,
                                  self._fixture.custom_filenames)
        for name in files:
            msg = error_message.format(name)
            self.assertTrue(name.name in self._fixture.good_filenames, msg=msg)

    def test_find_config_files_two(self):
        error_message = "The file '{0}' should have been loaded by the "\
                        "dodai.util.find.config_files function"

        files = find.config_files(self._fixture.PROJECT,
                                  self._fixture.custom_filenames)

        loaded_files = []
        for name in files:
            loaded_files.append(name.name)

        for name in self._fixture.good_filenames:
            msg = error_message.format(name)
            self.assertTrue(name in loaded_files, msg=msg)

    def test_find_config_files_three(self):
        error_message = "The file '{0}' should NOT have been loaded by the "\
                        "dodai.util.find.conf_files function"

        files = find.config_files(self._fixture.PROJECT,
                                  self._fixture.custom_filenames)

        loaded_files = []
        for name in files:
            loaded_files.append(name.name)

        for name in self._fixture.bogus_filenames:
            msg = error_message.format(name)
            self.assertFalse(name in loaded_files, msg=msg)
