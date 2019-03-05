from atomacos import converter
from atomacos.errors import (
    AXErrorUnsupported,
    raise_ax_error,
    AXErrorIllegalArgument,
)
from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCreateSystemWide,
    AXUIElementCopyAttributeValue,
    AXUIElementCopyAttributeNames,
    AXUIElementCopyActionNames,
    AXUIElementCopyElementAtPosition,
    AXUIElementGetPid,
    AXUIElementIsAttributeSettable,
    AXUIElementSetAttributeValue,
    AXUIElementPerformAction,
    kAXErrorSuccess,
    CFEqual,
    NSWorkspace,
    AXIsProcessTrusted,
)


class AXUIElement:
    def __init__(self, ref=None):
        self.ref = ref
        self.converter = converter.Converter(self.__class__)

    def __getattr__(self, item):
        if item in self.ax_attributes:
            return self._get_ax_attribute(item)
        elif item in self.ax_actions:

            def perform_ax_action():
                self._perform_ax_actions(item)

            return perform_ax_action
        else:
            raise AttributeError("%s has no attribute '%s'" % (self, item))

    def __setattr__(self, key, value):
        super(AXUIElement, self).__setattr__(key, value)
        try:
            if key in self.ax_attributes:
                self._set_ax_attribute(key, value)
        except AXErrorIllegalArgument:
            pass

    def __dir__(self):
        return (
            self.ax_attributes
            + self.ax_actions
            + super(AXUIElement, self).__dir__()
        )

    def _get_ax_attribute(self, item):
        """Get the value of the the specified attribute"""
        if item in self.ax_attributes:
            err, attrValue = AXUIElementCopyAttributeValue(
                self.ref, item, None
            )
            return self.converter.convert_value(attrValue)
        else:
            raise AttributeError("has no AX Attribute %s" % item)

    def _set_ax_attribute(self, name, value):
        """
        Set the specified attribute to the specified value
        """
        self._get_ax_attribute(name)

        err, to_set = AXUIElementCopyAttributeValue(self.ref, name, None)
        if err != kAXErrorSuccess:
            raise_ax_error(err, "Error retrieving attribute to set")

        err, settable = AXUIElementIsAttributeSettable(self.ref, name, None)
        if err != kAXErrorSuccess:
            raise_ax_error(err, "Error querying attribute")

        if not settable:
            raise AXErrorUnsupported("Attribute is not settable")

        err = AXUIElementSetAttributeValue(self.ref, name, value)

        if err != kAXErrorSuccess:
            raise_ax_error(err, "Error setting attribute value")

    @property
    def ax_attributes(self):
        """
        Get a list of attributes available on the AXUIElement
        """
        err, attr = AXUIElementCopyAttributeNames(self.ref, None)

        if err != kAXErrorSuccess:
            raise_ax_error(err, "Error retrieving attribute list")
        else:
            return list(attr)

    @property
    def ax_actions(self):
        """
        Get a list of actions available on the AXUIElement
        """
        err, actions = AXUIElementCopyActionNames(self.ref, None)

        if err != kAXErrorSuccess:
            raise_ax_error(err, "Error retrieving action names")
        else:
            return list(action[2:] for action in actions)

    def _perform_ax_actions(self, name):
        real_action_name = "AX" + name
        err = AXUIElementPerformAction(self.ref, real_action_name)

        if err != kAXErrorSuccess:
            raise_ax_error(err, "Error performing requested action")

    @property
    def pid(self):
        error_code, pid = AXUIElementGetPid(self.ref, None)
        if error_code != kAXErrorSuccess:
            raise_ax_error(error_code, "Error retrieving PID")
        return pid

    @classmethod
    def from_pid(cls, pid):
        """
        Get an AXUIElement reference to the application by specified PID.
        """
        app_ref = AXUIElementCreateApplication(pid)

        if app_ref is None:
            raise AXErrorUnsupported("Error getting app ref")

        return cls(ref=app_ref)

    @classmethod
    def systemwide(cls):
        """Get an AXUIElement reference for the system accessibility object."""
        app_ref = AXUIElementCreateSystemWide()

        if app_ref is None:
            raise AXErrorUnsupported("Error getting a11y object")

        return cls(ref=app_ref)

    def __eq__(self, other):
        print(str(other), str(self))
        if not isinstance(other, type(self)):
            return False
        if self.ref is None and other.ref is None:
            return True

        if self.ref is None or other.ref is None:
            return False

        return CFEqual(self.ref, other.ref)

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_element_at_position(self, x, y):
        if self.ref is None:
            raise AXErrorUnsupported(
                "Operation not supported on null element references"
            )

        err, res = AXUIElementCopyElementAtPosition(self.ref, x, y, None)
        if err != kAXErrorSuccess:
            try:
                raise_ax_error(err, "Unable to get element at position")
            except AXErrorIllegalArgument:
                raise ValueError("Arguments must be two floats.")

        return self.__class__(res)


def get_frontmost_pid():
    """Return the PID of the application in the foreground."""
    frontmost_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    pid = frontmost_app.processIdentifier()
    return pid


def axenabled():
    """Return the status of accessibility on the system."""
    return AXIsProcessTrusted()
