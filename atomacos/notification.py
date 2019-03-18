import logging
import signal
import threading
import time

from ApplicationServices import AXObserverGetRunLoopSource, NSDefaultRunLoopMode
from atomacos._macos import (
    PAXObserverAddNotification,
    PAXObserverCallback,
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

        @PAXObserverCallback
        def _callback(observer, element, notification, refcon):
            if self.callbackFn is not None:
                ret_element = self.ref.__class__(element)
                if ret_element is None:
                    raise RuntimeError("Could not create new AX UI Element.")
                callback_args = (ret_element,) + self.callbackArgs
                callback_result = self.callbackFn(*callback_args, **self.callbackKwargs)
                if callback_result is None:
                    raise RuntimeError("Python callback failed.")
                if callback_result in (-1, 1):
                    self.callback_result = callback_result

        observer = PAXObserverCreate(self.ref.pid, _callback)

        PAXObserverAddNotification(
            observer, self.ref.ref, notification_name, id(self.ref.ref)
        )
        # Add observer source to run loop
        CFRunLoopAddSource(
            CFRunLoopGetCurrent(),
            AXObserverGetRunLoopSource(observer),
            NSDefaultRunLoopMode,
        )

        def event_stopper():
            end_time = time.time() + timeout
            while time.time() < end_time:
                if self.callback_result is not None:
                    break
            AppHelper.callAfter(AppHelper.stopEventLoop)

        event_watcher = threading.Thread(target=event_stopper)
        event_watcher.daemon = True
        event_watcher.start()

        # Set the signal handlers prior to running the run loop
        oldSigIntHandler = MachSignals.signal(signal.SIGINT, _sigHandler)
        AppHelper.runConsoleEventLoop()
        MachSignals.signal(signal.SIGINT, oldSigIntHandler)

        PAXObserverRemoveNotification(observer, self.ref.ref, notification_name)

        return self.callback_result
