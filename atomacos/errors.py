from ApplicationServices import (
    kAXErrorActionUnsupported,
    kAXErrorAPIDisabled,
    kAXErrorCannotComplete,
    kAXErrorIllegalArgument,
    kAXErrorInvalidUIElement,
    kAXErrorNotImplemented,
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


def AXErrorFactory(code):
    return {
        kAXErrorAPIDisabled: AXErrorAPIDisabled,
        kAXErrorInvalidUIElement: AXErrorInvalidUIElement,
        kAXErrorCannotComplete: AXErrorCannotComplete,
        kAXErrorNotImplemented: AXErrorNotImplemented,
        kAXErrorIllegalArgument: AXErrorIllegalArgument,
        kAXErrorNoValue: AXErrorNoValue,
        kAXErrorActionUnsupported: AXErrorActionUnsupported,
    }.get(code, AXErrorUnsupported)


def raise_ax_error(code, message):
    """
    Raises an error with given message based on given error code.
    Defaults to AXErrorUnsupported for unknown codes.
    """
    error_message = "%s (AX Error %s)" % (message, code)

    raise AXErrorFactory(code)(error_message)
