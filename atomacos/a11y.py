from atomacos import converter
from atomacos.errors import AXErrorUnsupported, raise_ax_error
from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCreateSystemWide,
    AXUIElementCopyAttributeValue,
    AXUIElementCopyAttributeNames,
    AXUIElementCopyActionNames,
    kAXErrorSuccess,
)


class AXUIElement:
    def __init__(self, ref=None):
        self.ref = ref

    def __getattr__(self, item):
        if item in self._get_ax_attributes():
            err, attrValue = AXUIElementCopyAttributeValue(
                self.ref, item, None
            )
            return converter.convert_value(attrValue)
        else:
            raise AttributeError("has no AX Attribute %s" % item)

    def __dir__(self):
        return self._get_ax_attributes() + super(AXUIElement, self).__dir__()

    def _get_ax_attributes(self):
        """
        Get a list of attributes available on the AXUIElement
        """
        err, attr = AXUIElementCopyAttributeNames(self.ref, None)

        if err != kAXErrorSuccess:
            raise_ax_error(err, "Error retrieving attribute list")
        else:
            return list(attr)

    def _get_ax_actions(self):
        """
        Get a list of actions available on the AXUIElement
        """
        err, actions = AXUIElementCopyActionNames(self.ref, None)

        if err != kAXErrorSuccess:
            raise_ax_error(err, "Error retrieving action names")
        else:
            return list(actions)

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
