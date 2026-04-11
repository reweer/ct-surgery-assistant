class Controller:

    def __init__(self, model, viewer):
        self.model = model
        self.viewer = viewer

        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0

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

    def _parse_number(self, words):
        word_nums = {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
            "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
            "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
            "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
            "hundred": 100, "thousand": 1000
        }
        
        total = 0
        current = 0
        found = False

        for word in words:
            if word.isdigit():
                total = int(word)
                found = True
                break
            
            if word in word_nums:
                found = True
                val = word_nums[word]
                if val == 100:
                    current = (current if current > 0 else 1) * 100
                elif val == 1000:
                    total += (current if current > 0 else 1) * 1000
                    current = 0
                else:
                    current += val
        
        result = total + current
        return result if found else None

    def handle_voice(self, command):
        command = self.normalize_command(command)
        print(f"[DEBUG] Processing command: '{command}'")
        words = command.split()

        number = self._parse_number(words)

        if "first" in command:
            return self.execute_action("first")

        elif "last" in command:
            return self.execute_action("last")

        elif "middle" in command:
            return self.execute_action("middle")

        # Relative movement first
        elif "next" in command:
            return self.execute_action("next", number)

        elif "previous" in command or "back" in command:
            return self.execute_action("previous", number)

        # Absolute slice jump
        elif "slice" in command:
            if number is not None:
                return self.execute_action("slice", number)

        elif "bone" in command or "one" in command:
            if number is None or number == 1:
                return self.execute_action("bone")

        elif "soft" in command or "two" in command:
            if number is None or number == 2:
                return self.execute_action("soft")

        elif "zoom in" in command:
            return self.execute_action("zoom_in")

        elif "zoom out" in command:
            return self.execute_action("zoom_out")

        elif "left" in command:
            return self.execute_action("left")

        elif "right" in command:
            return self.execute_action("right")

        elif "up" in command:
            return self.execute_action("up")

        elif "down" in command:
            return self.execute_action("down")

        elif "center" in command:
            return self.execute_action("center")

        print(f"[DEBUG] Command '{command}' not matched to any action.")
        return False

    def execute_action(self, action, value=None):
        print(f"[DEBUG] Executing action: {action} with value: {value}")
        changed = False

        if action in ["next", "previous", "slice", "first", "last", "middle"]:
            self.zoom = 1.0
            self.offset_x = 0
            self.offset_y = 0

        if action == "next":
            step = value if value is not None else 1
            self.model.move_by(step)
            changed = True

        elif action == "previous":
            step = value if value is not None else 1
            self.model.move_by(-step)
            changed = True

        elif action == "slice":
            if value is not None:
                self.model.set_slice(value - 1)  # Humans use 1-based indexing
                changed = True

        elif action == "first":
            self.model.go_to_first()
            changed = True

        elif action == "last":
            self.model.go_to_last()
            changed = True

        elif action == "middle":
            self.model.go_to_middle()
            changed = True

        elif action == "bone":
            self.viewer.set_bone_window()
            changed = True

        elif action == "soft":
            self.viewer.set_soft_window()
            changed = True

        elif action == "zoom_in":
            self.zoom = min(5.0, self.zoom * 1.2)
            changed = True

        elif action == "zoom_out":
            self.zoom = max(1.0, self.zoom / 1.2)
            changed = True

        elif action == "left":
            self.offset_x += 30
            changed = True

        elif action == "right":
            self.offset_x -= 30
            changed = True

        elif action == "up":
            self.offset_y += 30
            changed = True

        elif action == "down":
            self.offset_y -= 30
            changed = True

        elif action == "center":
            self.zoom = 1.0
            self.offset_x = 0
            self.offset_y = 0
            changed = True

        return changed

    def update_view(self):
        self.viewer.set_image(self.model.get_current_slice())

    def clamp(self, img_w, img_h, view_w, view_h):
        max_x = max(0, (img_w * self.zoom - view_w) / 2)
        max_y = max(0, (img_h * self.zoom - view_h) / 2)

        self.offset_x = max(-max_x, min(self.offset_x, max_x))
        self.offset_y = max(-max_y, min(self.offset_y, max_y))