from ApplicationServices import (
    kAXErrorAPIDisabled,
    kAXErrorInvalidUIElement,
    kAXErrorCannotComplete,
    kAXErrorNotImplemented,
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


def set_error(code, message):
    """
    Raises an error with given message based on given error code.
    Defaults to AXErrorUnsupported for unknown codes.
    """
    CODE_TO_AXERROR = {
        kAXErrorAPIDisabled: AXErrorAPIDisabled,
        kAXErrorInvalidUIElement: AXErrorInvalidUIElement,
        kAXErrorCannotComplete: AXErrorCannotComplete,
        kAXErrorNotImplemented: AXErrorNotImplemented,
    }

    ErrorFromCode = CODE_TO_AXERROR.get(code, AXErrorUnsupported)
    raise ErrorFromCode("%s (AX Error %s)" % (message, code))
