# Copyright (C) 2016 Pier Carlo Chiodi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

from .base_formatter import Formatter


class JSONFormatter(Formatter):

    ID = "json"

    def _get_entries(self, entries, ip_ver):
        res = {}
        for e in entries[ip_ver]:
            s = str(e)
            res[s] = {"bl_ids": list(entries["unique"][s]["bl_ids"])}
        return res

    def emit(self, entries, output):
        results = {
            "v4": self._get_entries(entries, "v4"),
            "v6": self._get_entries(entries, "v6")
        }
        json.dump(results, output)
