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


class AcquireEnvironment(object):
    """Callable used to figure out the enviornment (eg.. prod, stage,
    dev etc..).
    """

    ENVIRONMENT_SEARCH_SECTIONS = ('server', 'basic', 'default', 'system',
                                   'main', 'config')
    ENVIRONMENT_FIELD_NAMES = ('environment', 'env',)
    ENVIRONMENT_DEFAULT = 'dev'

    def __init__(self, sections, log=None, value=None, section_name=None,
                 field_name=None, default_value=None):
        self._sections = sections
        self._section_name = section_name
        self._field_name = field_name
        self._default_value = default_value or self.ENVIRONMENT_DEFAULT
        self._out_ = None


    @classmethod
    def load(cls, sections, log=None, value=None, section_name=None,
             field_name=None, default_value=None):
        """Tees up this object; will figure out what the environment
        is set to.
         :param sections:  The config dictionary
         :param log:  The logger
         :param value:  Override of the value
         :param section:  The section that holds env variable
         :param field_name:  The key in the section that holds the env var
         :param default_value: The value used if there is no key
        """
        return cls(sections, log, value, section_name, field_name,
                   default_value)

    def _find(self, section_name, field_name):

        if section_name in self._sections:
            if field_name in self._sections[section_name]:
                return self._sections[section_name][field_name]
        return None

    def __call__(self, section_name=None, field_name=None,
                 default_value=None):
        section_name = section_name or self._section_name
        field_name = field_name or self._field_name
        default_value = default_value or self._default_value
        out = None

        if section_name:
            section_names = (section_name,)
        else:
            section_names = self.ENVIRONMENT_SEARCH_SECTIONS

        if field_name:
            field_names = (field_name,)
        else:
            field_names = self.ENVIRONMENT_FIELD_NAMES

        for section_name in section_names:
            for field_name in field_names:
                out = self._find(section_name, field_name)
                if out:
                    return out

        return default_value

