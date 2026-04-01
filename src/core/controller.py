class Controller:

    def __init__(self, model, viewer):
        self.model = model
        self.viewer = viewer

# 🔹 keyboard
    def handle_key(self, key):
        changed = False

        if key == "d":
            self.model.next_slice()
            changed = True

        elif key == "a":
            self.model.previous_slice()
            changed = True

        elif key == "1":
            self.viewer.set_bone_window()
            changed = True

        elif key == "2":
            self.viewer.set_soft_window()
            changed = True

        return changed



    # 🔹 voice
    def handle_voice(self, command):
        changed = False
        command = command.lower().strip()

        if "next" in command:
            self.model.next_slice()
            changed = True

        elif "previous" in command or "back" in command:
            self.model.previous_slice()
            changed = True

        elif "bone" in command:
            self.viewer.set_bone_window()
            changed = True

        elif "soft" in command:
            self.viewer.set_soft_window()
            changed = True

        elif "one" in command:
            self.viewer.set_bone_window()
            changed = True

        elif "two" in command:
            self.viewer.set_soft_window()
            changed = True

        return changed

    # 🔹 render
    def update_view(self):
        self.viewer.set_image(self.model.get_current_slice())