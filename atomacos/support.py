from ApplicationServices import NSWorkspace, AXIsProcessTrusted


def get_frontmost_pid():
    frontmost_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    pid = frontmost_app.processIdentifier()
    return pid


def axenabled():
    """
    Return the status of accessibility on the system.
    :return: bool
    """
    return AXIsProcessTrusted()
