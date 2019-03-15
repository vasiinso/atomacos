import fnmatch
import time
from collections import deque

import AppKit
import Quartz
from atomacos import AXKeyboard, AXKeyCodeConstants, a11y, errors
from atomacos.notification import Observer


class BaseAXUIElement(a11y.AXUIElement):
    """Base class for UI elements. Implements four major things:

    1. Factory class methods for getAppRef and getSystemObject which
       properly instantiate the class.
    2. Generators and methods for finding objects for use in child classes.
    3. __getattribute__ call for invoking actions.
    4. waitFor utility based upon AX notifications.
    """

    def __init__(self, ref=None):
        super(BaseAXUIElement, self).__init__(ref=ref)
        self.eventList = deque()

    @classmethod
    def _getRunningApps(cls):
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
        a11y.AXUIElement.launch_app_by_bundle_id(bundleID)

    @staticmethod
    def launchAppByBundlePath(bundlePath, arguments=None):
        """Launch app with a given bundle path.

        Return True if succeed.
        """
        return a11y.AXUIElement.launch_app_by_bundle_path(bundlePath, arguments)

    @staticmethod
    def terminateAppByBundleId(bundleID):
        """Terminate app with a given bundle ID.
        Requires 10.6.

        Return True if succeed.
        """
        return a11y.AXUIElement.terminate_app_by_bundle_id(bundleID)

    @classmethod
    def set_systemwide_timeout(cls, timeout=0.0):
        """Set the system-wide accessibility timeout.

        Optional: timeout (non-negative float; defaults to 0)
                  A value of 0 will reset the timeout to the system default.
        Returns: None.
        """
        return cls.systemwide().setTimeout(timeout)

    def setTimeout(self, timeout=0.0):
        """Set the accessibiltiy API timeout on the given reference.

        Optional: timeout (non-negative float; defaults to 0)
                  A value of 0 will reset the timeout to the system-wide
                  value
        Returns: None
        """
        self.set_timeout(timeout)

    def _postQueuedEvents(self, interval=0.01):
        """Private method to post queued events (e.g. Quartz events).

        Each event in queue is a tuple (event call, args to event call).
        """
        while len(self.eventList) > 0:
            (nextEvent, args) = self.eventList.popleft()
            nextEvent(*args)
            time.sleep(interval)

    def _clearEventQueue(self):
        """Clear the event queue."""
        if hasattr(self, "eventList"):
            self.eventList.clear()

    def _queueEvent(self, event, args):
        """Private method to queue events to run.

        Each event in queue is a tuple (event call, args to event call).
        """
        self.eventList.append((event, args))

    def _addKeyToQueue(self, keychr, modFlags=0, globally=False):
        """Add keypress to queue.

        Parameters: key character or constant referring to a non-alpha-numeric
                    key (e.g. RETURN or TAB)
                    modifiers
                    global or app specific
        Returns: None or raise ValueError exception.
        """
        # Awkward, but makes modifier-key-only combinations possible
        # (since sendKeyWithModifiers() calls this)
        if not keychr:
            return

        if not hasattr(self, "keyboard"):
            self.keyboard = AXKeyboard.loadKeyboard()

        if keychr in self.keyboard["upperSymbols"] and not modFlags:
            self._sendKeyWithModifiers(keychr, [AXKeyCodeConstants.SHIFT], globally)
            return

        if keychr.isupper() and not modFlags:
            self._sendKeyWithModifiers(
                keychr.lower(), [AXKeyCodeConstants.SHIFT], globally
            )
            return

        if keychr not in self.keyboard:
            self._clearEventQueue()
            raise ValueError("Key %s not found in keyboard layout" % keychr)

        # Press the key
        keyDown = Quartz.CGEventCreateKeyboardEvent(None, self.keyboard[keychr], True)
        # Release the key
        keyUp = Quartz.CGEventCreateKeyboardEvent(None, self.keyboard[keychr], False)
        # Set modflags on keyDown (default None):
        Quartz.CGEventSetFlags(keyDown, modFlags)
        # Set modflags on keyUp:
        Quartz.CGEventSetFlags(keyUp, modFlags)

        # Post the event to the given app
        if not globally:
            self._queueEvent(Quartz.CGEventPostToPid, (self._getPid(), keyDown))
            self._queueEvent(Quartz.CGEventPostToPid, (self._getPid(), keyUp))
        else:
            self._queueEvent(Quartz.CGEventPost, (0, keyDown))
            self._queueEvent(Quartz.CGEventPost, (0, keyUp))

    def _sendKey(self, keychr, modFlags=0, globally=False):
        """Send one character with no modifiers.

        Parameters: key character or constant referring to a non-alpha-numeric
                    key (e.g. RETURN or TAB)
                    modifier flags,
                    global or app specific
        Returns: None or raise ValueError exception
        """
        escapedChrs = {
            "\n": AXKeyCodeConstants.RETURN,
            "\r": AXKeyCodeConstants.RETURN,
            "\t": AXKeyCodeConstants.TAB,
        }
        if keychr in escapedChrs:
            keychr = escapedChrs[keychr]

        self._addKeyToQueue(keychr, modFlags, globally=globally)
        self._postQueuedEvents()

    def _sendKeys(self, keystr):
        """Send a series of characters with no modifiers.

        Parameters: keystr
        Returns: None or raise ValueError exception
        """
        for nextChr in keystr:
            self._sendKey(nextChr)

    def _pressModifiers(self, modifiers, pressed=True, globally=False):
        """Press given modifiers (provided in list form).

        Parameters: modifiers list, global or app specific
        Optional: keypressed state (default is True (down))
        Returns: Unsigned int representing flags to set
        """
        if not isinstance(modifiers, list):
            raise TypeError("Please provide modifiers in list form")

        if not hasattr(self, "keyboard"):
            self.keyboard = AXKeyboard.loadKeyboard()

        modFlags = 0

        # Press given modifiers
        for nextMod in modifiers:
            if nextMod not in self.keyboard:
                errStr = "Key %s not found in keyboard layout"
                self._clearEventQueue()
                raise ValueError(errStr % self.keyboard[nextMod])
            modEvent = Quartz.CGEventCreateKeyboardEvent(
                Quartz.CGEventSourceCreate(0), self.keyboard[nextMod], pressed
            )
            if not pressed:
                # Clear the modflags:
                Quartz.CGEventSetFlags(modEvent, 0)
            if globally:
                self._queueEvent(Quartz.CGEventPost, (0, modEvent))
            else:
                self._queueEvent(Quartz.CGEventPostToPid, (self._getPid(), modEvent))

            # Add the modifier flags
            modFlags += AXKeyboard.modKeyFlagConstants[nextMod]

        return modFlags

    def _holdModifierKeys(self, modifiers):
        """Hold given modifier keys (provided in list form).

        Parameters: modifiers list
        Returns: Unsigned int representing flags to set
        """
        modFlags = self._pressModifiers(modifiers)
        # Post the queued keypresses:
        self._postQueuedEvents()
        return modFlags

    def _releaseModifiers(self, modifiers, globally=False):
        """Release given modifiers (provided in list form).

        Parameters: modifiers list
        Returns: None
        """
        # Release them in reverse order from pressing them:
        modifiers.reverse()
        modFlags = self._pressModifiers(modifiers, pressed=False, globally=globally)
        return modFlags

    def _releaseModifierKeys(self, modifiers):
        """Release given modifier keys (provided in list form).

        Parameters: modifiers list
        Returns: Unsigned int representing flags to set
        """
        modFlags = self._releaseModifiers(modifiers)
        # Post the queued keypresses:
        self._postQueuedEvents()
        return modFlags

    @staticmethod
    def _isSingleCharacter(keychr):
        """Check whether given keyboard character is a single character.

        Parameters: key character which will be checked.
        Returns: True when given key character is a single character.
        """
        if not keychr:
            return False
        # Regular character case.
        if len(keychr) == 1:
            return True
        # Tagged character case.
        return (
            keychr.count("<") == 1
            and keychr.count(">") == 1
            and keychr[0] == "<"
            and keychr[-1] == ">"
        )

    def _sendKeyWithModifiers(self, keychr, modifiers, globally=False):
        """Send one character with the given modifiers pressed.

        Parameters: key character, list of modifiers, global or app specific
        Returns: None or raise ValueError exception
        """
        if not self._isSingleCharacter(keychr):
            raise ValueError("Please provide only one character to send")

        if not hasattr(self, "keyboard"):
            self.keyboard = AXKeyboard.loadKeyboard()

        modFlags = self._pressModifiers(modifiers, globally=globally)

        # Press the non-modifier key
        self._sendKey(keychr, modFlags, globally=globally)

        # Release the modifiers
        self._releaseModifiers(modifiers, globally=globally)

        # Post the queued keypresses:
        self._postQueuedEvents()

    def _queueMouseButton(
        self, coord, mouseButton, modFlags, clickCount=1, dest_coord=None
    ):
        """Private method to handle generic mouse button clicking.

        Parameters: coord (x, y) to click, mouseButton (e.g.,
                    kCGMouseButtonLeft), modFlags set (int)
        Optional: clickCount (default 1; set to 2 for double-click; 3 for
                  triple-click on host)
        Returns: None
        """
        # For now allow only left and right mouse buttons:
        mouseButtons = {
            Quartz.kCGMouseButtonLeft: "LeftMouse",
            Quartz.kCGMouseButtonRight: "RightMouse",
        }
        if mouseButton not in mouseButtons:
            raise ValueError("Mouse button given not recognized")

        eventButtonDown = getattr(Quartz, "kCGEvent%sDown" % mouseButtons[mouseButton])
        eventButtonUp = getattr(Quartz, "kCGEvent%sUp" % mouseButtons[mouseButton])
        eventButtonDragged = getattr(
            Quartz, "kCGEvent%sDragged" % mouseButtons[mouseButton]
        )

        # Press the button
        buttonDown = Quartz.CGEventCreateMouseEvent(
            None, eventButtonDown, coord, mouseButton
        )
        # Set modflags (default None) on button down:
        Quartz.CGEventSetFlags(buttonDown, modFlags)

        # Set the click count on button down:
        Quartz.CGEventSetIntegerValueField(
            buttonDown, Quartz.kCGMouseEventClickState, int(clickCount)
        )

        if dest_coord:
            # Drag and release the button
            buttonDragged = Quartz.CGEventCreateMouseEvent(
                None, eventButtonDragged, dest_coord, mouseButton
            )
            # Set modflags on the button dragged:
            Quartz.CGEventSetFlags(buttonDragged, modFlags)

            buttonUp = Quartz.CGEventCreateMouseEvent(
                None, eventButtonUp, dest_coord, mouseButton
            )
        else:
            # Release the button
            buttonUp = Quartz.CGEventCreateMouseEvent(
                None, eventButtonUp, coord, mouseButton
            )
        # Set modflags on the button up:
        Quartz.CGEventSetFlags(buttonUp, modFlags)

        # Set the click count on button up:
        Quartz.CGEventSetIntegerValueField(
            buttonUp, Quartz.kCGMouseEventClickState, int(clickCount)
        )
        # Queue the events
        self._queueEvent(Quartz.CGEventPost, (Quartz.kCGSessionEventTap, buttonDown))
        if dest_coord:
            self._queueEvent(Quartz.CGEventPost, (Quartz.kCGHIDEventTap, buttonDragged))
        self._queueEvent(Quartz.CGEventPost, (Quartz.kCGSessionEventTap, buttonUp))

    def _leftMouseDragged(self, stopCoord, strCoord, speed):
        """Private method to handle generic mouse left button dragging and
        dropping.

        Parameters: stopCoord(x,y) drop point
        Optional: strCoord (x, y) drag point, default (0,0) get current
                  mouse position
                  speed (int) 1 to unlimit, simulate mouse moving
                  action from some special requirement
        Returns: None
        """
        # Get current position as start point if strCoord not given
        if strCoord == (0, 0):
            loc = AppKit.NSEvent.mouseLocation()
            strCoord = (loc.x, Quartz.CGDisplayPixelsHigh(0) - loc.y)

        # Press left button down
        pressLeftButton = Quartz.CGEventCreateMouseEvent(
            None, Quartz.kCGEventLeftMouseDown, strCoord, Quartz.kCGMouseButtonLeft
        )
        # Queue the events
        Quartz.CGEventPost(Quartz.CoreGraphics.kCGHIDEventTap, pressLeftButton)
        # Wait for reponse of system, a fuzzy icon appears
        time.sleep(5)
        # Simulate mouse moving speed, k is slope
        speed = round(1 / float(speed), 2)
        xmoved = stopCoord[0] - strCoord[0]
        ymoved = stopCoord[1] - strCoord[1]
        if ymoved == 0:
            raise ValueError("Not support horizontal moving")
        else:
            k = abs(ymoved / xmoved)

        if xmoved != 0:
            for xpos in range(int(abs(xmoved))):
                if xmoved > 0 and ymoved > 0:
                    currcoord = (strCoord[0] + xpos, strCoord[1] + xpos * k)
                elif xmoved > 0 and ymoved < 0:
                    currcoord = (strCoord[0] + xpos, strCoord[1] - xpos * k)
                elif xmoved < 0 and ymoved < 0:
                    currcoord = (strCoord[0] - xpos, strCoord[1] - xpos * k)
                elif xmoved < 0 and ymoved > 0:
                    currcoord = (strCoord[0] - xpos, strCoord[1] + xpos * k)
                # Drag with left button
                dragLeftButton = Quartz.CGEventCreateMouseEvent(
                    None,
                    Quartz.kCGEventLeftMouseDragged,
                    currcoord,
                    Quartz.kCGMouseButtonLeft,
                )
                Quartz.CGEventPost(Quartz.CoreGraphics.kCGHIDEventTap, dragLeftButton)
                # Wait for reponse of system
                time.sleep(speed)
        else:
            raise ValueError("Not support vertical moving")
        upLeftButton = Quartz.CGEventCreateMouseEvent(
            None, Quartz.kCGEventLeftMouseUp, stopCoord, Quartz.kCGMouseButtonLeft
        )
        # Wait for reponse of system, a plus icon appears
        time.sleep(5)
        # Up left button up
        Quartz.CGEventPost(Quartz.CoreGraphics.kCGHIDEventTap, upLeftButton)

    def _waitFor(self, timeout, notification, **kwargs):
        """Wait for a particular UI event to occur; this can be built
        upon in NativeUIElement for specific convenience methods.
        """
        callback = self._matchOther
        retelem = None
        callbackArgs = None
        callbackKwargs = None

        # Allow customization of the callback, though by default use the basic
        # _match() method
        if "callback" in kwargs:
            callback = kwargs["callback"]
            del kwargs["callback"]

            # Deal with these only if callback is provided:
            if "args" in kwargs:
                if not isinstance(kwargs["args"], tuple):
                    errStr = "Notification callback args not given as a tuple"
                    raise TypeError(errStr)

                # If args are given, notification will pass back the returned
                # element in the first positional arg
                callbackArgs = kwargs["args"]
                del kwargs["args"]

            if "kwargs" in kwargs:
                if not isinstance(kwargs["kwargs"], dict):
                    errStr = "Notification callback kwargs not given as a dict"
                    raise TypeError(errStr)

                callbackKwargs = kwargs["kwargs"]
                del kwargs["kwargs"]
            # If kwargs are not given as a dictionary but individually listed
            # need to update the callbackKwargs dict with the remaining items in
            # kwargs
            if kwargs:
                if callbackKwargs:
                    callbackKwargs.update(kwargs)
                else:
                    callbackKwargs = kwargs
        else:
            if retelem:
                callbackArgs = (retelem,)
            # Pass the kwargs to the default callback
            callbackKwargs = kwargs

        return Observer(self).set_notification(
            timeout, notification, callback, callbackArgs, callbackKwargs
        )

    def waitForFocusToMatchCriteria(self, timeout=10, **kwargs):
        """Convenience method to wait for focused element to change
        (to element matching kwargs criteria).

        Returns: Element or None

        """

        def _matchFocused(retelem, **kwargs):
            return retelem if retelem._match(**kwargs) else None

        retelem = None
        return self._waitFor(
            timeout,
            "AXFocusedUIElementChanged",
            callback=_matchFocused,
            args=(retelem,),
            **kwargs
        )

    def _getActions(self):
        """Retrieve a list of actions supported by the object."""
        actions = self.ax_actions
        # strip leading AX from actions - help distinguish them from attributes
        return [action[2:] for action in actions]

    def _performAction(self, action):
        """Perform the specified action."""
        self._performAction("AX%s" % action)

    def _generateChildren(self):
        """Generator which yields all AXChildren of the object."""
        try:
            children = self.AXChildren
        except errors.AXError:
            return
        if children:
            for child in children:
                yield child

    def _generateChildrenR(self, target=None):
        """Generator which recursively yields all AXChildren of the object."""
        if target is None:
            target = self

        if "AXChildren" in target.ax_attributes:
            for child in target.AXChildren:
                yield child
                for c in self._generateChildrenR(child):
                    yield c
        else:
            return

    def _match(self, **kwargs):
        """Method which indicates if the object matches specified criteria.

        Match accepts criteria as kwargs and looks them up on attributes.
        Actual matching is performed with fnmatch, so shell-like wildcards
        work within match strings. Examples:

        obj._match(AXTitle='Terminal*')
        obj._match(AXRole='TextField', AXRoleDescription='search text field')
        """
        for k in kwargs.keys():
            try:
                val = getattr(self, k)
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

    def _matchOther(self, obj, **kwargs):
        """Perform _match but on another object, not self."""
        if obj is not None:
            # Need to check that the returned UI element wasn't destroyed first:
            if self._findFirstR(**kwargs):
                return obj._match(**kwargs)
        return False

    def _generateFind(self, **kwargs):
        """Generator which yields matches on AXChildren."""
        for needle in self._generateChildren():
            if needle._match(**kwargs):
                yield needle

    def _generateFindR(self, **kwargs):
        """Generator which yields matches on AXChildren and their children."""
        for needle in self._generateChildrenR():
            if needle._match(**kwargs):
                yield needle

    def _findAll(self, **kwargs):
        """Return a list of all children that match the specified criteria."""
        result = []
        for item in self._generateFind(**kwargs):
            result.append(item)
        return result

    def _findAllR(self, **kwargs):
        """Return a list of all children (recursively) that match the specified
        criteria.
        """
        result = []
        for item in self._generateFindR(**kwargs):
            result.append(item)
        return result

    def _findFirst(self, **kwargs):
        """Return the first object that matches the criteria."""
        for item in self._generateFind(**kwargs):
            return item

    def _findFirstR(self, **kwargs):
        """Search recursively for the first object that matches the criteria."""
        for item in self._generateFindR(**kwargs):
            return item

    def _getApplication(self):
        """Get the base application UIElement.

        If the UIElement is a child of the application, it will try
        to get the AXParent until it reaches the top application level
        element.
        """
        app = self
        while "AXParent" in app.ax_attributes:
            app = app.AXParent
        return app

    def _menuItem(self, menuitem, *args):
        """Return the specified menu item.

        Example - refer to items by name:

        app._menuItem(app.AXMenuBar, 'File', 'New').Press()
        app._menuItem(app.AXMenuBar, 'Edit', 'Insert', 'Line Break').Press()

        Refer to items by index:

        app._menuitem(app.AXMenuBar, 1, 0).Press()

        Refer to items by mix-n-match:

        app._menuitem(app.AXMenuBar, 1, 'About TextEdit').Press()
        """
        self._activate()
        for item in args:
            # If the item has an AXMenu as a child, navigate into it.
            # This seems like a silly abstraction added by apple's a11y api.
            if menuitem.AXChildren[0].AXRole == "AXMenu":
                menuitem = menuitem.AXChildren[0]
            # Find AXMenuBarItems and AXMenuItems using a handy wildcard
            try:
                menuitem = menuitem.AXChildren[int(item)]
            except ValueError:
                menuitem = menuitem.findFirst(AXRole="AXMenu*Item", AXTitle=item)
        return menuitem

    def _activate(self):
        """Activate the application (bringing menus and windows forward)."""
        ra = AppKit.NSRunningApplication
        app = ra.runningApplicationWithProcessIdentifier_(self.pid)
        # NSApplicationActivateAllWindows | NSApplicationActivateIgnoringOtherApps
        # == 3 - PyObjC in 10.6 does not expose these constants though so I have
        # to use the int instead of the symbolic names
        app.activateWithOptions_(3)

    def _getBundleId(self):
        """Return the bundle ID of the application."""
        ra = AppKit.NSRunningApplication
        app = ra.runningApplicationWithProcessIdentifier_(self.pid)
        return app.bundleIdentifier()

    def _getLocalizedName(self):
        """Return the localized name of the application."""
        return self._getApplication().AXTitle

    def __getattr__(self, name):
        """Handle attribute requests in several ways:

        1. If it starts with AX, it is probably an a11y attribute. Pass
           it to the handler in _a11y which will determine that for sure.
        2. See if the attribute is an action which can be invoked on the
           UIElement. If so, return a function that will invoke the attribute.
        """
        if "AX" + name in self.ax_actions:
            action = super(BaseAXUIElement, self).__getattr__("AX" + name)

            def performSpecifiedAction():
                # activate the app before performing the specified action
                self._activate()
                return action()

            return performSpecifiedAction
        else:
            return super(BaseAXUIElement, self).__getattr__(name)
