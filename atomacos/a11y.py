from atomacos import converter
from atomacos.errors import AXErrorUnsupported, set_error
from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCreateSystemWide,
    AXUIElementCopyAttributeValue,
    AXUIElementCopyAttributeNames,
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
        err, attr = AXUIElementCopyAttributeNames(self.ref, None)

        if err != kAXErrorSuccess:
            set_error(err, "Error retrieving attribute list")
        else:
            return list(attr)

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
