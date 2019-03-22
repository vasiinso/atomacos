import pyautogui


class Mouse(object):
    def dragMouseButtonLeft(self, coord, dest_coord, interval=0.5):
        """Drag the left mouse button without modifiers pressed.

        Parameters: coordinates to click on screen (tuple (x, y))
                    dest coordinates to drag to (tuple (x, y))
                    interval to send event of btn down, drag and up
        Returns: None
        """
        pyautogui.moveTo(*coord)
        pyautogui.dragTo(*dest_coord, duration=interval, button="left")

    def doubleClickDragMouseButtonLeft(self, coord, dest_coord, interval=0.5):
        """Double-click and drag the left mouse button without modifiers
        pressed.

        Parameters: coordinates to double-click on screen (tuple (x, y))
                    dest coordinates to drag to (tuple (x, y))
                    interval to send event of btn down, drag and up
        Returns: None
        """
        pyautogui.click(*coord)
        pyautogui.dragTo(*dest_coord, duration=interval, button="left")

    def clickMouseButtonLeft(self, coord, interval=0.0, clicks=1):
        """Click the left mouse button without modifiers pressed.

        Parameters: coordinates to click on screen (tuple (x, y))
        Returns: None
        """
        pyautogui.click(*coord, interval=interval, button="left", clicks=clicks)

    def clickMouseButtonRight(self, coord, interval=0.0):
        """Click the right mouse button without modifiers pressed.

        Parameters: coordinates to click on scren (tuple (x, y))
        Returns: None
        """
        pyautogui.click(*coord, interval=interval, button="right")

    def clickMouseButtonLeftWithMods(self, coord, modifiers, interval=None, clicks=1):
        """Click the left mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list) (e.g. ["shift"] or
                    ["command", "shift"])
        Returns: None
        """
        kb = Keyboard()
        kb.pressModifiers(modifiers)
        self.clickMouseButtonLeft(coord, interval=interval, clicks=clicks)
        kb.releaseModifiers(modifiers)

    def clickMouseButtonRightWithMods(self, coord, modifiers, interval=None):
        """Click the right mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list)
        Returns: None
        """
        kb = Keyboard()
        kb.pressModifiers(modifiers)
        self.clickMouseButtonRight(coord, interval=interval)
        kb.releaseModifiers(modifiers)

    def leftMouseDragged(self, stopCoord, strCoord=(0, 0), speed=1):
        """Click the left mouse button and drag object.

        Parameters: stopCoord, the position of dragging stopped
                    strCoord, the position of dragging started
                    (0,0) will get current position
                    speed is mouse moving speed, 0 to unlimited
        Returns: None
        """
        if strCoord == (0, 0):
            strCoord = pyautogui.position()
        self.dragMouseButtonLeft(coord=strCoord, dest_coord=stopCoord, interval=speed)

    def doubleClickMouse(self, coord):
        """Double-click primary mouse button.

        Parameters: coordinates to click (assume primary is left button)
        Returns: None
        """
        pyautogui.doubleClick(*coord, button="left")

    def doubleMouseButtonLeftWithMods(self, coord, modifiers):
        """Click the left mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list)
        Returns: None
        """
        kb = Keyboard()
        kb.pressModifiers(modifiers)
        pyautogui.doubleClick(*coord, button="left")
        kb.releaseModifiers(modifiers)

    def tripleClickMouse(self, coord):
        """Triple-click primary mouse button.

        Parameters: coordinates to click (assume primary is left button)
        Returns: None
        """
        pyautogui.tripleClick(*coord, button="left")


class Keyboard(object):
    def sendKey(self, keychr):
        """Send one character with no modifiers."""
        pyautogui.press(keychr)

    def sendKeyWithModifiers(self, keychr, modifiers):
        """Send one character with modifiers pressed

        Parameters: key character, modifiers (list) (e.g. ["shift"] or
                    ["command", "shift"]
        """
        self.pressModifiers(modifiers)
        self.sendKey(keychr)
        self.releaseModifiers(modifiers)

    def sendGlobalKey(self, keychr):
        """Send one character without modifiers to the system.

        It will not send an event directly to the application, system will
        dispatch it to the window which has keyboard focus.

        Parameters: keychr - Single keyboard character which will be sent.
        """
        self.sendKey(keychr)

    def sendGlobalKeyWithModifiers(self, keychr, modifiers):
        """Global send one character with modifiers pressed.

        See sendKeyWithModifiers
        """
        self.sendKeyWithModifiers(keychr, modifiers)

    def sendKeys(self, keystr):
        """Send a series of characters with no modifiers."""
        pyautogui.typewrite(keystr)

    def pressModifiers(self, modifiers):
        """Hold modifier keys (e.g. [Option])."""
        for modifier in modifiers:
            pyautogui.keyDown(modifier)

    def releaseModifiers(self, modifiers):
        """Release modifier keys (e.g. [Option])."""
        for modifier in modifiers:
            pyautogui.keyUp(modifier)


class KeyboardMouseMixin(Mouse, Keyboard):
    pass
