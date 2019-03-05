from CoreFoundation import CFGetTypeID, CFArrayGetTypeID
from ApplicationServices import (
    AXUIElementGetTypeID,
    AXValueGetType,
    kAXValueCGSizeType,
    kAXValueCGPointType,
    NSSizeFromString,
)
import re


def convert_value(value, cls=None):
    if CFGetTypeID(value) == AXUIElementGetTypeID():
        return convert_app_ref(cls, value)
    if CFGetTypeID(value) == CFArrayGetTypeID():
        return convert_list(value, cls)
    if AXValueGetType(value) == kAXValueCGSizeType:
        return convert_size(value)
    if AXValueGetType(value) == kAXValueCGPointType:
        return convert_size(value)
    else:
        return value


def convert_list(value, cls=None):
    return [convert_value(item, cls) for item in value]


def convert_app_ref(cls, value):
    return cls(value)


def convert_size(value):
    repr_searched = re.search("{.*}", str(value)).group()
    return tuple(NSSizeFromString(repr_searched))
