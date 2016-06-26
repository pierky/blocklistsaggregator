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


class LinesFormatter(Formatter):

    ID = "lines"

    def __init__(self, args):
        self.line_format = args.lines_format
        self.show_macros = args.lines_show_macros

    @staticmethod
    def add_args(parser):
        group = parser.add_argument_group(
            title="Lines output options"
        )

        group.add_argument(
            "--lines-format",
            help="Output line format: can contain a list of macros that "
                 "are expanded with block list entries' properties. The "
                 "list of these macros can be viewed using the "
                 "--lines-show-macros option. Default: '{prefix}'.",
            default="{prefix}",
            metavar="LINE_FORMAT"
        )

        group.add_argument(
            "--lines-show-macros",
            help="Do not process block lists but only display all the "
                 "macros that can be used to form the output lines.",
            action="store_true"
        )

    def init(self):
        if self.show_macros:
            print("""
    {prefix}      IPv4 or IPv6 prefix, in CIDR format.
                  Ex.: 192.0.2.0/24, 2001:db8::/32

    {ip}          IPv4 or IPv6 address.
                  Ex.: 192.0.2.1, 2001:db8::1

    {network}     IPv4 or IPv6 network ID.
                  Ex.: 192.0.2.0, 2001:db8::

    {netmask}     IPv4 or IPv6 netmask.
                  Ex.: 255.255.255.0, ffff:ffff::

    {prefixlen}   IPv4 or IPv6 CIDR prefix length.
                  Ex.: 32, 24, 128, 64

    {hostmask}    IPv4 or IPv6 hostmask (wildcard).
                  Ex.: 0.0.0.255, ::ffff:ffff:ffff:ffff:ffff:ffff

    {broadcast}   IPv4 or IPv6 broadcast address.
                  Ex.: 192.0.2.255, 2001:db8:ffff:ffff:ffff:ffff:ffff:ffff

    {version}     IP version, 4 or 6.

    {ip_ipv6}     'ip' string in case of an IPv6 entry, 'ipv6' otherwise.

    {bl_ids}      List of blocklist IDs where the prefix has been found.

    {bl_names}    List of blocklist names where the prefix has been found.
    """)
            return False

        return True

    def emit(self, entries, output):
        tpl = self.line_format + "\n"
        try:
            for v4v6 in (4, 6):
                for entry in entries["v{}".format(v4v6)]:
                    bl_ids = entries["unique"][str(entry)]["bl_ids"]

                    output.write(tpl.format(
                        prefix=str(entry),
                        ip=str(entry.ip),
                        network=str(entry.network),
                        netmask=str(entry.netmask),
                        prefixlen=str(entry.prefixlen),
                        hostmask=str(entry.hostmask),
                        broadcast=str(entry.broadcast),
                        version=str(entry.version),
                        ip_ipv6="ip" if entry.version == 4 else "ipv6",
                        bl_ids=", ".join(bl_ids),
                        bl_names=", ".join(get_bl_names(bl_ids))
                    ))
        except KeyError as e:
            raise ValueError("Unknown macro: {}".format(str(e)))
