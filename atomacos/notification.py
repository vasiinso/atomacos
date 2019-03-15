import logging
import signal

import objc
from ApplicationServices import (
    AXObserverCreate,
    AXObserverGetRunLoopSource,
    NSDefaultRunLoopMode,
)
from atomacos._objc_ax import (
    PAXObserverAddNotification,
    PAXObserverCreate,
    PAXObserverRemoveNotification,
)
from CoreFoundation import CFRunLoopAddSource, CFRunLoopGetCurrent
from PyObjCTools import AppHelper

try:
    from PyObjCTools import MachSignals
except ImportError:

    class MachSignals:
        signal = signal.signal


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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
        else:
            self.callbackKwargs = dict()

        self.callback_result = None
        self.timedout = True

        @objc.callbackFor(AXObserverCreate)
        def _observer_callback(observer, element, notification, refcon):
            if self.callbackFn is not None:
                ret_element = self.ref.__class__(element)
                if ret_element is None:
                    raise RuntimeError("Could not create new AX UI Element.")
                callback_args = (ret_element,) + self.callbackArgs
                callback_result = self.callbackFn(*callback_args, **self.callbackKwargs)
                if callback_result is None:
                    raise RuntimeError("Python callback failed.")
                if callback_result in (-1, 1):
                    self.timedout = False
                    AppHelper.stopEventLoop()

                self.callback_result = callback_result
            else:
                self.timedout = False
                AppHelper.stopEventLoop()

        observer = PAXObserverCreate(self.ref.pid, _observer_callback)

        PAXObserverAddNotification(
            observer, self.ref.ref, notification_name, id(self.ref.ref)
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

        PAXObserverRemoveNotification(observer, self.ref.ref, notification_name)

        return self.callback_result
