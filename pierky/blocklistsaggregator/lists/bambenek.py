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

from .base_list import BlockList

from netaddr import IPNetwork


class Bambenek_C2_List(BlockList):
    ID = "bambenek_c2"
    URL = "http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt"
    NAME = "Bambenek Consulting C2 master feed"

    def parse_entry(self, entry):
        ip = IPNetwork(entry.split(",")[0])
        self.entries.append(ip)
