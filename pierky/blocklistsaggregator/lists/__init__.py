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

from .spamhaus import Spamhaus_DROP_List, Spamhaus_DROPv6_List, \
                      Spamhaus_EDROP_List
from .abuse_ch import Feodo_BadIP_List, Feodo_IP_List, Palevo_CC_List, \
                      Zeus_IP_List, RW_IPBL_List, RW_DomBL_List, RW_URLBL_List
from .bambenek import Bambenek_C2_List

BlockLists = [RW_IPBL_List, RW_DomBL_List, RW_URLBL_List,
              Spamhaus_DROP_List, Spamhaus_DROPv6_List, Spamhaus_EDROP_List,
              Feodo_BadIP_List, Feodo_IP_List, Palevo_CC_List, Zeus_IP_List,
              Bambenek_C2_List]


def get_bl_from_id(id):
    return [bl_class for bl_class in BlockLists if bl_class.ID == id][0]


def get_bl_names(bl_ids):
    ret = []
    for bl_class in BlockLists:
        if bl_class.ID in bl_ids:
            ret.append(bl_class.NAME)
    return ret
