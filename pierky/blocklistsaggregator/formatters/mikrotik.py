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

from .base_formatter import Formatter
from ..lists import get_bl_names


class MikrotikFormatter(Formatter):

    ID = "mikrotik"

    def __init__(self, args):
        self.address_list_name = args.mikrotik_address_list_name
        self.remove_before_adding = args.mikrotik_remove_before_adding

    @staticmethod
    def add_args(parser):
        group = parser.add_argument_group(
            title="Mikrotik RouterOS output options"
        )

        group.add_argument(
            "--mikrotik-address-list-name",
            help="Address list name. Default: 'block_list'.",
            default="block_list"
        )

        group.add_argument(
            "--mikrotik-remove-before-adding",
            help="Add a 'remove' statement before the 'add'. "
                 "Default: False.",
            action="store_true",
            default=False
        )

    def emit(self, entries, output):
        for v4v6 in (4, 6):
            output.write("/{} firewall address-list\n".format(
                "ip" if v4v6 == 4 else "ipv6"
            ))

            if self.remove_before_adding:
                output.write("remove [find list=""{}""]\n".format(
                    self.address_list_name
                ))
            for entry in entries["v{}".format(v4v6)]:
                output.write(
                    """add list={} address="{}" comment="{}"\n""".format(
                        self.address_list_name, str(entry),
                        ", ".join(
                            get_bl_names(
                                entries["unique"][str(entry)]["bl_ids"]
                            )
                        )
                    )
                )
