import os
import subprocess
import time

import atomacos
import pytest
from atomacos import _converter


def pytest_exception_interact(node, call, report):
    if os.getenv("CI", False):
        filename = "{}.png".format(node.name)
        subprocess.call("screencapture .env/{}".format(filename), shell=True)
        subprocess.call(".env/imgur.sh/imgur.sh .env/{}".format(filename), shell=True)
        subprocess.call("rm .env/{}".format(filename), shell=True)

        print("Printing all elements")
        for app in atomacos.NativeUIElement.getRunningApps():
            pid = app.processIdentifier()
            app_ref = atomacos.NativeUIElement.from_pid(pid)
            print("\n%s" % app_ref)
            for child in app_ref._generateChildren(recursive=True):
                print("%s" % child)
                for attribute in child.ax_attributes:
                    if attribute == "AXChildren":
                        continue
                    try:
                        print({attribute: child._get_ax_attribute(attribute)})
                    except atomacos.errors.AXError as e:
                        print("Issue getting %s: %s" % (attribute, e))


def app_by_bid(bid):
    running_apps = list(atomacos.NativeUIElement.getRunningApps())
    if not any([bid in str(app) for app in running_apps]):
        atomacos.launchAppByBundleId(bid)
    app = atomacos.NativeUIElement.from_bundle_id(bid)
    while not app.windowsR():
        time.sleep(1)
        if not app.windowsR():
            app.menuItem("File", "New*").Press()
        else:
            break
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
    app.activate()
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
    return _converter.Converter(atomacos.NativeUIElement)
