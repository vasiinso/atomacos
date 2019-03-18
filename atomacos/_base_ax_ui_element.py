from collections import deque

from atomacos import AXCallbacks, a11y


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

    def _generateChildren(self, target=None, recursive=False):
        """Generator which yields all AXChildren of the object."""
        if target is None:
            target = self

        if "AXChildren" not in target.ax_attributes:
            return

        for child in target.AXChildren:
            yield child
            if recursive:
                for c in self._generateChildren(child, recursive):
                    yield c

    def _findAll(self, recursive=False, **kwargs):
        """Return a list of all children that match the specified criteria."""
        for needle in self._generateChildren(recursive=recursive):
            if AXCallbacks.match(needle, **kwargs):
                yield needle

    def _findFirst(self, recursive=False, **kwargs):
        """Return the first object that matches the criteria."""
        for item in self._findAll(recursive=recursive, **kwargs):
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
