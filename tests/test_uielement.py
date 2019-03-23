from atomacos import NativeUIElement


def test_uielement_repr_no_ref():
    sut = NativeUIElement()
    assert "role" in repr(sut)


def test_uielement_repr_finder(finder_app):
    assert "Finder" in repr(finder_app)


def test_get_localized_name(finder_app):
    assert finder_app.getLocalizedName() == "Finder"
