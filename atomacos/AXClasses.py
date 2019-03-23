# Copyright (c) 2010-2011 VMware, Inc. All Rights Reserved.

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

import time
from collections import deque

from atomacos import a11y
from atomacos.mixin import KeyboardMouseMixin, SearchMethodsMixin, WaitForMixin


class NativeUIElement(
    KeyboardMouseMixin, WaitForMixin, SearchMethodsMixin, a11y.AXUIElement
):
    """NativeUIElement class - expose the accessibility API in the simplest,
    most natural way possible.
    """

    def __init__(self, ref=None):
        super(NativeUIElement, self).__init__(ref=ref)
        self.eventList = deque()

    @classmethod
    def getRunningApps(cls):
        """Get a list of the running applications."""
        return a11y.get_running_apps()

    @classmethod
    def getAppRefByPid(cls, pid):
        """Get the top level element for the application specified by pid."""
        return cls.from_pid(pid)

    @classmethod
    def getAppRefByBundleId(cls, bundleId):
        """
        Get the top level element for the application with the specified
        bundle ID, such as com.vmware.fusion.
        """
        return cls.from_bundle_id(bundleId)

    @classmethod
    def getAppRefByLocalizedName(cls, name):
        """Get the top level element for the application with the specified
        localized name, such as VMware Fusion.

        Wildcards are also allowed.
        """
        # Refresh the runningApplications list
        return cls.from_localized_name(name)

    @classmethod
    def getFrontmostApp(cls):
        """Get the current frontmost application.

        Raise a ValueError exception if no GUI applications are found.
        """
        # Refresh the runningApplications list
        return cls.frontmost()

    @classmethod
    def getAnyAppWithWindow(cls):
        """Get a random app that has windows.

        Raise a ValueError exception if no GUI applications are found.
        """
        # Refresh the runningApplications list
        return cls.with_window()

    @classmethod
    def getSystemObject(cls):
        """Get the top level system accessibility object."""
        return cls.systemwide()

    @classmethod
    def setSystemWideTimeout(cls, timeout=0.0):
        """Set the system-wide accessibility timeout.

        Args:
            timeout: non-negative float. 0 will reset to the system default.

        Returns:
            None

        """
        return cls.set_systemwide_timeout(timeout)

    @staticmethod
    def launchAppByBundleId(bundleID):
        """Launch the application with the specified bundle ID"""
        # NSWorkspaceLaunchAllowingClassicStartup does nothing on any
        # modern system that doesn't have the classic environment installed.
        # Encountered a bug when passing 0 for no options on 10.6 PyObjC.
        a11y.launch_app_by_bundle_id(bundleID)

    @staticmethod
    def launchAppByBundlePath(bundlePath, arguments=None):
        """Launch app with a given bundle path.

        Return True if succeed.
        """
        return a11y.launch_app_by_bundle_path(bundlePath, arguments)

    @staticmethod
    def terminateAppByBundleId(bundleID):
        """Terminate app with a given bundle ID.
        Requires 10.6.

        Return True if succeed.
        """
        return a11y.terminate_app_by_bundle_id(bundleID)

    @classmethod
    def set_systemwide_timeout(cls, timeout=0.0):
        """Set the system-wide accessibility timeout.

        Args:
            timeout: A value of 0 will reset the timeout to the system default.
        """
        return cls.systemwide().setTimeout(timeout)

    def setTimeout(self, timeout=0.0):
        """Set the accessibiltiy API timeout on the given reference.

        Args:
            timeout: A value of 0 will reset the timeout to the systemwide value
        """
        self.set_timeout(timeout)

    def getAttributes(self):
        """Get a list of the attributes available on the element."""
        return self.ax_attributes

    def getActions(self):
        """Return a list of the actions available on the element."""
        actions = self.ax_actions
        # strip leading AX from actions - help distinguish them from attributes
        return [action[2:] for action in actions]

    def setString(self, attribute, string):
        """Set the specified attribute to the specified string."""
        return self.__setattr__(attribute, str(string))

    def getElementAtPosition(self, coord):
        """Return the AXUIElement at the given coordinates.

        If self is behind other windows, this function will return self.
        """
        return self._getElementAtPosition(float(coord[0]), float(coord[1]))

    def activate(self):
        """Activate the application (bringing menus and windows forward)"""
        return self._activate()

    def getApplication(self):
        """Get the base application UIElement.

        If the UIElement is a child of the application, it will try
        to get the AXParent until it reaches the top application level
        element.
        """
        app = self
        while "AXParent" in app.ax_attributes:
            app = app.AXParent
        return app

    def menuItem(self, *args):
        """Return the specified menu item.

        Example - refer to items by name:

        app.menuItem('File', 'New').Press()
        app.menuItem('Edit', 'Insert', 'Line Break').Press()

        Refer to items by index:

        app.menuitem(1, 0).Press()

        Refer to items by mix-n-match:

        app.menuitem(1, 'About TextEdit').Press()
        """
        menuitem = self.getApplication().AXMenuBar
        return self._menuItem(menuitem, *args)

    def popUpItem(self, *args):
        """Return the specified item in a pop up menu."""
        self.Press()
        time.sleep(0.5)
        return self._menuItem(self, *args)

    def getBundleId(self):
        """Return the bundle ID of the application."""
        return self.bundle_id

    def getLocalizedName(self):
        """Return the localized name of the application."""
        return self.getApplication().AXTitle

    def __getattr__(self, name):
        """Handle attribute requests in several ways:

        1. If it starts with AX, it is probably an a11y attribute. Pass
           it to the handler in _a11y which will determine that for sure.
        2. See if the attribute is an action which can be invoked on the
           UIElement. If so, return a function that will invoke the attribute.
        """
        if "AX" + name in self.ax_actions:
            action = super(NativeUIElement, self).__getattr__("AX" + name)

            def performSpecifiedAction():
                # activate the app before performing the specified action
                self._activate()
                return action()

            return performSpecifiedAction
        else:
            return super(NativeUIElement, self).__getattr__(name)
