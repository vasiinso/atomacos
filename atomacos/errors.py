from ApplicationServices import (
    kAXErrorActionUnsupported,
    kAXErrorAPIDisabled,
    kAXErrorCannotComplete,
    kAXErrorFailure,
    kAXErrorIllegalArgument,
    kAXErrorInvalidUIElement,
    kAXErrorNotImplemented,
    kAXErrorNoValue,
    kAXErrorSuccess,
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


class AXErrorFailure(AXError):
    pass


def AXErrorFactory(code):
    return {
        kAXErrorAPIDisabled: AXErrorAPIDisabled,
        kAXErrorInvalidUIElement: AXErrorInvalidUIElement,
        kAXErrorCannotComplete: AXErrorCannotComplete,
        kAXErrorNotImplemented: AXErrorNotImplemented,
        kAXErrorIllegalArgument: AXErrorIllegalArgument,
        kAXErrorNoValue: AXErrorNoValue,
        kAXErrorFailure: AXErrorFailure,
        kAXErrorActionUnsupported: AXErrorActionUnsupported,
    }.get(code, AXErrorUnsupported)


def check_ax_error(error_code, error_messages):
    """
    Returns if code is kAXErrorSuccess.
    Raises an error with given message based on given error code.
    Defaults to AXErrorUnsupported for unknown codes.

    Args:
        error_code: the error code
        error_messages: mapping from error code to error message
    """
    if error_code == kAXErrorSuccess:
        return

    try:
        error_message = error_messages[error_code]
    except KeyError:
        error_message = "Unknown AX Error: %s" % error_code

    raise AXErrorFactory(error_code)(error_message)
