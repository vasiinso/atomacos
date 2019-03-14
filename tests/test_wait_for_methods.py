import atomacos


def test_waitfor_notification_names(monkeypatch):
    sut = atomacos.NativeUIElement()
    monkeypatch.setattr(
        sut, "_waitFor", lambda timeout, notification, **kwargs: notification
    )

    assert sut.waitForCreation() == "AXCreated"
    assert sut.waitForFocusToMatchCriteria() == "AXFocusedUIElementChanged"
    assert sut.waitForSheetToAppear() == "AXSheetCreated"
    assert sut.waitForValueToChange() == "AXValueChanged"
    assert sut.waitForWindowToAppear("name") == "AXWindowCreated"
    assert sut.waitForFocusedWindowToChange("name") == "AXFocusedWindowChanged"
    # assert sut.waitForWindowToDisappear('name') == "AXUIElementDestroyed"
    # assert sut.waitForFocusToChange(sut) == "AXFocusedUIElementChanged"
