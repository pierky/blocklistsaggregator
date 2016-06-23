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


class Feodo_List(BlockList):

    def _verify(self):
        last_entry = self.raw_entries[-1]
        if last_entry.startswith("# END"):
            cnt = last_entry.split("(")[1].split(" ")[0]

            if not cnt.isdigit():
                raise ValueError(
                    "Can't parse entries summary: {}".format(last_entry)
                )

            if int(cnt) != len(self.entries):
                raise ValueError(
                    "The number of parsed entries ({}) does not "
                    "match the expected one ({})".format(
                        len(self.entries),
                        int(cnt)
                    )
                )
            else:
                return

        raise ValueError("Can't find entries summary")


class Feodo_BadIP_List(Feodo_List):
    ID = "feodo_badip"
    URL = "https://feodotracker.abuse.ch/blocklist/?download=badips"
    NAME = "Feodo BadIP"


class Feodo_IP_List(Feodo_List):
    ID = "feodo_ip"
    URL = "https://feodotracker.abuse.ch/blocklist/?download=ipblocklist"
    NAME = "Feodo IP"


class RW_IPBL_List(BlockList):
    ID = "rw_ipbl"
    URL = "https://ransomwaretracker.abuse.ch/downloads/RW_IPBL.txt"
    NAME = "Ransomware tracker RW_IPBL"

    def _verify(self):
        last_entry = self.raw_entries[-1]
        if last_entry[0] == self.COMMENT:
            if "entries" in last_entry:
                cnt = last_entry.split(" ")[1]
                if not cnt.isdigit():
                    raise ValueError(
                        "Can't parse entries summary: {}".format(
                            last_entry
                        )
                    )

                if int(cnt) != len(self.entries):
                    raise ValueError(
                        "The number of parsed entries ({}) does not "
                        "match the expected one ({})".format(
                            len(self.entries),
                            int(cnt)
                        )
                    )
                else:
                    return

        raise ValueError("Can't find entries summary")


class Palevo_CC_List(BlockList):
    ID = "palevo"
    URL = "https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist"
    NAME = "Palevo C&C"


class Zeus_IP_List(BlockList):
    ID = "zeus"
    URL = "https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist"
    NAME = "Zeus IP"
