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

from dodai.validate.ignore import ShouldIgnore
from dodai.validate.field.base import SectionExists
from dodai.validate.field.dialect import IsValidDialect
from dodai.validate.field.host import IsValidHost
from dodai.validate.field.port import IsValidPort
from dodai.validate.field.username import IsValidUsername
from dodai.validate.field.password import IsValidPassword
from dodai.validate.field.database import IsValidDatabase
from dodai.validate.field.schema import IsValidSchema
from dodai.validate.field.path import IsValidPath


class IsDatabaseConnectionSection(object):

    PREFIX = 'db'

    def __init__(self, sections, prefix, section_exists, should_ignore,
                 is_valid_dialect):
        self._sections = sections
        self._prefix = prefix
        self._section_exists = section_exists
        self._should_ignore = should_ignore
        self._is_valid_dialect = is_valid_dialect

    @classmethod
    def load(cls, sections, log=None, raise_errors=True, prefix=None):

        prefix = prefix or cls.PREFIX
        section_exists = SectionExists(sections, log,
                                       raise_errors=raise_errors)
        should_ignore = ShouldIgnore(sections, log)
        is_validate_dialect = IsValidDialect.load(sections, log,
                                        raise_errors=raise_errors)
        return cls(sections, prefix, section_exists, should_ignore,
                   is_validate_dialect)

    def __call__(self, section_name):
        if self._section_exists(section_name):
            if section_name.startswith(self._prefix):
                if not self._should_ignore(section_name):
                    if self._is_valid_dialect(section_name):
                        return True
        return False


class IsValidDatabaseConnectionSection(object):

    FILE_DATABASES = ('sqlite', 'access',)
    NO_SCHEMA_DIALECT = ('mysql',)

    def __init__(self, sections, dialect_key, is_database_section,
                 is_valid_path, is_valid_host, is_valid_port,
                 is_valid_username, is_valid_password, is_valid_database,
                 is_valid_schema, also_validate_schema):
        self._sections = sections
        self._dialect_key = dialect_key
        self._is_database_section = is_database_section
        self._is_valid_path = is_valid_path
        self._chain = (is_valid_host, is_valid_port, is_valid_username,
                       is_valid_password, is_valid_database)
        self._is_valid_schema = is_valid_schema
        self._also_validate_schema = also_validate_schema

    @classmethod
    def load(cls, sections, log=None, raise_errors=True, prefix=None,
             also_validate_schema=True):

        dialect_key = IsValidDialect.KEY
        is_database_section = IsDatabaseConnectionSection.load(sections, log,
                                                        raise_errors, prefix)
        is_valid_path = IsValidPath.load(sections, log,
                                            raise_errors=raise_errors)
        is_valid_host = IsValidHost.load(sections, log,
                                            raise_errors=raise_errors)
        is_valid_port = IsValidPort.load(sections, log,
                                            raise_errors=raise_errors)
        is_valid_username = IsValidUsername.load(sections, log,
                                            raise_errors=raise_errors)
        is_valid_password = IsValidPassword.load(sections, log,
                                            raise_errors=raise_errors)
        is_valid_database = IsValidDatabase.load(sections, log,
                                            raise_errors=raise_errors)
        is_valid_schema = IsValidSchema.load(sections, log,
                                            raise_errors=raise_errors)
        return cls(sections, dialect_key, is_database_section,
                 is_valid_path, is_valid_host, is_valid_port,
                 is_valid_username, is_valid_password, is_valid_database,
                 is_valid_schema, also_validate_schema)

    def __call__(self, section_name):
        if self._is_database_section(section_name):
            dialect = self._sections[section_name][self._dialect_key]
            if dialect.lower() in self.FILE_DATABASES:
                return self._validate_file_database(section_name)
            else:
                return self._validate_connection_database(section_name,
                                                          dialect)
        return False

    def _validate_file_database(self, section_name):
        return self._is_valid_path(section_name)

    def _validate_connection_database(self, section_name, dialect):
        out = True
        for validate in self._chain:
            result = validate(section_name)
            if result == False:
                out = False

        if out:
            if self._also_validate_schema:
                if dialect not in self.NO_SCHEMA_DIALECT:
                    out = self._is_valid_schema(section_name)
        return out
