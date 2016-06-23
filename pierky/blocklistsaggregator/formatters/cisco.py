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


class CiscoFormatter(Formatter):

    ID = "cisco-ios"

    def __init__(self, args):
        self.cfg_element = args.cisco_cfg_element
        self.cfg_element_name = args.cisco_cfg_element_name
        self.cfg_element_action = args.cisco_cfg_element_action
        self.remove_before_adding = args.cisco_remove_before_adding

    @staticmethod
    def add_args(parser):
        group = parser.add_argument_group(
            title="Cisco IOS output options"
        )

        group.add_argument(
            "--cisco-cfg-element",
            help="Type of configuration element to build. "
                 "Default: 'prefix-list'.",
            choices=["prefix-list", "acl_source", "acl_dest"],
            default="prefix-list"
        )

        group.add_argument(
            "--cisco-cfg-element-name",
            help="Name of the configuration element to build. "
                 "Default: 'block_list'.",
            default="block_list"
        )

        group.add_argument(
            "--cisco-cfg-element-action",
            help="Action of the prefix-list/ACL. Default: 'permit'.",
            choices=["permit", "deny"],
            default="deny"
        )

        group.add_argument(
            "--cisco-remove-before-adding",
            help="Add a 'no <cfg_element_name>' statement before the "
                 "statements that build the new configuration block. "
                 "Default: False.",
            action="store_true",
            default=False
        )

    def _emit_prefix_list(self, entries, output, v4v6):
        ip_or_ipv6 = "ip" if v4v6 == 4 else "ipv6"

        if self.remove_before_adding:
            output.write("no {} prefix-list {}\n".format(
                ip_or_ipv6, self.cfg_element_name
            ))

        for entry in entries["v{}".format(v4v6)]:
            output.write("{} prefix-list {} {} {}\n".format(
                ip_or_ipv6,
                self.cfg_element_name,
                self.cfg_element_action,
                str(entry)
            ))

    def _emit_acl(self, entries, output, v4v6, src_or_dst):
        tpl_remove = ""
        tpl_create = ""
        tpl_ace = ""
        tpl_last_ace = ""

        if v4v6 == 4 and src_or_dst == "src":
            tpl_remove = "no ip access-list standard {name}\n"
            tpl_create = "ip access-list standard {name}\n"
            tpl_ace = "{action} {host_addr_or_net_wildcard}\n"
            if self.cfg_element_action == "deny":
                tpl_last_ace = "permit any\n"
        elif v4v6 == 4 and src_or_dst == "dst":
            tpl_remove = "no ip access-list extended {name}\n"
            tpl_create = "ip access-list extended {name}\n"
            tpl_ace = "{action} ip any {host_addr_or_net_wildcard}\n"
            if self.cfg_element_action == "deny":
                tpl_last_ace = "permit ip any any\n"
        elif v4v6 == 6:
            tpl_remove = "no ipv6 access-list {name}\n"
            tpl_create = "ipv6 access-list {name}\n"
            if src_or_dst == "src":
                tpl_ace = "{action} {prefix} any\n"
            else:
                tpl_ace = "{action} any {prefix}\n"
            if self.cfg_element_action == "deny":
                tpl_last_ace = "permit any any\n"

        if self.remove_before_adding:
            output.write(tpl_remove.format(name=self.cfg_element_name))

        output.write(tpl_create.format(name=self.cfg_element_name))

        for entry in entries["v{}".format(v4v6)]:
            host_addr_or_net_wildcard = ""
            if entry.version == 4:
                if entry.prefixlen == 32:
                    host_addr_or_net_wildcard = "host {}".format(str(entry.ip))
                else:
                    host_addr_or_net_wildcard = "{} {}".format(
                        str(entry.ip), str(entry.hostmask)
                    )

            output.write(tpl_ace.format(
                action=self.cfg_element_action,
                host_addr_or_net_wildcard=host_addr_or_net_wildcard,
                prefix=str(entry)
            ))

        output.write(tpl_last_ace)

    def emit(self, entries, output):
        for v4v6 in (4, 6):
            if self.cfg_element == "prefix-list":
                self._emit_prefix_list(entries, output, v4v6)
            elif self.cfg_element == "acl_source":
                self._emit_acl(entries, output, v4v6, "src")
            elif self.cfg_element == "acl_dest":
                self._emit_acl(entries, output, v4v6, "dst")
