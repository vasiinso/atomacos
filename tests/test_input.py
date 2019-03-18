import time


def calculate_center(size, position):
    center = (position.x + size.width / 2, position.y + size.height / 2)
    return center


def test_click_and_enter(finder_app):
    fields = finder_app.textFieldsR("*search*")
    field = fields[0]
    center_position = calculate_center(field.AXSize, field.AXPosition)
    field.clickMouseButtonLeft(center_position)
    field.sendKeys("hello")
    time.sleep(1)
    assert field.AXValue == "hello"
