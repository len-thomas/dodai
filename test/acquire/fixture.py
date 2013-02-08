# Copyright (C) 2013 Leonard Thomas
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

from collections import namedtuple


SECTIONS_01 = {
    'default': {
        'port': 123,
        'env': 'prod',
    },
    'info': {
        'port': 123
    }
}

SECTIONS_02 = {
    'default': {
        'port': 123,
        'environment': 'prod',
    },
    'info': {
        'port': 123
    }
}

SECTIONS_03 = {
    'default': {
        'port': 123,
        'environment': '\u5148\u751f',
    },
    'info': {
        'port': 123
    }
}

