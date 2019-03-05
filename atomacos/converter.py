from CoreFoundation import CFGetTypeID, CFArrayGetTypeID


def convert_value(value):
    if CFGetTypeID(value) == CFArrayGetTypeID():
        return convert_list(value)
    else:
        return value


def convert_list(value):
    return [item for item in value]
