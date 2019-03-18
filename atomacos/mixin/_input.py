import time

import AppKit
import Quartz
from atomacos import AXKeyboard, AXKeyCodeConstants


class EventQueue(object):
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


class Mouse(object):
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


class Keyboard(object):
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
            self._queueEvent(Quartz.CGEventPostToPid, (self.pid, keyDown))
            self._queueEvent(Quartz.CGEventPostToPid, (self.pid, keyUp))
        else:
            self._queueEvent(Quartz.CGEventPost, (0, keyDown))
            self._queueEvent(Quartz.CGEventPost, (0, keyUp))

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


class KeyboardMouseMixin(Mouse, Keyboard, EventQueue):
    pass
