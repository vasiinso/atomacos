import atomacos
import pytest


def test_get_app_ref_by_localized_name(finder_app):
    finder = atomacos.getAppRefByLocalizedName("Finder")
    assert finder == finder_app


def test_get_bad_localized_name():
    with pytest.raises(ValueError):
        atomacos.getAppRefByLocalizedName("Bad Localized Name")


def test_launch_app_by_bundle_path():
    atomacos.launchAppByBundlePath("/Applications/Calculator.app")
    automator = atomacos.getAppRefByLocalizedName("Calculator")
    assert automator.pid != 0


def test_set_systemwide_timeout():
    atomacos.setSystemWideTimeout(0)


def test_get_app_by_bundle_id(finder_app):
    bid = finder_app.getBundleId()
    bybid = atomacos.getAppRefByBundleId(bid)
    assert bybid == finder_app


def test_bad_bundle_id():
    with pytest.raises(ValueError):
        atomacos.getAppRefByBundleId("bad.bundle.id")


def test_get_app_by_pid(finder_app):
    pid = finder_app.pid
    app = atomacos.getAppRefByPid(pid)
    assert app == finder_app
