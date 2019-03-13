import atomacos as atomac


def test_launch_app_by_bundle_id():
    atomac.launchAppByBundleId("com.apple.Automator")


def test_get_app_ref_by_bundle_id():
    atomac.launchAppByBundleId("com.apple.Automator")
    automator = atomac.getAppRefByBundleId("com.apple.Automator")
    assert isinstance(automator, atomac.NativeUIElement)


def test_find_object():
    atomac.launchAppByBundleId("com.apple.Automator")
    automator = atomac.getAppRefByBundleId("com.apple.Automator")
    window = automator.windows()[0]
    assert window.AXTitle == u"Untitled"


def test_find_sheet_shortcut():
    atomac.launchAppByBundleId("com.apple.Automator")
    automator = atomac.getAppRefByBundleId("com.apple.Automator")
    window = automator.windows()[0]
    sheet1 = window.sheets()[0]
    sheet2 = automator.sheetsR()[0]
    assert sheet1 == sheet2


def test_search_method():
    atomac.launchAppByBundleId("com.apple.Automator")
    automator = atomac.getAppRefByBundleId("com.apple.Automator")
    window = automator.windows()[0]
    sheet = window.sheets()[0]
    close = sheet.buttons("Close")[0]
    assert isinstance(close, atomac.NativeUIElement)


def test_search_by_axattributes():
    atomac.launchAppByBundleId("com.apple.Automator")
    automator = atomac.getAppRefByBundleId("com.apple.Automator")
    window = automator.windows()[0]
    sheet = window.sheets()[0]
    close = sheet.findFirst(AXRole="AXButton", AXTitle="Close")
    assert isinstance(close, atomac.NativeUIElement)


def test_get_list_of_attributes():
    atomac.launchAppByBundleId("com.apple.Automator")
    automator = atomac.getAppRefByBundleId("com.apple.Automator")
    close = automator.findFirstR(AXRole="AXButton", AXTitle="Close")
    assert len(close.getAttributes()) > 0


def test_get_list_of_acctions():
    atomac.launchAppByBundleId("com.apple.Automator")
    automator = atomac.getAppRefByBundleId("com.apple.Automator")
    close = automator.findFirstR(AXRole="AXButton", AXTitle="Close")
    assert len(close.getActions()) > 0


def test_perform_action():
    atomac.launchAppByBundleId("com.apple.Automator")
    automator = atomac.getAppRefByBundleId("com.apple.Automator")
    close = automator.findFirstR(AXRole="AXButton", AXTitle="Close")
    close.Press()
