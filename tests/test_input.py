import subprocess
import time


def calculate_center(size, position):
    center = (position.x + size.width / 2, position.y + size.height / 2)
    return center


def test_types(finder_app):
    fields = finder_app.textFieldsR("*search*")
    field = fields[0]
    center_position = calculate_center(field.AXSize, field.AXPosition)
    field.clickMouseButtonLeft(center_position)
    field.sendKeys("hello")
    time.sleep(1)
    assert field.AXValue == "hello"
    field.sendKey("!")
    assert field.AXValue == "hello!"
    field.sendKeyWithModifiers("a", ["shift"])
    assert field.AXValue == "hello!A"
    field.sendGlobalKey("@")
    assert field.AXValue == "hello!A@"
    field.sendGlobalKeyWithModifiers("b", ["shift"])
    assert field.AXValue == "hello!A@B"


def test_clicks(finder_app):
    fields = finder_app.textFieldsR("*search*")
    field = fields[0]
    center_position = calculate_center(field.AXSize, field.AXPosition)
    field.clickMouseButtonLeft(center_position)
    field.sendKeys("hey there world")
    field.doubleClickMouse(center_position)
    selected_text = field.AXSelectedText
    assert len(selected_text.split()) == 1
    field.tripleClickMouse(center_position)
    selected_text = field.AXSelectedText
    assert len(selected_text.split()) > 1


def test_drag_folders(finder_app):
    test_path = "~/Desktop/test_input"

    subprocess.call("rm -rf {}".format(test_path), shell=True)
    subprocess.call("mkdir {}".format(test_path), shell=True)

    finder_app.sendKeyWithModifiers("g", modifiers=["command", "shift"])

    end_time = time.time() + 10
    while (
        not finder_app.findFirstR(AXRole="AXButton", AXTitle="Go")
        and time.time() < end_time
    ):
        time.sleep(0.1)

    finder_app.sendKeys(test_path + "\n")

    while (
        finder_app.findFirstR(AXRole="AXButton", AXTitle="Go")
        and time.time() < end_time
    ):
        time.sleep(0.1)

    finder_app.sendKeyWithModifiers("n", modifiers=["command", "shift"])
    finder_app.sendKeys("helloworld\n")

    finder_app.sendKeyWithModifiers("n", modifiers=["command", "shift"])
    finder_app.sendKeys("helloworld2\n")

    file1 = finder_app.findFirstR(AXFilename="helloworld")
    file2 = finder_app.findFirstR(AXFilename="helloworld2")

    def center_position(ref):
        pos = ref.AXPosition
        size = ref.AXSize
        return pos.x + size.width / 2, pos.y + size.height / 2

    finder_app.dragMouseButtonLeft(center_position(file2), center_position(file1))

    output = subprocess.check_output(
        "ls {}/helloworld".format(test_path), shell=True, universal_newlines=True
    )
    assert "helloworld2" in output
