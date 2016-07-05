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


class Spamhaus_List(BlockList):
    COMMENT = ";"

    def parse_entry(self, entry):
        ip = IPNetwork(entry.split(" ")[0])
        self.entries.append(ip)


class Spamhaus_DROP_List(Spamhaus_List):
    ID = "drop"
    URL = "https://www.spamhaus.org/drop/drop.lasso"
    NAME = "Spamhaus DROP"


class Spamhaus_DROPv6_List(Spamhaus_List):
    ID = "drop_v6"
    URL = "https://www.spamhaus.org/drop/dropv6.txt"
    NAME = "Spamhaus DROPv6"


class Spamhaus_EDROP_List(Spamhaus_List):
    ID = "edrop"
    URL = "https://www.spamhaus.org/drop/edrop.lasso"
    NAME = "Spamhaus EDROP"
