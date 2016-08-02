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

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

from netaddr import IPNetwork

from ..errors import BlockListProcessingError


class BlockList(object):
    ID = None
    URL = None
    NAME = None
    COMMENT = "#"
    USE_BY_DEFAULT = True

    def __init__(self):
        self.raw_data = None
        self.raw_entries = []
        self.entries = []

    def load(self):
        try:
            self.fetch()
        except Exception as e:
            raise BlockListProcessingError(
                "Error while fetching the blocklist's data - {}".format(
                    str(e)
                )
            )

        try:
            self.parse()
        except Exception as e:
            raise BlockListProcessingError(
                "Error while processing the blocklist's data - {}".format(
                    str(e)
                )
            )

        try:
            self.verify()
        except Exception as e:
            raise BlockListProcessingError(
                "Error while verifying the blocklist's data - {}".format(
                    str(e)
                )
            )

    def fetch(self):
        if not self.URL:
            raise NotImplementedError()
        response = urlopen(self.URL)
        self.raw_data = response.read().decode("utf-8")
        self.raw_entries = self.raw_data.split("\n")

    def parse(self):
        for entry in self.raw_entries:
            entry = entry.strip()
            if not entry or entry[0] == self.COMMENT:
                continue
            self.parse_entry(entry)

    def parse_entry(self, entry):
        try:
            ip = IPNetwork(entry)
        except:
            raise ValueError("Incorrect IP address/net: {}".format(entry))
        self.entries.append(ip)

    def _verify(self):
        pass

    def verify(self):
        try:
            if not self.raw_data:
                raise ValueError("No data")

            if len([_ for _ in self.raw_entries if _]) == 0:
                raise ValueError("Empty list of raw entries")

            self._verify()

        except Exception as e:
            raise ValueError(
                "Can't determine the expected num. of entries - {}.".format(
                    str(e)
                )
            )

    def load_from_file(self, path):
        with open(path, "r") as f:
            lines = f.readlines()
        for line in lines:
            if not line:
                continue
            self.entries.append(IPNetwork(line))

    def save_to_file(self, path):
        with open(path, "w") as f:
            for entry in self.entries:
                f.write("{}\n".format(str(entry)))
