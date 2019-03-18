"""
Wrap objc calls to raise python exception
"""
from ApplicationServices import (
    AXObserverAddNotification,
    AXObserverCreate,
    AXObserverRemoveNotification,
    AXUIElementCopyActionNames,
    AXUIElementCopyAttributeNames,
    AXUIElementCopyAttributeValue,
    AXUIElementCopyElementAtPosition,
    AXUIElementGetPid,
    AXUIElementIsAttributeSettable,
    AXUIElementPerformAction,
    AXUIElementSetAttributeValue,
    AXUIElementSetMessagingTimeout,
)
from atomacos import errors
from objc import callbackFor

PAXObserverCallback = callbackFor(AXObserverCreate)


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


def PAXUIElementCopyAttributeValue(element, attribute):
    """
    Returns the value of an accessibility object's attribute

    Args:
        element: The AXUIElementRef representing the accessibility object
        attribute: The attribute name

    Returns: the value associated with the specified attribute

    """
    err, attrValue = AXUIElementCopyAttributeValue(element, attribute, None)
    errors.check_ax_error(err, "Unable to get attribute. %s" % attribute)
    return attrValue


def PAXUIElementIsAttributeSettable(element, attribute):
    """
    Returns whether the specified accessibility object's attribute can be modified

    Args:
        element: The AXUIElementRef representing the accessibility object
        attribute: The attribute name

    Returns: a Boolean value indicating whether the attribute is settable

    """
    err, settable = AXUIElementIsAttributeSettable(element, attribute, None)
    errors.check_ax_error(err, "Error querying attribute")
    return settable


def PAXUIElementSetAttributeValue(element, attribute, value):
    """
    Sets the accessibility object's attribute to the specified value

    Args:
        element: The AXUIElementRef representing the accessibility object
        attribute: The attribute name
        value: The new value for the attribute

    """
    err = AXUIElementSetAttributeValue(element, attribute, value)
    errors.check_ax_error(err, "Error setting attribute value")


def PAXUIElementCopyAttributeNames(element):
    """
    Returns a list of all the attributes supported by the specified accessibility object

    Args:
        element: The AXUIElementRef representing the accessibility object

    Returns: an array containing the accessibility object's attribute names

    """
    err, names = AXUIElementCopyAttributeNames(element, None)
    errors.check_ax_error(err, "Error retrieving attribute list")
    return names


def PAXUIElementCopyActionNames(element):
    """
    Returns a list of all the actions the specified accessibility object can perform

    Args:
        element: The AXUIElementRef representing the accessibility object

    Returns: an array of actions the accessibility object can perform
        (empty if the accessibility object supports no actions)

    """
    err, names = AXUIElementCopyActionNames(element, None)
    errors.check_ax_error(err, "Error retrieving action names")
    return names


def PAXUIElementPerformAction(element, action):
    """
    Requests that the specified accessibility object perform the specified action

    Args:
        element: The AXUIElementRef representing the accessibility object
        action: The action to be performed

    """
    err = AXUIElementPerformAction(element, action)
    errors.check_ax_error(err, "Error performing requested action")


def PAXUIElementGetPid(element):
    """
    Returns the process ID associated with the specified accessibility object

    Args:
        element: The AXUIElementRef representing an accessibility object

    Returns: the process ID associated with the specified accessibility object

    """
    err, pid = AXUIElementGetPid(element, None)
    errors.check_ax_error(err, "Error retrieving PID")
    return pid


def PAXUIElementCopyElementAtPosition(application, x, y):
    """
    Returns the accessibility object at the specified position in
    top-left relative screen coordinates

    Args:
        application: The AXUIElementRef representing the application that
            contains the screen coordinates (or the system-wide accessibility object)
        x: The horizontal position
        y: The vertical position

    Returns: the accessibility object at the position specified by x and y

    """
    err, element = AXUIElementCopyElementAtPosition(application, x, y, None)
    errors.check_ax_error(err, "Unable to get element at position")
    return element


def PAXUIElementSetMessagingTimeout(element, timeoutInSeconds):
    """
    Sets the timeout value used in the accessibility API

    Args:
        element: The AXUIElementRef representing an accessibility object
        timeoutInSeconds: The number of seconds for the new timeout value

    """
    err = AXUIElementSetMessagingTimeout(element, timeoutInSeconds)
    errors.check_ax_error(err, "The element reference is invalid")
