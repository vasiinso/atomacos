# Copyright (c) 2010 VMware, Inc. All Rights Reserved.

# This file is part of ATOMac.

# ATOMac is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation version 2 and no later version.

# ATOMac is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License version 2
# for more details.

# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# St, Fifth Floor, Boston, MA 02110-1301 USA.
import fnmatch


def match_filter(**kwargs):
    def _match(obj):
        for k in kwargs.keys():
            try:
                val = getattr(obj, k)
            except AttributeError:
                return False
            if isinstance(val, str):
                if not fnmatch.fnmatch(val, kwargs[k]):
                    return False
            else:
                if val != kwargs[k]:
                    return False
        return True

    return _match
