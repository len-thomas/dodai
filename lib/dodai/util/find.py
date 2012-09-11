# Copyright (C) 2011 Leonard Thomas
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

import sys
import os
import platform
from collections import namedtuple

def home_direcotry(project_name=None):
    """Return the full real path of this script user's home directory.
    The passed in project name will be appended to the home directory.
    """
    if project_name:
        project_name = project_name.strip()

    # Test for windows
    try:
        from win32com.shell import shellcon, shell
    except ImportError:
        out = os.path.expanduser('~')
    else:
        out = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
    out = os.path.realpath(out)
    if project_name:
        project_name = ".{0}".format(project_name)
        out = os.path.join(out, project_name)
    return os.path.realpath(out)

def system_config_directory(project_name=None):
    """Returns the full real path to the system config directory with the
    passed in project_name appended.  Does not work on windows.
    """
    if project_name:
        project_name = project_name.strip()

    if platform.system() and platform.system() not in ('Windows', 'Java',):
        path = "{0}{1}".format(os.path.sep, 'etc')
        if project_name:
            return os.path.join(path, project_name)
        else:
            return path
    return None

def system_encoding():
    """Returns the system's character encoding
    """

    def _find_the_system_encoding__():
        encoding = sys.getfilesystemencoding()
        if not encoding:
            encoding = sys.getdefaultencoding()
        return encoding

    return _find_the_system_encoding__()

def project_config_directory(with_config=True):
    """Returns the directory of where this executable is running from.  When
    'with_config' is set to True then 'config' will be appended to the
    returned value
    """
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    if with_config:
        return os.path.join(path, 'config')
    else:
        return path

def config_directories(project_name):
    """Returns a list of the possible project config directories
    """
    return [
        project_config_directory(),
        system_config_directory(project_name),
        home_direcotry(project_name)
    ]


class ConfigFiles(object):
    """Callable object used to find config files that will be parsed
    """

    # Tuple of possible names of config files without the file extensions
    FILENAME_ROOTS = ('cfg', 'cfgs', 'config', 'configs', 'configure',
        'connect', 'connection', 'connections', 'database', 'databases', 'db',
        'dbs', 'server', 'servers', 'setup',)

    # Tuple of possible file extensions
    FILENAME_EXTENSIONS = ('cfg', 'txt', 'ini', '',)
    FIELDS = ('name', 'encoding')

    def __init__(self, directories, default_encoding):
        self.directories = directories
        self.default_encoding = default_encoding
        self._make = namedtuple('config_file', self.FIELDS)

    @classmethod
    def load(cls, project_name):
        directories = config_directories(project_name)
        default_encoding = system_encoding()
        return cls(directories, default_encoding)

    def __call__(self, filenames=None):
        """Returns a list of (filename, encoding) of config files that
        actually exist in the filesystem.

        :param filenames: A list of complete file paths that will
            added to the list of config files that exist on the system. The
            file path can also be a tuple (filename, encoding).  If the
            encoding is not given the default system encoding will be used
        """
        out = []
        possible_filenames = self._build_list_of_possible_filenames(filenames)
        for possible_filename in possible_filenames:
            if (os.path.exists(possible_filename.name)
                    and os.path.isfile(possible_filename.name)):
                out.append(possible_filename)
        return out

    def _build_list_of_possible_filenames(self, filenames):
        possible_filenames = []
        if filenames:
            for filename in filenames:
                if isinstance(filename, tuple):
                    if len(filename) > 1:
                        possible_filenames.append(
                                self._make(filename[0], filename[1])
                        )
                    elif len(filename) == 1:
                        possible_filenames.append(
                                self._make(filename[0], self.default_encoding)
                        )
                else:
                    possible_filenames.append(
                            self._make(filename, self.default_encoding)
                    )

        # Build all the possible default paths
        for directory in self.directories:
            for filename in self._build_filenames():
                filename = os.path.join(directory, filename)
                possible_filenames.append(
                        self._make(filename, self.default_encoding)
                )
        return possible_filenames

    def _build_filenames(self):
        out = []
        for root in self.FILENAME_ROOTS:
            for extension in self.FILENAME_EXTENSIONS:
                if extension:
                    filename = "{0}.{1}".format(root, extension)
                    out.append(filename)
                    out.append(".{0}".format(filename))
                else:
                    out.append(root)
                    out.append(".{0}".format(root))
        return out



def config_files(project_name, filenames=None):
    """Returns a list of (filename, encoding) of the config filenames that
    actually exist on the system.  Passed in filenames (list or string) can
    override the defaults
    """
    find_config_files = ConfigFiles.load(project_name)
    return find_config_files(filenames)
