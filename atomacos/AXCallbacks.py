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


def elemDisappearedCallback(retelem, obj, **kwargs):
    """Callback for checking if a UI element is no longer onscreen.

    kwargs should contains some unique set of identifier (e.g. title/value, role)
    Returns:  Boolean
    """
    return not obj.findFirstR(**kwargs)


def returnElemCallback(retelem):
    """Callback for when a sheet appears.

    Returns: element returned by observer callback
    """
    return retelem


def match(obj, **kwargs):
    """Method which indicates if the object matches specified criteria.

    Match accepts criteria as kwargs and looks them up on attributes.
    Actual matching is performed with fnmatch, so shell-like wildcards
    work within match strings. Examples:

    match(obj, AXTitle='Terminal*')
    match(obj, AXRole='TextField', AXRoleDescription='search text field')
    """
    for k in kwargs.keys():
        try:
            val = getattr(obj, k)
        except AttributeError:
            return False
        # Not all values may be strings (e.g. size, position)
        if isinstance(val, str):
            if not fnmatch.fnmatch(val, kwargs[k]):
                return False
        else:
            if val != kwargs[k]:
                return False
    return True
