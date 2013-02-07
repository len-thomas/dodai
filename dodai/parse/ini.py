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

from dodai.util import find
import configparser
import os

class ParseIni(object):
    """Callable object used to load and parse config ini files
    """
    def __init__(self, project_name):
        """
        :param project_name: The name of the project
        """
        self.project_name = project_name

    def __call__(self, config_files=None, dictionary=None):
        """Grabs and returns a dictionary-like object of the data that was
        parsed from all of the config files.

        :param config_files: A list of complete file paths that will added to the
            list of config files that exist on the system. The file path can
            also be a tuple (filename, encoding).  If the encoding is not
            given the default system encoding will be used.

        :param dictionary: A dictionary of default values added to the
            output dictionary.  This input dictionary must look like:
            data[section_name][key] = val
        """
        config_files = self._config_files(config_files)
        parser = configparser.ConfigParser()
        self._load_config_files(parser, config_files)
        if dictionary:
            parser.read_dict(dictionary)
        return parser

    def _load_config_files(self, parser, config_files):
        for file_ in config_files:
            with open(file_.name, 'r', encoding=file_.encoding) as f:
                parser.read_file(f, file_.name)

    def _config_files(self, config_files):
        if config_files:
            return find.config_files(self.project_name, config_files)
        else:
            return find.config_files(self.project_name)
