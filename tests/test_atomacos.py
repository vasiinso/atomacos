from atomacos import errors
import pytest


class TestErrors:
    def test_error_message_in_exception(self):
        try:
            raise errors.AXErrorAPIDisabled("apple")
        except errors.AXError as e:
            assert "apple" in str(e)

    def test_set_known_code(self):
        with pytest.raises(errors.AXErrorAPIDisabled):
            errors.set_error(-25211, "test")
        with pytest.raises(errors.AXErrorInvalidUIElement):
            errors.set_error(-25202, "test")
        with pytest.raises(errors.AXErrorCannotComplete):
            errors.set_error(-25204, "test")
        with pytest.raises(errors.AXErrorNotImplemented):
            errors.set_error(-25208, "test")
