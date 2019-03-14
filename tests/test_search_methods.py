import atomacos


def test_convenienceMatch(monkeypatch):
    sut = atomacos.NativeUIElement()
    monkeypatch.setattr(sut, "_convenienceMatch", lambda *args: args)

    assert sut.textAreas(1) == ("AXTextArea", "AXTitle", 1)
    assert sut.textFields(3) == ("AXTextField", "AXRoleDescription", 3)
    assert sut.buttons("a") == ("AXButton", "AXTitle", "a")
    assert sut.windows() == ("AXWindow", "AXTitle", None)
    assert sut.sheets() == ("AXSheet", "AXDescription", None)
    assert sut.staticTexts() == ("AXStaticText", "AXValue", None)
    assert sut.genericElements() == ("AXGenericElement", "AXValue", None)
    assert sut.groups() == ("AXGroup", "AXRoleDescription", None)
    assert sut.radioButtons() == ("AXRadioButton", "AXTitle", None)
    assert sut.popUpButtons() == ("AXPopUpButton", "AXTitle", None)
    assert sut.rows() == ("AXRow", "AXTitle", None)
    assert sut.sliders() == ("AXSlider", "AXValue", None)


def test_recursive(monkeypatch):
    sut = atomacos.NativeUIElement()
    monkeypatch.setattr(sut, "_convenienceMatchR", lambda *args: args)

    assert sut.textAreasR(2) == ("AXTextArea", "AXTitle", 2)
    assert sut.textFieldsR(4) == ("AXTextField", "AXRoleDescription", 4)
    assert sut.buttonsR("a") == ("AXButton", "AXTitle", "a")
    assert sut.windowsR() == ("AXWindow", "AXTitle", None)
    assert sut.sheetsR() == ("AXSheet", "AXDescription", None)
    assert sut.staticTextsR() == ("AXStaticText", "AXValue", None)
    assert sut.genericElementsR() == ("AXGenericElement", "AXValue", None)
    assert sut.groupsR() == ("AXGroup", "AXRoleDescription", None)
    assert sut.radioButtonsR() == ("AXRadioButton", "AXTitle", None)
    assert sut.popUpButtonsR() == ("AXPopUpButton", "AXTitle", None)
    assert sut.rowsR() == ("AXRow", "AXTitle", None)
    assert sut.slidersR() == ("AXSlider", "AXValue", None)
