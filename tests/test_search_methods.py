import atomacos


def test_search_method_for_roles(monkeypatch):
    sut = atomacos.NativeUIElement()
    monkeypatch.setattr(sut, "_findAll", lambda **kwargs: kwargs.items())

    assert ("AXRole", "AXTextField") in sut.textFields()
    assert ("AXRole", "AXButton") in sut.buttons()
    assert ("AXRole", "AXWindow") in sut.windows()
    assert ("AXRole", "AXSheet") in sut.sheets()
    assert ("AXRole", "AXStaticText") in sut.staticTexts()
    assert ("AXRole", "AXGenericElement") in sut.genericElements()
    assert ("AXRole", "AXGroup") in sut.groups()
    assert ("AXRole", "AXRadioButton") in sut.radioButtons()
    assert ("AXRole", "AXPopUpButton") in sut.popUpButtons()
    assert ("AXRole", "AXRow") in sut.rows()
    assert ("AXRole", "AXSlider") in sut.sliders()
    assert ("AXRole", "AXSlider") in sut.sliders()


def test_search_method_for_roles_recursive(monkeypatch):
    sut = atomacos.NativeUIElement()
    monkeypatch.setattr(sut, "_findAll", lambda **kwargs: kwargs.items())

    assert ("AXRole", "AXTextField") in sut.textFieldsR()
    assert ("AXRole", "AXButton") in sut.buttonsR()
    assert ("AXRole", "AXWindow") in sut.windowsR()
    assert ("AXRole", "AXSheet") in sut.sheetsR()
    assert ("AXRole", "AXStaticText") in sut.staticTextsR()
    assert ("AXRole", "AXGenericElement") in sut.genericElementsR()
    assert ("AXRole", "AXGroup") in sut.groupsR()
    assert ("AXRole", "AXRadioButton") in sut.radioButtonsR()
    assert ("AXRole", "AXPopUpButton") in sut.popUpButtonsR()
    assert ("AXRole", "AXRow") in sut.rowsR()
    assert ("AXRole", "AXSlider") in sut.slidersR()
    assert ("AXRole", "AXSlider") in sut.slidersR()


def test_search_extra_attributes(monkeypatch):
    sut = atomacos.NativeUIElement()
    monkeypatch.setattr(sut, "_findAll", lambda **kwargs: kwargs.items())

    assert ("AXRoleDescription", 1) in sut.textFields(1)
    assert ("AXTitle", 1) in sut.buttons(1)
    assert ("AXTitle", 1) in sut.windows(1)
    assert ("AXDescription", 1) in sut.sheets(1)
    assert ("AXValue", 1) in sut.staticTexts(1)
    assert ("AXValue", 1) in sut.genericElements(1)
    assert ("AXRoleDescription", 1) in sut.groups(1)
    assert ("AXTitle", 1) in sut.radioButtons(1)
    assert ("AXTitle", 1) in sut.popUpButtons(1)
    assert ("AXTitle", 1) in sut.rows(1)
    assert ("AXValue", 1) in sut.sliders(1)


def test_search_extra_attributes_recursive(monkeypatch):
    sut = atomacos.NativeUIElement()
    monkeypatch.setattr(sut, "_findAll", lambda **kwargs: kwargs.items())

    assert ("AXRoleDescription", 1) in sut.textFieldsR(1)
    assert ("AXTitle", 1) in sut.buttonsR(1)
    assert ("AXTitle", 1) in sut.windowsR(1)
    assert ("AXDescription", 1) in sut.sheetsR(1)
    assert ("AXValue", 1) in sut.staticTextsR(1)
    assert ("AXValue", 1) in sut.genericElementsR(1)
    assert ("AXRoleDescription", 1) in sut.groupsR(1)
    assert ("AXTitle", 1) in sut.radioButtonsR(1)
    assert ("AXTitle", 1) in sut.popUpButtonsR(1)
    assert ("AXTitle", 1) in sut.rowsR(1)
    assert ("AXValue", 1) in sut.slidersR(1)
