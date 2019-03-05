from ApplicationServices import NSWorkspace


def get_frontmost_pid():
    frontmost_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    pid = frontmost_app.processIdentifier()
    return pid
