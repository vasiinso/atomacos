from atomacos import errors, converter, a11y
import pytest


class TestErrors:
    def test_error_message_in_exception(self):
        try:
            raise errors.AXErrorAPIDisabled("apple")
        except errors.AXError as e:
            assert "apple" in str(e)

    def test_set_known_code(self):
        with pytest.raises(errors.AXErrorAPIDisabled):
            errors.raise_ax_error(-25211, "test")
        with pytest.raises(errors.AXErrorInvalidUIElement):
            errors.raise_ax_error(-25202, "test")
        with pytest.raises(errors.AXErrorCannotComplete):
            errors.raise_ax_error(-25204, "test")
        with pytest.raises(errors.AXErrorNotImplemented):
            errors.raise_ax_error(-25208, "test")


class TestToPythonConversion:
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

    def test_convert_boolean(self):
        from CoreFoundation import kCFBooleanTrue, kCFBooleanFalse

        result1 = converter.convert_value(kCFBooleanTrue)
        result2 = converter.convert_value(kCFBooleanFalse)

        assert isinstance(result1, bool)
        assert isinstance(result2, bool)
        assert result1 is True
        assert result2 is False

    def test_convert_array(self):
        from CoreFoundation import CFArrayCreate, kCFTypeArrayCallBacks

        array = CFArrayCreate(None, [1, 2, 3, 4], 4, kCFTypeArrayCallBacks)
        result = converter.convert_value(array)
        assert isinstance(result, list)
        assert result == [1, 2, 3, 4]

    def test_convert_number_int(self):
        from CoreFoundation import CFNumberCreate, kCFNumberIntType

        num = CFNumberCreate(None, kCFNumberIntType, 1.5)
        result = converter.convert_value(num)
        assert result == 1
        assert isinstance(result, int)

    def test_convert_number_double(self):
        from CoreFoundation import CFNumberCreate, kCFNumberDoubleType

        num = CFNumberCreate(None, kCFNumberDoubleType, 1.5)
        result = converter.convert_value(num)
        assert result == 1.5
        assert isinstance(result, float)


class TestHelpers:
    def test_get_frontmost_pid(self):
        pid = a11y.get_frontmost_pid()
        assert isinstance(pid, int)
        assert pid > 0

    def test_axenabled(self):
        assert isinstance(a11y.axenabled(), bool)


@pytest.fixture
def frontmost_app():
    pid = a11y.get_frontmost_pid()
    app_ref = a11y.AXUIElement.from_pid(pid)
    return app_ref


@pytest.fixture
def front_title_ui(frontmost_app):
    return frontmost_app.AXWindows[0].AXTitleUIElement


class TestAXUIElement:
    def test_init(self):
        a11y.AXUIElement()

    def test_app_ref_from_pid(self):
        pid = a11y.get_frontmost_pid()
        app_ref = a11y.AXUIElement.from_pid(pid)
        assert "Application" in str(app_ref.ref)

    def test_app_ref_from_system_object(self):
        app_ref = a11y.AXUIElement.systemwide()
        assert "System Wide" in str(app_ref.ref)

    def test_get_ax_attributes(self, frontmost_app):
        sut = frontmost_app.ax_attributes
        assert isinstance(sut, list)
        assert "AXRole" in sut
        assert "AXWindows" in sut
        assert "AXChildren" in sut

    def test_get_ax_actions(self, frontmost_app):
        sut = frontmost_app.ax_actions
        assert isinstance(sut, list)

    def test_basic_get_attr(self, frontmost_app):
        assert isinstance(frontmost_app.AXTitle, str)
        assert isinstance(frontmost_app.AXWindows, list)

    def test_dir_has_ref(self, frontmost_app):
        assert "ref" in dir(frontmost_app)
        assert "AXTitle" in dir(frontmost_app)

    def test_get_pid(self):
        pid = a11y.get_frontmost_pid()
        app_ref = a11y.AXUIElement.from_pid(pid)
        assert app_ref.pid == pid

    def test_eq(self):
        pid = a11y.get_frontmost_pid()
        app_ref1 = a11y.AXUIElement.from_pid(pid)
        app_ref2 = a11y.AXUIElement.from_pid(pid)
        assert app_ref1 == app_ref2

    def test_ne(self):
        pid = a11y.get_frontmost_pid()
        app_ref1 = a11y.AXUIElement.from_pid(pid)
        app_ref2 = a11y.AXUIElement.systemwide()
        assert app_ref1 != app_ref2

    def test_list_returns_pyobj(self, frontmost_app):
        window = frontmost_app.AXWindows[0]
        assert isinstance(window, a11y.AXUIElement)

    def test_get_child_uielement(self, frontmost_app):
        window = frontmost_app.AXWindows[0]
        assert isinstance(window, a11y.AXUIElement)

    def test_convert_ax_size(self, front_title_ui):
        size = front_title_ui.AXSize
        assert isinstance(size, tuple)
        assert isinstance(size[0], float)
        assert isinstance(size[1], float)

    def test_size_namedtuple(self, front_title_ui):
        size = front_title_ui.AXSize
        assert isinstance(size.width, float)
        assert isinstance(size.height, float)

    def test_convert_ax_point(self, front_title_ui):
        point = front_title_ui.AXPosition
        assert isinstance(point, tuple)
        assert isinstance(point[0], float)
        assert isinstance(point[1], float)

    def test_point_namedtuple(self, front_title_ui):
        point = front_title_ui.AXPosition
        assert isinstance(point.x, float)
        assert isinstance(point.y, float)

    def test_convert_ax_range(self, front_title_ui):
        range = front_title_ui.AXVisibleCharacterRange
        assert isinstance(range, tuple)
        assert isinstance(range[0], int)
        assert isinstance(range[1], int)

    def test_range_namedtuple(self, front_title_ui):
        range = front_title_ui.AXVisibleCharacterRange
        assert isinstance(range.location, int)
        assert isinstance(range.length, int)
