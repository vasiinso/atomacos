from atomacos import AXCallbacks


class SearchMethodsMixin(object):
    def findFirst(self, **kwargs):
        """Return the first object that matches the criteria."""
        return self._findFirst(**kwargs)

    def findFirstR(self, **kwargs):
        """Search recursively for the first object that matches the
        criteria.
        """
        return self._findFirstR(**kwargs)

    def findAll(self, **kwargs):
        """Return a list of all children that match the specified criteria."""
        return self._findAll(**kwargs)

    def findAllR(self, **kwargs):
        """Return a list of all children (recursively) that match
        the specified criteria.
        """
        return self._findAllR(**kwargs)

    def _convenienceMatch(self, role, attr, match):
        """Method used by role based convenience functions to find a match"""
        kwargs = {}
        # If the user supplied some text to search for,
        # supply that in the kwargs
        if match:
            kwargs[attr] = match
        return self.findAll(AXRole=role, **kwargs)

    def _convenienceMatchR(self, role, attr, match):
        """Method used by role based convenience functions to find a match"""
        kwargs = {}
        # If the user supplied some text to search for,
        # supply that in the kwargs
        if match:
            kwargs[attr] = match
        return self.findAllR(AXRole=role, **kwargs)

    def textAreas(self, match=None):
        """Return a list of text areas with an optional match parameter."""
        return self._convenienceMatch("AXTextArea", "AXTitle", match)

    def textAreasR(self, match=None):
        """Return a list of text areas with an optional match parameter."""
        return self._convenienceMatchR("AXTextArea", "AXTitle", match)

    def textFields(self, match=None):
        """Return a list of textfields with an optional match parameter."""
        return self._convenienceMatch("AXTextField", "AXRoleDescription", match)

    def textFieldsR(self, match=None):
        """Return a list of textfields with an optional match parameter."""
        return self._convenienceMatchR("AXTextField", "AXRoleDescription", match)

    def buttons(self, match=None):
        """Return a list of buttons with an optional match parameter."""
        return self._convenienceMatch("AXButton", "AXTitle", match)

    def buttonsR(self, match=None):
        """Return a list of buttons with an optional match parameter."""
        return self._convenienceMatchR("AXButton", "AXTitle", match)

    def windows(self, match=None):
        """Return a list of windows with an optional match parameter."""
        return self._convenienceMatch("AXWindow", "AXTitle", match)

    def windowsR(self, match=None):
        """Return a list of windows with an optional match parameter."""
        return self._convenienceMatchR("AXWindow", "AXTitle", match)

    def sheets(self, match=None):
        """Return a list of sheets with an optional match parameter."""
        return self._convenienceMatch("AXSheet", "AXDescription", match)

    def sheetsR(self, match=None):
        """Return a list of sheets with an optional match parameter."""
        return self._convenienceMatchR("AXSheet", "AXDescription", match)

    def staticTexts(self, match=None):
        """Return a list of statictexts with an optional match parameter."""
        return self._convenienceMatch("AXStaticText", "AXValue", match)

    def staticTextsR(self, match=None):
        """Return a list of statictexts with an optional match parameter"""
        return self._convenienceMatchR("AXStaticText", "AXValue", match)

    def genericElements(self, match=None):
        """Return a list of genericelements with an optional match parameter."""
        return self._convenienceMatch("AXGenericElement", "AXValue", match)

    def genericElementsR(self, match=None):
        """Return a list of genericelements with an optional match parameter."""
        return self._convenienceMatchR("AXGenericElement", "AXValue", match)

    def groups(self, match=None):
        """Return a list of groups with an optional match parameter."""
        return self._convenienceMatch("AXGroup", "AXRoleDescription", match)

    def groupsR(self, match=None):
        """Return a list of groups with an optional match parameter."""
        return self._convenienceMatchR("AXGroup", "AXRoleDescription", match)

    def radioButtons(self, match=None):
        """Return a list of radio buttons with an optional match parameter."""
        return self._convenienceMatch("AXRadioButton", "AXTitle", match)

    def radioButtonsR(self, match=None):
        """Return a list of radio buttons with an optional match parameter."""
        return self._convenienceMatchR("AXRadioButton", "AXTitle", match)

    def popUpButtons(self, match=None):
        """Return a list of popup menus with an optional match parameter."""
        return self._convenienceMatch("AXPopUpButton", "AXTitle", match)

    def popUpButtonsR(self, match=None):
        """Return a list of popup menus with an optional match parameter."""
        return self._convenienceMatchR("AXPopUpButton", "AXTitle", match)

    def rows(self, match=None):
        """Return a list of rows with an optional match parameter."""
        return self._convenienceMatch("AXRow", "AXTitle", match)

    def rowsR(self, match=None):
        """Return a list of rows with an optional match parameter."""
        return self._convenienceMatchR("AXRow", "AXTitle", match)

    def sliders(self, match=None):
        """Return a list of sliders with an optional match parameter."""
        return self._convenienceMatch("AXSlider", "AXValue", match)

    def slidersR(self, match=None):
        """Return a list of sliders with an optional match parameter."""
        return self._convenienceMatchR("AXSlider", "AXValue", match)


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
