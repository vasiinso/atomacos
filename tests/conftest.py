import time

import pytest

import atomacos
from atomacos import converter


def app_by_bid(bid):
    running_apps = list(atomacos.NativeUIElement._getRunningApps())
    if not any([bid in str(app) for app in running_apps]):
        atomacos.launchAppByBundleId(bid)
    app = atomacos.NativeUIElement.from_bundle_id(bid)
    while len(app.windowsR()) == 0:
        time.sleep(1)
        app.menuItem("File", "New*").Press()
        time.sleep(1)
    return app


@pytest.fixture(scope="module")
def automator_app():
    bid = "com.apple.Automator"
    app = app_by_bid(bid)
    yield app
    app.terminateAppByBundleId(bid)


@pytest.fixture(scope="module")
def finder_app():
    bid = "com.apple.finder"
    app = app_by_bid(bid)
    yield app
    app.terminateAppByBundleId(bid)


@pytest.fixture
def frontmost_app(finder_app):
    finder_app.activate()
    return finder_app


@pytest.fixture
def front_title_ui(frontmost_app):
    return frontmost_app.findFirstR(AXRole="AXStaticText")


@pytest.fixture
def axconverter():
    return converter.Converter(atomacos.NativeUIElement)
