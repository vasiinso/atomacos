import functools
import logging
import signal

import objc
from ApplicationServices import (
    AXObserverCreate,
    AXObserverGetRunLoopSource,
    AXObserverRemoveNotification,
    AXObserverAddNotification,
    kAXErrorSuccess,
    NSDefaultRunLoopMode,
)
from CoreFoundation import CFRunLoopGetCurrent, CFRunLoopAddSource
from PyObjCTools import AppHelper, MachSignals

from atomacos import errors

logger = logging.getLogger(__name__)


def _sigHandler(sig):
    AppHelper.stopEventLoop()
    raise KeyboardInterrupt("Keyboard interrupted Run Loop")


class Observer:
    def __init__(self, uielement=None):
        self.ref = uielement
        self.callback = None
        self.callback_result = None

    def set_notification(
        self,
        timeout=0,
        notification_name=None,
        callbackFn=None,
        callbackArgs=None,
        callbackKwargs=None,
    ):
        if callable(callbackFn):
            self.callbackFn = callbackFn

        if isinstance(callbackArgs, tuple):
            self.callbackArgs = callbackArgs
        else:
            self.callbackArgs = tuple()

        if isinstance(callbackKwargs, dict):
            self.callbackKwargs = callbackKwargs

        self.callback = functools.partial(
            callbackFn, callbackArgs, callbackKwargs
        )
        self.callback_result = None
        self.timedout = True

        @objc.callbackFor(AXObserverCreate)
        def _observer_callback(observer, element, notification, refcon):
            logger.debug("observer: %s" % observer)
            logger.debug("element: %s" % element)
            logger.debug("notification: %s" % notification)
            logger.debug("refcon: %s" % refcon)
            self.callback_result = self.callback()
            self.timedout = False
            AppHelper.stopEventLoop()

        err, observer = AXObserverCreate(
            self.ref.pid, _observer_callback, None
        )
        if err != kAXErrorSuccess:
            errors.raise_ax_error(
                err, "Could not create observer for notification"
            )

        err = AXObserverAddNotification(
            observer, self.ref.ref, notification_name, id(self.ref.ref)
        )
        if err != kAXErrorSuccess:
            errors.raise_ax_error(
                err, "Could not add notification to observer"
            )
        # Add observer source to run loop
        CFRunLoopAddSource(
            CFRunLoopGetCurrent(),
            AXObserverGetRunLoopSource(observer),
            NSDefaultRunLoopMode,
        )

        # Set the signal handlers prior to running the run loop
        oldSigIntHandler = MachSignals.signal(signal.SIGINT, _sigHandler)
        AppHelper.callLater(timeout, AppHelper.stopEventLoop)
        AppHelper.runConsoleEventLoop()
        MachSignals.signal(signal.SIGINT, oldSigIntHandler)

        err = AXObserverRemoveNotification(
            observer, self.ref.ref, notification_name
        )
        if err != kAXErrorSuccess:
            errors.raise_ax_error(
                err, "Could not remove notification from observer"
            )

        return self.callback_result
