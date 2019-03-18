class SearchMethodsMixin(object):
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
