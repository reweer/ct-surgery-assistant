import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from core.ct_model import CTModel
from core.controller import Controller


class MockViewer:
    def __init__(self):
        self.window_mode = None
        self.center_delta = 0
        self.width_delta = 0

    def set_image(self, image):
        pass

    def set_bone_window(self):
        self.window_mode = "bone"

    def set_soft_window(self):
        self.window_mode = "soft"

    def set_sinus_window(self):
        self.window_mode = "sinus"

    def change_window(self, center_delta=0, width_delta=0):
        self.center_delta += center_delta
        self.width_delta += width_delta


def make_controller():
    volume = list(range(200))
    model = CTModel(volume)
    viewer = MockViewer()
    controller = Controller(model, viewer)
    return controller, model, viewer


def test_handle_voice_next_five():
    controller, model, viewer = make_controller()

    start = model.get_current_index()
    changed = controller.handle_voice("next five")

    assert changed is True
    assert model.get_current_index() == start + 5


def test_handle_voice_back_ten_asr_alias():
    controller, model, viewer = make_controller()

    start = model.get_current_index()
    changed = controller.handle_voice("burton")

    assert changed is True
    assert model.get_current_index() == start - 10


def test_handle_voice_slice_absolute():
    controller, model, viewer = make_controller()

    changed = controller.handle_voice("slice 20")

    assert changed is True
    assert model.get_current_index() == 19


def test_handle_voice_first_last_middle():
    controller, model, viewer = make_controller()

    assert controller.handle_voice("first slice") is True
    assert model.get_current_index() == 0

    assert controller.handle_voice("last slice") is True
    assert model.get_current_index() == 199

    assert controller.handle_voice("middle slice") is True
    assert model.get_current_index() == 100


def test_handle_voice_bone_soft_sinus():
    controller, model, viewer = make_controller()

    assert controller.handle_voice("bone") is True
    assert viewer.window_mode == "bone"

    assert controller.handle_voice("soft") is True
    assert viewer.window_mode == "soft"

    assert controller.handle_voice("sinus") is True
    assert viewer.window_mode == "sinus"


def test_handle_voice_zoom_in_and_out():
    controller, model, viewer = make_controller()

    start_zoom = controller.zoom

    assert controller.handle_voice("zoom in") is True
    assert controller.zoom > start_zoom

    zoom_after_in = controller.zoom

    assert controller.handle_voice("zoom out") is True
    assert controller.zoom < zoom_after_in


def test_handle_voice_pan_and_center():
    controller, model, viewer = make_controller()

    assert controller.handle_voice("left") is True
    assert controller.offset_x > 0

    assert controller.handle_voice("up") is True
    assert controller.offset_y > 0

    assert controller.handle_voice("center") is True
    assert controller.zoom == 1.0
    assert controller.offset_x == 0
    assert controller.offset_y == 0


def test_handle_voice_brighter_and_contrast():
    controller, model, viewer = make_controller()

    assert controller.handle_voice("brighter") is True
    assert viewer.center_delta == -50

    assert controller.handle_voice("contrast up") is True
    assert viewer.width_delta == -100


def test_handle_voice_unknown_command():
    controller, model, viewer = make_controller()

    start_index = model.get_current_index()
    start_zoom = controller.zoom

    changed = controller.handle_voice("abracadabra")

    assert changed is False
    assert model.get_current_index() == start_index
    assert controller.zoom == start_zoom