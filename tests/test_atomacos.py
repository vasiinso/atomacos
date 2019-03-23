import pytest
from atomacos import (
    NativeUIElement,
    a11y,
    getAppRefByPid,
    getFrontmostApp,
    notification,
)


@pytest.mark.skipif(not a11y.axenabled(), reason="Accessibility Permission Needed")
class TestAXUIElement:
    def test_init(self):
        NativeUIElement()

    def test_app_ref_from_pid(self):
        pid = a11y.get_frontmost_pid()
        app_ref = NativeUIElement.getAppRefByPid(pid)
        assert "Application" in str(app_ref.ref)

    def test_app_ref_from_system_object(self):
        app_ref = NativeUIElement.getSystemObject()
        assert "System Wide" in str(app_ref.ref)

    def test_app_with_windows(self):
        sut = NativeUIElement.getAnyAppWithWindow()
        assert len(sut.windows()) > 0

    def test_get_ax_attributes(self, frontmost_app):
        sut = frontmost_app.ax_attributes
        assert isinstance(sut, list)
        assert "AXRole" in sut
        assert "AXWindows" in sut
        assert "AXChildren" in sut

    def test_get_ax_actions(self, frontmost_app):
        main_window = frontmost_app.AXMainWindow
        sut = main_window.ax_actions
        assert isinstance(sut, list)
        assert "AXRaise" in sut

    @pytest.mark.slow
    @pytest.mark.skipif(not a11y.axenabled(), reason="Accessibility Permission Needed")
    def test_perform_ax_action(self, frontmost_app):
        main_window = frontmost_app.AXMainWindow
        main_window.Raise()

    def test_basic_get_attr(self, frontmost_app):
        assert isinstance(frontmost_app.AXTitle, str)
        assert isinstance(frontmost_app.AXWindows, list)

    def test_dir_has_ref(self, frontmost_app):
        assert "ref" in dir(frontmost_app)
        assert "AXTitle" in dir(frontmost_app)

    def test_get_pid(self):
        pid = a11y.get_frontmost_pid()
        app_ref = getAppRefByPid(pid)
        assert app_ref.pid == pid

    def test_get_bad_pid(self):
        bad_pid = 90909
        assert "<No role!>" in str(getAppRefByPid(bad_pid))

    def test_eq(self):
        app_ref1 = getFrontmostApp()
        app_ref2 = getAppRefByPid(app_ref1.pid)
        app_ref3 = NativeUIElement()
        assert app_ref1 == app_ref2
        assert app_ref1 != app_ref3
        assert app_ref3 == app_ref3
        assert app_ref3 != 3

    def test_ne(self):
        app_ref1 = getFrontmostApp()
        app_ref2 = NativeUIElement.getSystemObject()
        assert app_ref1 != app_ref2

    def test_list_returns_pyobj(self, frontmost_app):
        window = frontmost_app.AXWindows[0]
        assert isinstance(window, NativeUIElement)

    def test_get_child_uielement(self, frontmost_app):
        window = frontmost_app.AXWindows[0]
        assert isinstance(window, NativeUIElement)

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

    def test_element_at_current_position(self, front_title_ui):
        system_ref = front_title_ui.systemwide()
        position = front_title_ui.AXPosition
        size = front_title_ui.AXSize
        center_x, center_y = (
            position.x + size.width / 2.0,
            position.y + size.height / 2.0,
        )
        element_at_position = system_ref.get_element_at_position(center_x, center_y)
        assert element_at_position == front_title_ui

    def test_get_empty_field(self, finder_app):
        search = finder_app.textFieldsR("*search*")[0]
        assert search.AXValue is None

    def test_set_string(self, finder_app):
        search = finder_app.textFieldsR("*search*")[0]
        search.setString("AXValue", "test")
        assert search.AXValue == "test"


@pytest.mark.skipif(not a11y.axenabled(), reason="Accessibility Permission Needed")
class TestObserver:
    def test_observer_init(self, front_title_ui):
        notification.Observer(front_title_ui)

    @pytest.mark.slow
    def test_observer_wait_for(self, monkeypatch, finder_app):
        import threading
        from ApplicationServices import kAXWindowCreatedNotification

        def open_new_window():
            finder_app.menuItem("File", "New Finder Window").Press()

        new_window = threading.Thread(target=open_new_window)
        new_window.daemon = True
        new_window.start()

        observer = notification.Observer(finder_app)
        result = observer.wait_for(
            timeout=10,
            notification=kAXWindowCreatedNotification,
            filter_=lambda _: True,
        )

        assert isinstance(result, NativeUIElement)
