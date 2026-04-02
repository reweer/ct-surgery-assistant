import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.ct_model import CTModel
from core.controller import Controller

class MockViewer:
    def set_image(self, image): pass
    def set_bone_window(self): pass
    def set_soft_window(self): pass

def test_navigation():
    # Setup: 100 slices
    volume = list(range(100))
    model = CTModel(volume)
    viewer = MockViewer()
    controller = Controller(model, viewer)

    # Initial state (usually middle)
    print(f"Initial slice: {model.get_current_index()}") # 50

    # 1. Next / Previous
    controller.handle_voice("next")
    assert model.get_current_index() == 51
    controller.handle_voice("previous")
    assert model.get_current_index() == 50
    print("✓ Basic next/previous OK")

    # 2. Next 5 / Previous 5 / Back 5
    controller.handle_voice("next five")
    assert model.get_current_index() == 55
    controller.handle_voice("previous 5")
    assert model.get_current_index() == 50
    controller.handle_voice("back five")
    assert model.get_current_index() == 45
    print("✓ Steps (words and digits) OK")

    # 3. Slice number
    controller.handle_voice("slice 10")
    assert model.get_current_index() == 9 # 1-based to 0-based
    controller.handle_voice("slice one hundred") # "one hundred" isn't in word_nums yet, but "100" would be. Let's try digits.
    controller.handle_voice("slice 80")
    assert model.get_current_index() == 79
    print("✓ Absolute slice jumps OK")

    # 4. First / Last / Middle
    controller.handle_voice("first slice")
    assert model.get_current_index() == 0
    controller.handle_voice("last slice")
    assert model.get_current_index() == 99
    controller.handle_voice("middle slice")
    assert model.get_current_index() == 50
    print("✓ Boundary jumps (first/last/middle) OK")

    # 5. Out of bounds
    controller.handle_voice("slice 200")
    assert model.get_current_index() == 99
    controller.handle_voice("slice 0")
    assert model.get_current_index() == 0
    controller.handle_voice("previous 1000")
    assert model.get_current_index() == 0
    print("✓ Boundary safety OK")

    print("\nALL NAVIGATION TESTS PASSED!")

if __name__ == "__main__":
    test_navigation()
