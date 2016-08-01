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
        last_entry = [line for line in self.raw_entries if line][-1]
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
        last_entry = [line for line in self.raw_entries if line][-1]
        if last_entry[0] == self.COMMENT:
            if "entries" in last_entry:
                cnt = last_entry.split(" ")[1]
                if not cnt.isdigit():
                    raise ValueError(
                        "Can't parse entries summary: {}".format(
                            last_entry
                        )
                    )

                # It seems that RW_IPBL is having some issues with the
                # number of entries reported in the last line.
                # If an empty line is found it's counted as an entry, so
                # last line's counter reports a wrong number.
                # Trying to mitigate this behaviour.

                # raw data format / block_idx
                #
                # ############################################ block_idx = 1
                # # comments                                   block_idx = 2
                # ############################################ block_idx = 3
                # entries                                      block_idx = 4
                # # xxx entries                                block_idx = 5

                empty_entry_found = False
                block_idx = 0
                for entry in self.raw_entries:
                    entry = entry.strip()
                    if entry.startswith(self.COMMENT * 10):
                        if block_idx == 0:
                            block_idx = 1
                        elif block_idx == 2:
                            block_idx = 3
                    elif entry.startswith(self.COMMENT):
                        if "entries" not in entry and block_idx == 1:
                            block_idx = 2
                        elif "entries" in entry and block_idx == 4:
                            block_idx = 5
                    elif block_idx == 3:
                        block_idx = 4

                    if not entry and block_idx == 4:
                        empty_entry_found = True
                        break

                if empty_entry_found:
                    cnt = int(cnt) - 1

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
