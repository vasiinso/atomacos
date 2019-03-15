from ApplicationServices import (
    kAXErrorAPIDisabled,
    kAXErrorInvalidUIElement,
    kAXErrorCannotComplete,
    kAXErrorNotImplemented,
    kAXErrorIllegalArgument,
    kAXErrorActionUnsupported,
    kAXErrorSuccess,
    kAXErrorNoValue,
)


class AXError(Exception):
    pass


class AXErrorUnsupported(AXError):
    pass


class AXErrorAPIDisabled(AXError):
    pass


class AXErrorInvalidUIElement(AXError):
    pass


class AXErrorCannotComplete(AXError):
    pass


class AXErrorNotImplemented(AXError):
    pass


class AXErrorIllegalArgument(AXError):
    pass


class AXErrorActionUnsupported(AXError):
    pass


class AXErrorNoValue(AXError):
    pass


def raise_ax_error(code, message):
    """
    Raises an error with given message based on given error code.
    Defaults to AXErrorUnsupported for unknown codes.
    """
    if code == kAXErrorSuccess:
        return

    CODE_TO_AXERROR = {
        kAXErrorAPIDisabled: AXErrorAPIDisabled,
        kAXErrorInvalidUIElement: AXErrorInvalidUIElement,
        kAXErrorCannotComplete: AXErrorCannotComplete,
        kAXErrorNotImplemented: AXErrorNotImplemented,
        kAXErrorIllegalArgument: AXErrorIllegalArgument,
        kAXErrorNoValue: AXErrorNoValue,
        kAXErrorActionUnsupported: AXErrorActionUnsupported,
    }

    ErrorFromCode = CODE_TO_AXERROR.get(code, AXErrorUnsupported)
    raise ErrorFromCode("%s (AX Error %s)" % (message, code))
