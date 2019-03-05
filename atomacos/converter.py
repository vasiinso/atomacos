from collections import namedtuple

from CoreFoundation import CFGetTypeID, CFArrayGetTypeID
from ApplicationServices import (
    AXUIElementGetTypeID,
    AXValueGetType,
    kAXValueCGSizeType,
    kAXValueCGPointType,
    kAXValueCFRangeType,
    NSSizeFromString,
    NSPointFromString,
    NSRangeFromString,
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
        return convert_point(value)
    if AXValueGetType(value) == kAXValueCFRangeType:
        return convert_range(value)
    else:
        return value


def convert_list(value, cls=None):
    return [convert_value(item, cls) for item in value]


def convert_app_ref(cls, value):
    return cls(value)


def convert_size(value):
    repr_searched = re.search("{.*}", str(value)).group()
    CGSize = namedtuple("CGSize", ["width", "height"])
    size = NSSizeFromString(repr_searched)

    return CGSize(size.width, size.height)


def convert_point(value):
    repr_searched = re.search("{.*}", str(value)).group()
    CGPoint = namedtuple("CGPoint", ["x", "y"])
    point = NSPointFromString(repr_searched)

    return CGPoint(point.x, point.y)


def convert_range(value):
    repr_searched = re.search("{.*}", str(value)).group()
    CFRange = namedtuple("CFRange", ["location", "length"])
    range = NSRangeFromString(repr_searched)

    return CFRange(range.location, range.length)
