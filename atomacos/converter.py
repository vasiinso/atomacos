from CoreFoundation import CFGetTypeID, CFArrayGetTypeID
from ApplicationServices import AXUIElementGetTypeID


def convert_value(value, cls=None):
    if CFGetTypeID(value) == AXUIElementGetTypeID():
        return convert_app_ref(cls, value)
    if CFGetTypeID(value) == CFArrayGetTypeID():
        return convert_list(value, cls)
    else:
        return value


def convert_list(value, cls=None):
    return [convert_value(item, cls) for item in value]


def convert_app_ref(cls, value):
    return cls(value)
