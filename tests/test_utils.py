# -*- coding: utf-8 -*-
import pytest
from atomacos import _a11y, errors


class TestErrors:
    def test_error_message_in_exception(self):
        try:
            raise errors.AXErrorAPIDisabled("apple")
        except errors.AXError as e:
            assert "apple" in str(e)

    def test_check_error_success(self):
        errors.check_ax_error(errors.kAXErrorSuccess, {})

    def test_check_error_raises(self):
        with pytest.raises(errors.AXErrorInvalidUIElement):
            errors.check_ax_error(errors.kAXErrorInvalidUIElement, {})

    def test_check_error_message(self):
        error_messages = {errors.kAXErrorInvalidUIElement: "pass"}
        try:
            errors.check_ax_error(errors.kAXErrorInvalidUIElement, error_messages)
        except errors.AXError as e:
            assert "pass" in str(e)


class TestHelpers:
    def test_get_frontmost_pid(self):
        pid = _a11y.get_frontmost_pid()
        assert isinstance(pid, int)
        assert pid > 0

    def test_axenabled(self):
        assert isinstance(_a11y.axenabled(), bool)


class TestToPythonConversion:
    def test_convert_string(self, axconverter):
        from CoreFoundation import CFStringCreateWithCString, kCFStringEncodingASCII

        sut = CFStringCreateWithCString(None, b"hello", kCFStringEncodingASCII)
        result = axconverter.convert_value(sut)
        assert isinstance(result, str)
        assert result == "hello"

        sut = CFStringCreateWithCString(None, b"world", kCFStringEncodingASCII)
        result = axconverter.convert_value(sut)
        assert isinstance(result, str)
        assert result == "world"

    def test_convert_unicode(self, axconverter):
        from future.utils import string_types
        from CoreFoundation import CFStringCreateWithCharacters

        sut = CFStringCreateWithCharacters(None, u"€10", 3)
        result = axconverter.convert_value(sut)
        print(result)
        assert isinstance(result, string_types)

    def test_convert_boolean(self, axconverter):
        from CoreFoundation import kCFBooleanTrue, kCFBooleanFalse

        result1 = axconverter.convert_value(kCFBooleanTrue)
        result2 = axconverter.convert_value(kCFBooleanFalse)

        assert isinstance(result1, bool)
        assert isinstance(result2, bool)
        assert result1 is True
        assert result2 is False

    def test_convert_array(self, axconverter):
        from CoreFoundation import CFArrayCreate, kCFTypeArrayCallBacks

        array = CFArrayCreate(None, [1, 2, 3, 4], 4, kCFTypeArrayCallBacks)
        result = axconverter.convert_value(array)
        assert isinstance(result, list)
        assert result == [1, 2, 3, 4]

    def test_convert_number_int(self, axconverter):
        from CoreFoundation import CFNumberCreate, kCFNumberIntType

        num = CFNumberCreate(None, kCFNumberIntType, 1.5)
        result = axconverter.convert_value(num)
        assert result == 1
        assert isinstance(result, int)

    def test_convert_number_double(self, axconverter):
        from CoreFoundation import CFNumberCreate, kCFNumberDoubleType

        num = CFNumberCreate(None, kCFNumberDoubleType, 1.5)
        result = axconverter.convert_value(num)
        assert result == 1.5
        assert isinstance(result, float)
