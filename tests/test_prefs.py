from atomacos import Prefs


def test_prefs():
    fp = Prefs("com.apple.finder")
    assert isinstance(fp["GoToField"], str)
