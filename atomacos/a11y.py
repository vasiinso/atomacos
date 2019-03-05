from atomacos.errors import AXErrorUnsupported
from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCreateSystemWide,
)


class AXUIElement:
    def __init__(self, ref=None):
        self.ref = ref

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
