from atomacos import AXCallbacks


class SearchMethodsMixin(object):
    def _generateChildren(self, target=None, recursive=False):
        """Generator which yields all AXChildren of the object."""
        if target is None:
            target = self

        if "AXChildren" not in target.ax_attributes:
            return

        for child in target.AXChildren:
            yield child
            if recursive:
                for c in self._generateChildren(child, recursive):
                    yield c

    def _findAll(self, recursive=False, **kwargs):
        """Return a list of all children that match the specified criteria."""
        return filter(
            AXCallbacks.match_filter(**kwargs),
            self._generateChildren(recursive=recursive),
        )

    def _findFirst(self, recursive=False, **kwargs):
        """Return the first object that matches the criteria."""
        for item in self._findAll(recursive=recursive, **kwargs):
            return item

    def findFirst(self, **kwargs):
        """Return the first object that matches the criteria."""
        return self._findFirst(**kwargs)

    def findFirstR(self, **kwargs):
        """Search recursively for the first object that matches the
        criteria.
        """
        return self._findFirst(recursive=True, **kwargs)

    def findAll(self, **kwargs):
        """Return a list of all children that match the specified criteria."""
        return list(self._findAll(**kwargs))

    def findAllR(self, **kwargs):
        """Return a list of all children (recursively) that match
        the specified criteria.
        """
        return list(self._findAll(recursive=True, **kwargs))

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

    def _menuItem(self, menuitem, *args):
        """Return the specified menu item.

        Example - refer to items by name:

        app._menuItem(app.AXMenuBar, 'File', 'New').Press()
        app._menuItem(app.AXMenuBar, 'Edit', 'Insert', 'Line Break').Press()

        Refer to items by index:

        app._menuitem(app.AXMenuBar, 1, 0).Press()

        Refer to items by mix-n-match:

        app._menuitem(app.AXMenuBar, 1, 'About TextEdit').Press()
        """
        self._activate()
        for item in args:
            # If the item has an AXMenu as a child, navigate into it.
            # This seems like a silly abstraction added by apple's a11y api.
            if menuitem.AXChildren[0].AXRole == "AXMenu":
                menuitem = menuitem.AXChildren[0]
            # Find AXMenuBarItems and AXMenuItems using a handy wildcard
            try:
                menuitem = menuitem.AXChildren[int(item)]
            except ValueError:
                menuitem = menuitem.findFirst(AXRole="AXMenu*Item", AXTitle=item)
        return menuitem
