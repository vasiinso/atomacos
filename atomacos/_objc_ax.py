"""
Wrap objc calls to raise python exception
"""
from ApplicationServices import (
    AXObserverAddNotification,
    AXObserverCreate,
    AXObserverRemoveNotification,
)
from atomacos import errors


def PAXObserverCreate(application, callback):
    """
    Creates a new observer that can receive notifications
    from the specified application.

    Args:
        application: The process ID of the application
        callback: The callback function

    Returns: an AXObserverRef representing the observer object

    """
    err, observer = AXObserverCreate(application, callback, None)
    errors.check_ax_error(err, "Could not create observer for notification")
    return observer


def PAXObserverAddNotification(observer, element, notification, refcon):
    """
    Registers the specified observer to receive notifications from
    the specified accessibility object

    Args:
        observer: The observer object created from a call to AXObserverCreate
        element: The accessibility object for which to observe notifications
        notification: The name of the notification to observe
        refcon: Application-defined data passed to the callback when it is called

    """
    err = AXObserverAddNotification(observer, element, notification, refcon)
    errors.check_ax_error(err, "Could not add notification to observer")


def PAXObserverRemoveNotification(observer, element, notification):
    """
    Removes the specified notification from the list of notifications the
    observer wants to receive from the accessibility object.

    Args:
        observer: The observer object created from a call to AXObserverCreate
        element: The accessibility object for which this observer observes notifications
        notification: The name of the notification to remove from
            the list of observed notifications

    """
    err = AXObserverRemoveNotification(observer, element, notification)
    errors.check_ax_error(err, "Could not remove notification from observer")
