import pyautogui
from atomacos.AXKeyCodeConstants import COMMAND, CONTROL, OPTION, SHIFT

modifier_map = {COMMAND: "command", CONTROL: "ctrl", OPTION: "option", SHIFT: "shift"}


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

        Parameters: coordinates to click; modifiers (list) (e.g. [SHIFT] or
                    [COMMAND, SHIFT] (assuming you've first used
                    from pyatom.AXKeyCodeConstants import *))
        Returns: None
        """
        kb = Keyboard()
        kb.pressModifiers(modifiers)
        self.clickMouseButtonLeft(interval=interval, clicks=clicks)
        kb.releaseModifiers(modifiers)

    def clickMouseButtonRightWithMods(self, coord, modifiers, interval=None):
        """Click the right mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list)
        Returns: None
        """
        kb = Keyboard()
        kb.pressModifiers(modifiers)
        self.clickMouseButtonRight(interval=interval)
        kb.releaseModifiers(modifiers)

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
            strCoord = pyautogui.position()
        self.dragMouseButtonLeft(coord=strCoord, dest_coord=stopCoord, interval=speed)

    def doubleClickMouse(self, coord):
        """Double-click primary mouse button.

        Parameters: coordinates to click (assume primary is left button)
        Returns: None
        """
        self.clickMouseButtonLeft(coord=coord, clicks=2)

    def doubleMouseButtonLeftWithMods(self, coord, modifiers):
        """Click the left mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list)
        Returns: None
        """
        self.clickMouseButtonLeftWithMods(coord=coord, modifiers=modifiers, clicks=2)

    def tripleClickMouse(self, coord):
        """Triple-click primary mouse button.

        Parameters: coordinates to click (assume primary is left button)
        Returns: None
        """
        # Note above re: double-clicks applies to triple-clicks
        self.clickMouseButtonLeft(coord=coord, clicks=3)


class Keyboard(object):
    def sendKey(self, keychr):
        """Send one character with no modifiers."""
        pyautogui.press(keychr)

    def sendGlobalKey(self, keychr):
        """Send one character without modifiers to the system.

        It will not send an event directly to the application, system will
        dispatch it to the window which has keyboard focus.

        Parameters: keychr - Single keyboard character which will be sent.
        """
        self.sendKey(keychr)

    def sendKeys(self, keystr):
        """Send a series of characters with no modifiers."""
        pyautogui.typewrite(keystr)

    def pressModifiers(self, modifiers):
        """Hold modifier keys (e.g. [Option])."""
        for modifier in modifiers:
            pyautogui.keyDown(modifier_map[modifier])

    def releaseModifiers(self, modifiers):
        """Release modifier keys (e.g. [Option])."""
        for modifier in modifiers:
            pyautogui.keyUp(modifier_map[modifier])

    def sendKeyWithModifiers(self, keychr, modifiers):
        """Send one character with modifiers pressed

        Parameters: key character, modifiers (list) (e.g. [SHIFT] or
                    [COMMAND, SHIFT] (assuming you've first used
                    from pyatom.AXKeyCodeConstants import *))
        """
        self.pressModifiers(modifiers)
        self.sendKeys(keychr)
        self.releaseModifiers(modifiers)

    def sendGlobalKeyWithModifiers(self, keychr, modifiers):
        """Global send one character with modifiers pressed.

        See sendKeyWithModifiers
        """
        self.sendKeyWithModifiers(keychr, modifiers)


class KeyboardMouseMixin(Mouse, Keyboard):
    pass
