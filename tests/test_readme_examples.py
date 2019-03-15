import pytest
from atomacos import NativeUIElement
from atomacos.a11y import axenabled


@pytest.mark.skipif(not axenabled(), reason="Accessibility Permission Needed")
def test_basic_automator_app_ref(automator_app):
    assert isinstance(automator_app, NativeUIElement)


@pytest.mark.skipif(not axenabled(), reason="Accessibility Permission Needed")
def test_find_object(automator_app):
    window = automator_app.windows()[0]
    assert u"Untitled" in window.AXTitle


@pytest.mark.skipif(not axenabled(), reason="Accessibility Permission Needed")
def test_find_sheet_shortcut(automator_app):
    window = automator_app.windows()[0]
    sheet1 = window.sheets()[0]
    sheet2 = automator_app.sheetsR()[0]
    assert sheet1 == sheet2


@pytest.mark.skipif(not axenabled(), reason="Accessibility Permission Needed")
def test_search_method(automator_app):
    window = automator_app.windows()[0]
    sheet = window.sheets()[0]
    close = sheet.buttons("Close")[0]
    assert isinstance(close, NativeUIElement)


@pytest.mark.skipif(not axenabled(), reason="Accessibility Permission Needed")
def test_search_by_axattributes(automator_app):
    window = automator_app.windows()[0]
    sheet = window.sheets()[0]
    close = sheet.findFirst(AXRole="AXButton", AXTitle="Close")
    assert isinstance(close, NativeUIElement)


@pytest.mark.skipif(not axenabled(), reason="Accessibility Permission Needed")
def test_get_list_of_attributes(automator_app):
    window = automator_app.windows()[0]
    sheet = window.sheets()[0]
    close = sheet.findFirst(AXRole="AXButton", AXTitle="Close")
    assert len(close.getAttributes()) > 0


@pytest.mark.skipif(not axenabled(), reason="Accessibility Permission Needed")
def test_get_list_of_actions(automator_app):
    window = automator_app.windows()[0]
    sheet = window.sheets()[0]
    close = sheet.findFirst(AXRole="AXButton", AXTitle="Close")
    assert len(close.getActions()) > 0


@pytest.mark.skipif(not axenabled(), reason="Accessibility Permission Needed")
def test_perform_action(automator_app):
    window = automator_app.windows()[0]
    sheet = window.sheets()[0]
    close = sheet.findFirst(AXRole="AXButton", AXTitle="Close")
    close.Press()
