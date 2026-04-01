class Controller:

    def __init__(self, model, viewer):
        self.model = model
        self.viewer = viewer

    def handle_key(self, key):
        if key == "d":
            return self.execute_action("next")

        elif key == "a":
            return self.execute_action("previous")

        elif key == "1":
            return self.execute_action("bone")

        elif key == "2":
            return self.execute_action("soft")

        return False

    def normalize_command(self, command):
        command = command.lower().strip()

        filler_words = {"go", "please", "to"}
        words = command.split()
        words = [word for word in words if word not in filler_words]

        return " ".join(words)

    def handle_voice(self, command):
        command = self.normalize_command(command)

        if "next" in command:
            return self.execute_action("next")

        elif "previous" in command or "back" in command:
            return self.execute_action("previous")

        elif "bone" in command or "one" in command:
            return self.execute_action("bone")

        elif "soft" in command or "two" in command:
            return self.execute_action("soft")

        return False

    def execute_action(self, action):
        changed = False

        if action == "next":
            self.model.next_slice()
            changed = True

        elif action == "previous":
            self.model.previous_slice()
            changed = True

        elif action == "bone":
            self.viewer.set_bone_window()
            changed = True

        elif action == "soft":
            self.viewer.set_soft_window()
            changed = True

        return changed

    def update_view(self):
        self.viewer.set_image(self.model.get_current_slice())