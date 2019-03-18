from atomacos import AXCallbacks


class WaitForMixin(object):
    def waitFor(self, timeout, notification, **kwargs):
        """Generic wait for a UI event that matches the specified
        criteria to occur.

        For customization of the callback, use keyword args labeled
        'callback', 'args', and 'kwargs' for the callback fn, callback args,
        and callback kwargs, respectively.  Also note that on return,
        the observer-returned UI element will be included in the first
        argument if 'args' are given.  Note also that if the UI element is
        destroyed, callback should not use it, otherwise the function will
        hang.
        """
        return self._waitFor(timeout, notification, **kwargs)

    def waitForCreation(self, timeout=10, notification="AXCreated"):
        """Convenience method to wait for creation of some UI element.

        Returns: The element created
        """
        callback = AXCallbacks.returnElemCallback
        retelem = None
        args = (retelem,)

        return self.waitFor(timeout, notification, callback=callback, args=args)

    def waitForWindowToAppear(self, winName, timeout=10):
        """Convenience method to wait for a window with the given name to
        appear.

        Returns: Boolean
        """
        return self.waitFor(timeout, "AXWindowCreated", AXTitle=winName)

    def waitForWindowToDisappear(self, winName, timeout=10):
        """Convenience method to wait for a window with the given name to
        disappear.

        Returns: Boolean
        """
        callback = AXCallbacks.elemDisappearedCallback
        retelem = None
        args = (retelem, self)

        # For some reason for the AXUIElementDestroyed notification to fire,
        # we need to have a reference to it first
        win = self.findFirst(AXRole="AXWindow", AXTitle=winName)  # noqa: F841
        return self.waitFor(
            timeout,
            "AXUIElementDestroyed",
            callback=callback,
            args=args,
            AXRole="AXWindow",
            AXTitle=winName,
        )

    def waitForSheetToAppear(self, timeout=10):
        """Convenience method to wait for a sheet to appear.

        Returns: the sheet that appeared (element) or None
        """
        return self.waitForCreation(timeout, "AXSheetCreated")

    def waitForValueToChange(self, timeout=10):
        """Convenience method to wait for value attribute of given element to
        change.

        Some types of elements (e.g. menu items) have their titles change,
        so this will not work for those.  This seems to work best if you set
        the notification at the application level.

        Returns: Element or None
        """
        # Want to identify that the element whose value changes matches this
        # object's.  Unique identifiers considered include role and position
        # This seems to work best if you set the notification at the application
        # level
        callback = AXCallbacks.returnElemCallback
        retelem = None
        return self.waitFor(
            timeout, "AXValueChanged", callback=callback, args=(retelem,)
        )

    def waitForFocusToChange(self, newFocusedElem, timeout=10):
        """Convenience method to wait for focused element to change (to new
        element given).

        Returns: Boolean
        """
        return self.waitFor(
            timeout,
            "AXFocusedUIElementChanged",
            AXRole=newFocusedElem.AXRole,
            AXPosition=newFocusedElem.AXPosition,
        )

    def waitForFocusedWindowToChange(self, nextWinName, timeout=10):
        """Convenience method to wait for focused window to change

        Returns: Boolean
        """
        return self.waitFor(timeout, "AXFocusedWindowChanged", AXTitle=nextWinName)

    def waitForFocusToMatchCriteria(self, timeout=10, **kwargs):
        """Convenience method to wait for focused element to change
        (to element matching kwargs criteria).

        Returns: Element or None

        """

        def _matchFocused(retelem, **kwargs):
            return retelem if retelem._match(**kwargs) else None

        retelem = None
        return self._waitFor(
            timeout,
            "AXFocusedUIElementChanged",
            callback=_matchFocused,
            args=(retelem,),
            **kwargs
        )
