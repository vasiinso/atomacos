from atomacos import Prefs
from future.utils import string_types


def test_prefs():
    fp = Prefs("com.apple.finder")
    assert isinstance(fp["GoToField"], string_types)
