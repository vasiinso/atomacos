import atomacos


def test_wait_for_window_to_appear(finder_app):
    import threading

    def open_new_window():
        finder_app.menuItem("File", "New Finder Window").Press()

    new_window = threading.Thread(target=open_new_window)
    new_window.daemon = True
    new_window.start()

    window_appeared = finder_app.waitForWindowToAppear("*")
    assert window_appeared


def test_waitfor_notification_names(monkeypatch):
    sut = atomacos.NativeUIElement()
    monkeypatch.setattr(
        sut, "waitFor", lambda timeout, notification, **kwargs: notification
    )

    assert sut.waitForCreation() == "AXCreated"
    assert sut.waitForFocusToMatchCriteria() == "AXFocusedUIElementChanged"
    assert sut.waitForSheetToAppear() == "AXSheetCreated"
    assert sut.waitForValueToChange() == "AXValueChanged"
    assert sut.waitForWindowToAppear("name") == "AXWindowCreated"
    assert sut.waitForFocusedWindowToChange("name") == "AXFocusedWindowChanged"
    # assert sut.waitForWindowToDisappear('name') == "AXUIElementDestroyed"
    # assert sut.waitForFocusToChange(sut) == "AXFocusedUIElementChanged"
