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
    AXUIElementGetPid,
    AXUIElementIsAttributeSettable,
    AXUIElementSetAttributeValue,
    kAXErrorSuccess,
    CFEqual,
)


class AXUIElement:
    def __init__(self, ref=None):
        self.ref = ref

    def __getattr__(self, item):
        if item in self.ax_attributes:
            return self._get_ax_attribute(item)

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
            return converter.convert_value(attrValue, self.__class__)
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
            return list(actions)

    @property
    def pid(self):
        error_code, pid = AXUIElementGetPid(self.ref, None)
        if error_code != kAXErrorSuccess:
            raise_ax_error(error_code, "Error retrieving PID")
        return pid

    @classmethod
    def from_pid(cls, pid):
        app_ref = AXUIElementCreateApplication(pid)

        if app_ref is None:
            raise AXErrorUnsupported("Error getting app ref")

        return cls(ref=app_ref)

    @classmethod
    def systemwide(cls):
        app_ref = AXUIElementCreateSystemWide()

        if app_ref is None:
            raise AXErrorUnsupported("Error getting a11y object")

        return cls(ref=app_ref)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if self.ref is None and other.ref is None:
            return True

        if self.ref is None or other.ref is None:
            return False

        return CFEqual(self.ref, other.ref)

    def __ne__(self, other):
        return not self.__eq__(other)
