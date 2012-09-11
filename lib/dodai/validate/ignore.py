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


class ShouldIgnore(object):
    """Callable object used to determin if the section should be ignored
    """

    KEY = 'ignore'
    TRUE = ('true', 'yes')
    MSG = "The config section '{section_name}' has been ignored"

    def __init__(self, sections, log=None, ignore_key=None):
        self._sections = sections
        self._log = log
        self._ignore_key = ignore_key or self.KEY

    def __call__(self, section_name):
        if self._ignore_key in self._sections[section_name]:
            val = self._sections[section_name].get(self._ignore_key)
            if val.lower() in self.TRUE:
                if self._log:
                    msg = self.MSG.format(section_name=section_name)
                    self._log.debug(msg)
                return True
        return False

