#
#    Copyright 2012 Leonard Thomas, Mike Crute
#
#    This file is part of Dodai.
#
#    Dodai is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Dodai is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Dodai.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from setuptools import setup
from setuptools import find_packages
from subprocess import Popen
from subprocess import PIPE
from collections import OrderedDict


try:
    # This is probably Linux
    from ctypes.util import _findLib_ldconfig as find_library
except ImportError:
    # This is something else (maybe Mac OS X?)
    from ctypes.util import find_library

VERSION = "0.5.0"
DESCRIPTION = """
    A Python 3+ module used by developers to have quick easy access to
    parsed-text-based configuration files.
"""
LONG_DESCRIPTION = """
    A Python 3+ module that is designed to be used by devlopers as part of a
    configuration step in an application.  This module looks for all possible
    related configuration files on the system and parses them.  This parsed
    configuration data can also be used by this module to quickly spin up
    SQLAlchemy objects for use in an application.
"""
META = dict(
    name='dodai',
    version=VERSION,
    author='\x4c\x65\x6f\x6e\x61\x72\x64\x20\x54\x68\x6f\x6d\x61\x73',
    author_email='\x31\x39\x37\x30\x69\x6e\x61\x7a\x75\x6d\x61\x40\x67\x6d'\
                 '\x61\x69\x6c\x2e\x63\x6f\x6d',
    url='http://code.google.com/p/dodai/downloads/list',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS 9',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: PL/SQL',
        'Programming Language :: PROGRESS',
        'Programming Language :: SQL',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION
)


class _BaseLibCheck(object):
    """Base class that provides several methods for use in determining if
    the computer system has the required libraries installed in order to
    continue setting up the python module
    """

    def _has_library(self, lib):
        """Returns True if the given lib name exists on this computer
        """
        # Uses the ctypes find_library
        if find_library(lib):
            return True
        else:
            return False

    def _which(self, name):
        cmd = ['which', name]
        return Popen(cmd, stdout=PIPE).communicate()[0]


    def _should_be_processed(self, name):
        """Returns True if the given name should be processed by this
        object.
        """
        if name.strip().lower().startswith(self.PACKAGE.lower()):
            return True
        else:
            return False


class CanInstallPsycopg2(_BaseLibCheck):
    """Callable object used to determine if the psycopg2 python module
    can be installed.  psycopg2 is used by SQLAlchemy to connect to
    PostgreSQL databases.
    """
    PACKAGE = 'psycopg2'
    LIB = 'pq'

    def __call__(self, package):
        if self._should_be_processed(package):
            if self._has_library(self.LIB):
                return True
            return False


class CanInstallMysqlPython(_BaseLibCheck):
    """Callable object used to determine if the mysql-python module can
    be installed.  mysql-python is used by SQLAlchemy to connect to MySQL
    databases.
    """
    PACKAGE = 'mysql-python'
    LIB = 'mysqlpp'

    def __call__(self, package):
        if self._should_be_processed(package):
            # Seems that mysql-python doesn't work in python 3 yet
            if sys.version < '3.0':
                if self._has_library(self.LIB):
                    if self._which('mysql_config'):
                        return True
            return False


class CanInstallCxOracle(_BaseLibCheck):
    """Callable object used to determine if the cx_oracle python module can
    be installed.  cx_oracle is used by SQLAlchemy to connect to Oracle
    databases.
    """
    PACKAGE = 'cx_oracle'
    LIB = 'clntsh'

    def __call__(self, package):
        if self._should_be_processed(package):
            if 'ORACLE_HOME' in os.environ:
                if os.environ['ORACLE_HOME']:
                    return True
            else:
                if self._has_library(self.LIB):
                    self._set_oracle_home()
                    return True
            return False

    def _set_oracle_home(self):
        path = find_library(self.LIB)
        os.environ['ORACLE_HOME'] = os.path.dirname(path)


def install_requires(*packages):
    """Checks the given pacakges to see if the required libs are installed
    locally.  If they are not then the package is removed from the list.
    """
    out = []
    hold = OrderedDict()
    can_install_chain = [
        CanInstallPsycopg2(),
        CanInstallMysqlPython(),
        CanInstallCxOracle()
    ]

    for package in packages:
        for can_install in can_install_chain:
            current = hold.get(package)
            if current not in (True, False):
                hold[package] = can_install(package)

    for key in hold.keys():
        if hold[key] is not False:
            out.append(key)
    return out

ARGS = dict(
    zip_safe=False,
    package_dir={'':'lib'},
    packages=['dodai'],
    platforms=['Linux', 'Darwin'],
    test_suite='dodai.test.run',
    install_requires=install_requires('psycopg2', 'mysql-python', 'cx_oracle',
                                      'SQLALchemy'),
    **META
)

if __name__ == '__main__':

    if sys.version < '3.2':
        message = "{package} is not able to install:  The version of python "\
                  "that is being used, '{version}', is not compatable with "\
                  "{package}.  {package} will only install with Python "\
                  "version {package_version} or greater"
        message = message.format(package=ARGS['name'], version=sys.version,
                                 package_version='2.6')
        sys.stderr.write(message)
        sys.exit(1)

    setup(**ARGS)
