import Quartz


class KeyboardMouseMixin(object):
    def sendKey(self, keychr):
        """Send one character with no modifiers."""
        return self._sendKey(keychr)

    def sendGlobalKey(self, keychr):
        """Send one character without modifiers to the system.

        It will not send an event directly to the application, system will
        dispatch it to the window which has keyboard focus.

        Parameters: keychr - Single keyboard character which will be sent.
        """
        return self._sendKey(keychr, globally=True)

    def sendKeys(self, keystr):
        """Send a series of characters with no modifiers."""
        return self._sendKeys(keystr)

    def pressModifiers(self, modifiers):
        """Hold modifier keys (e.g. [Option])."""
        return self._holdModifierKeys(modifiers)

    def releaseModifiers(self, modifiers):
        """Release modifier keys (e.g. [Option])."""
        return self._releaseModifierKeys(modifiers)

    def sendKeyWithModifiers(self, keychr, modifiers):
        """Send one character with modifiers pressed

        Parameters: key character, modifiers (list) (e.g. [SHIFT] or
                    [COMMAND, SHIFT] (assuming you've first used
                    from pyatom.AXKeyCodeConstants import *))
        """
        return self._sendKeyWithModifiers(keychr, modifiers, False)

    def sendGlobalKeyWithModifiers(self, keychr, modifiers):
        """Global send one character with modifiers pressed.

        See sendKeyWithModifiers
        """
        return self._sendKeyWithModifiers(keychr, modifiers, True)

    def dragMouseButtonLeft(self, coord, dest_coord, interval=0.5):
        """Drag the left mouse button without modifiers pressed.

        Parameters: coordinates to click on screen (tuple (x, y))
                    dest coordinates to drag to (tuple (x, y))
                    interval to send event of btn down, drag and up
        Returns: None
        """

        modFlags = 0
        self._queueMouseButton(
            coord, Quartz.kCGMouseButtonLeft, modFlags, dest_coord=dest_coord
        )
        self._postQueuedEvents(interval=interval)

    def doubleClickDragMouseButtonLeft(self, coord, dest_coord, interval=0.5):
        """Double-click and drag the left mouse button without modifiers
        pressed.

        Parameters: coordinates to double-click on screen (tuple (x, y))
                    dest coordinates to drag to (tuple (x, y))
                    interval to send event of btn down, drag and up
        Returns: None
        """
        modFlags = 0
        self._queueMouseButton(
            coord, Quartz.kCGMouseButtonLeft, modFlags, dest_coord=dest_coord
        )
        self._queueMouseButton(
            coord,
            Quartz.kCGMouseButtonLeft,
            modFlags,
            dest_coord=dest_coord,
            clickCount=2,
        )
        self._postQueuedEvents(interval=interval)

    def clickMouseButtonLeft(self, coord, interval=None):
        """Click the left mouse button without modifiers pressed.

        Parameters: coordinates to click on screen (tuple (x, y))
        Returns: None
        """

        modFlags = 0
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags)
        if interval:
            self._postQueuedEvents(interval=interval)
        else:
            self._postQueuedEvents()

    def clickMouseButtonRight(self, coord):
        """Click the right mouse button without modifiers pressed.

        Parameters: coordinates to click on scren (tuple (x, y))
        Returns: None
        """
        modFlags = 0
        self._queueMouseButton(coord, Quartz.kCGMouseButtonRight, modFlags)
        self._postQueuedEvents()

    def clickMouseButtonLeftWithMods(self, coord, modifiers, interval=None):
        """Click the left mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list) (e.g. [SHIFT] or
                    [COMMAND, SHIFT] (assuming you've first used
                    from pyatom.AXKeyCodeConstants import *))
        Returns: None
        """
        modFlags = self._pressModifiers(modifiers)
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags)
        self._releaseModifiers(modifiers)
        if interval:
            self._postQueuedEvents(interval=interval)
        else:
            self._postQueuedEvents()

    def clickMouseButtonRightWithMods(self, coord, modifiers):
        """Click the right mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list)
        Returns: None
        """
        modFlags = self._pressModifiers(modifiers)
        self._queueMouseButton(coord, Quartz.kCGMouseButtonRight, modFlags)
        self._releaseModifiers(modifiers)
        self._postQueuedEvents()

    def leftMouseDragged(self, stopCoord, strCoord=(0, 0), speed=1):
        """Click the left mouse button and drag object.

        Parameters: stopCoord, the position of dragging stopped
                    strCoord, the position of dragging started
                    (0,0) will get current position
                    speed is mouse moving speed, 0 to unlimited
        Returns: None
        """
        self._leftMouseDragged(stopCoord, strCoord, speed)

    def doubleClickMouse(self, coord):
        """Double-click primary mouse button.

        Parameters: coordinates to click (assume primary is left button)
        Returns: None
        """
        modFlags = 0
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags)
        # This is a kludge:
        # If directed towards a Fusion VM the clickCount gets ignored and this
        # will be seen as a single click, so in sequence this will be a double-
        # click
        # Otherwise to a host app only this second one will count as a double-
        # click
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags, clickCount=2)
        self._postQueuedEvents()

    def doubleMouseButtonLeftWithMods(self, coord, modifiers):
        """Click the left mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list)
        Returns: None
        """
        modFlags = self._pressModifiers(modifiers)
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags)
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags, clickCount=2)
        self._releaseModifiers(modifiers)
        self._postQueuedEvents()

    def tripleClickMouse(self, coord):
        """Triple-click primary mouse button.

        Parameters: coordinates to click (assume primary is left button)
        Returns: None
        """
        # Note above re: double-clicks applies to triple-clicks
        modFlags = 0
        for _ in range(2):
            self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags)
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags, clickCount=3)
        self._postQueuedEvents()
