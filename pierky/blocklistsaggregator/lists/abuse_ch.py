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

import os
import socket
import sys
try:
    # For Python 3.0 and later
    from urllib.parse import urlparse
except ImportError:
    # Fall back to Python 2's urllib2
    from urlparse import urlparse

from netaddr import IPNetwork

from .base_list import BlockList
from ..sanitisers import sanitise


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


class RW_List(BlockList):

    def __init__(self):
        BlockList.__init__(self)

        self._expected_entries = None

    @property
    def expected_entries(self):
        if self._expected_entries:
            return self._expected_entries

        self._expected_entries = self._get_entries_summary()
        return self._expected_entries

    def _get_entries_summary(self):
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
                cnt = int(cnt)

                # It seems that RW_IPBL is having some issues with the
                # number of entries reported in the last line.
                # If an empty line is found it's counted as an entry, so
                # last line's counter reports a wrong number.
                # Trying to mitigate this behaviour.

                # raw data format                              block_idx
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
                    cnt = cnt - 1

                return cnt

        raise ValueError("Can't find entries summary")

    def _get_parsed_entries_cnt(self):
        return len(self.entries)

    def _verify(self):
        parsed_entries_cnt = self._get_parsed_entries_cnt()

        if self.expected_entries != parsed_entries_cnt:
            raise ValueError(
                "The number of parsed entries ({}) does not "
                "match the expected one ({})".format(
                    parsed_entries_cnt,
                    self.expected_entries
                )
            )


class RW_IPBL_List(RW_List):
    ID = "rw_ipbl"
    URL = "https://ransomwaretracker.abuse.ch/downloads/RW_IPBL.txt"
    NAME = "Ransomware tracker RW_IPBL"


class RW_DomBL_List(RW_List):
    ID = "rw_dombl"
    URL = "https://ransomwaretracker.abuse.ch/downloads/RW_DOMBL.txt"
    NAME = "Ransomware tracker RW_DOMBL"
    USE_BY_DEFAULT = False

    def __init__(self):
        RW_List.__init__(self)
        self.parsed_entries = 0
        self.processed_entries = 0
        self.resolved_domainnames = []

    def _get_parsed_entries_cnt(self):
        return self.parsed_entries

    def _resolve_domainname(self, domainname):
        if domainname in self.resolved_domainnames:
            return

        self.resolved_domainnames.append(domainname)

        try:
            for info in socket.getaddrinfo(
                domainname,
                None, 0, socket.IPPROTO_TCP
            ):
                resolved_addr = info[4][0]

                try:
                    ip = IPNetwork(resolved_addr)
                    self.entries.append(ip)
                except:
                    raise ValueError(
                        "Resolved IP address is invalid: {}".format(
                            resolved_addr
                        )
                    )

        except socket.gaierror:
            pass

        except Exception as e:
            raise ValueError(
                "Can't resolve {} - {}".format(domainname, str(e))
            )

    def _provide_processing_entry_feedback(self, entry):
        self.processed_entries += 1
        if os.isatty(sys.stdout.fileno()):
            if self.processed_entries > 1:
                sys.stdout.write("\033[F")
            sys.stdout.write("\r\033[KProcessing entry {}/{} ({})...\n".format(
                self.processed_entries,
                self.expected_entries,
                sanitise(entry)
            ))

    def parse_entry(self, entry):
        self._provide_processing_entry_feedback(entry)
        self._resolve_domainname(entry)
        self.parsed_entries += 1


class RW_URLBL_List(RW_DomBL_List):
    ID = "rw_urlbl"
    URL = "https://ransomwaretracker.abuse.ch/downloads/RW_URLBL.txt"
    NAME = "Ransomware tracker RW_URLBL"
    USE_BY_DEFAULT = False

    def parse_entry(self, entry):
        self._provide_processing_entry_feedback(entry)

        try:
            url_parts = urlparse(entry)

            if not url_parts.netloc:
                raise ValueError("Can't extract netloc from URL {}".format(
                    entry
                ))

            if ":" in url_parts.netloc:
                domainname = url_parts.split(":")[0]
            else:
                domainname = url_parts.netloc

            self._resolve_domainname(domainname)
            self.parsed_entries += 1

        except Exception as e:
            raise ValueError("Can't parse URL {} - {}".format(entry, str(e)))


class Palevo_CC_List(BlockList):
    ID = "palevo"
    URL = "https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist"
    NAME = "Palevo C&C"


class Zeus_IP_List(BlockList):
    ID = "zeus"
    URL = "https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist"
    NAME = "Zeus IP"
