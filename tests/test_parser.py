import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from core.ct_model import CTModel
from core.controller import Controller


class MockViewer:
    def set_image(self, image):
        pass

    def set_bone_window(self):
        pass

    def set_soft_window(self):
        pass

    def set_sinus_window(self):
        pass

    def change_window(self, center_delta=0, width_delta=0):
        pass


def make_controller():
    volume = list(range(200))
    model = CTModel(volume)
    viewer = MockViewer()
    return Controller(model, viewer)


def test_parse_next():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("next"))
    assert parsed == {"action": "next", "value": 1}


def test_parse_next_five_word():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("next five"))
    assert parsed == {"action": "next", "value": 5}


def test_parse_next_ten_asr_mistake():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("next them"))
    assert parsed == {"action": "next", "value": 10}


def test_parse_previous_five():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("back five"))
    assert parsed == {"action": "previous", "value": 5}


def test_parse_slice_absolute():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("slice 120"))
    assert parsed == {"action": "slice", "value": 120}


def test_parse_first():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("first slice"))
    assert parsed == {"action": "first"}


def test_parse_last():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("last slice"))
    assert parsed == {"action": "last"}


def test_parse_middle():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("middle slice"))
    assert parsed == {"action": "middle"}


def test_parse_bone():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("bone"))
    assert parsed == {"action": "bone"}


def test_parse_soft():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("soft"))
    assert parsed == {"action": "soft"}


def test_parse_sinus():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("sinus"))
    assert parsed == {"action": "sinus"}


def test_parse_zoom_in():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("zoom in"))
    assert parsed == {"action": "zoom_in", "value": 1}


def test_parse_zoom_in_fast():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("zoom in a lot"))
    assert parsed == {"action": "zoom_in", "value": 2}


def test_parse_zoom_out():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("zoom out"))
    assert parsed == {"action": "zoom_out", "value": 1}


def test_parse_left():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("left"))
    assert parsed == {"action": "left"}


def test_parse_right():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("right"))
    assert parsed == {"action": "right"}


def test_parse_up():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("up"))
    assert parsed == {"action": "up"}


def test_parse_down():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("down"))
    assert parsed == {"action": "down"}


def test_parse_center():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("center"))
    assert parsed == {"action": "center"}


def test_parse_brighter():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("brighter"))
    assert parsed == {"action": "brighter"}


def test_parse_darker():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("darker"))
    assert parsed == {"action": "darker"}


def test_parse_contrast_up():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("contrast up"))
    assert parsed == {"action": "contrast_up"}


def test_parse_contrast_down():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("contrast down"))
    assert parsed == {"action": "contrast_down"}


def test_parse_unknown_command():
    controller = make_controller()
    parsed = controller.parse_command(controller.normalize_command("abracadabra"))
    assert parsed is None