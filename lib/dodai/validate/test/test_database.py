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
from dodai.validate.database import IsDatabaseConnectionSection
from dodai.validate.database import IsValidDatabaseConnectionSection

class TestIsDatabaseConnectionSection(unittest.TestCase):

    DATA = {
        'db.green': {
            'dialect': 'mysql',
        },
        'db.brown': {
            'dialect': 'postgresql',
            'ignore': 'true'
        },
        'red': {
            'dialect': 'access'
        },
        'db.orange': {
            'dialect': 'foobar'
        }
    }

    def setUp(self):
        self.is_database_section = IsDatabaseConnectionSection.load(self.DATA)

    def test_missing(self):
        with self.assertRaises(KeyError):
            self.is_database_section('grey')

    def test_green(self):
        self.assertTrue(self.is_database_section('db.green'))

    def test_brown(self):
        self.assertFalse(self.is_database_section('db.brown'))

    def test_red(self):
        self.assertFalse(self.is_database_section('red'))

    def test_orange(self):
        with self.assertRaises(ValueError):
            self.is_database_section('db.orange')


class TestIsValidDatabaseConnectionSection(unittest.TestCase):

    DATA = {
        'db.green': {
            'dialect': 'sqlite',
            'path': '/foo'
        },
        'db.brown': {
            'dialect': 'postgresql',
            'host': 'example.com',
            'port': '1234',
            'username': 'foo',
            'password': 'bar',
            'database': 'test',
            'schema': 'foobar'
        },
        'db.red': {
            'dialect': 'access'
        },
        'db.orange': {
            'dialect': 'oracle',
            'host': 'example.com',
            'port': '1234',
            'username': 'foo',
            'password': 'bar',
            'database': 'test'
        }
    }

    def setUp(self):
        self.validate = IsValidDatabaseConnectionSection.load(self.DATA)

    def test_green(self):
        self.assertTrue(self.validate('db.green'))

    def test_brown(self):
        self.assertTrue(self.validate('db.brown'))

    def test_red(self):
        with self.assertRaises(KeyError):
            self.validate('db.red')

    def test_orange_one(self):
        with self.assertRaises(KeyError):
            self.validate('db.orange')

    def test_orange_two(self):
        validate = IsValidDatabaseConnectionSection.load(self.DATA,
                                                also_validate_schema=False)
        self.assertTrue(validate('db.orange'))
