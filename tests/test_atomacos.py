from atomacos import errors, converter
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


class TestValueConversions:
    def test_convert_string(self):
        from CoreFoundation import (
            CFStringCreateWithCString,
            kCFStringEncodingASCII,
        )

        sut = CFStringCreateWithCString(None, b"hello", kCFStringEncodingASCII)
        result = converter.convert_value(sut)
        assert isinstance(result, str)
        assert result == "hello"

        sut = CFStringCreateWithCString(None, b"world", kCFStringEncodingASCII)
        result = converter.convert_value(sut)
        assert isinstance(result, str)
        assert result == "world"
