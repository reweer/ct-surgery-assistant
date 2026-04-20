import re


class Controller:

    def __init__(self, model, viewer):
        self.model = model
        self.viewer = viewer

        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.last_voice_transcript = ""

    def handle_key(self, key):
        if key == "d":
            return self.execute_action("next")

        elif key == "a":
            return self.execute_action("previous")

        elif key == "1":
            return self.execute_action("bone")

        elif key == "2":
            return self.execute_action("soft")

        elif key == "3":
            return self.execute_action("sinus")
        
        elif key == "r":
            return self.execute_action("restore_view")

        return False

    def normalize_command(self, command):
        command = command.lower().strip()

        # phrase-level cleanup first
        phrase_aliases = {
            "zoomin": "zoom in",
            "zoomout": "zoom out",
            "a lot": "fast",
            "go back": "previous",
            "move left": "left",
            "move right": "right",
            "move up": "up",
            "move down": "down",

            # common ASR phrase mistakes
            "but thing": "previous ten",
            "bark ten": "previous ten",
            "please use them": "previous ten",
            "sly stone": "slice ten",
            "zoom mean": "zoom in",
            "you re in": "zoom in",
            "you are in": "zoom in",
            "john mean": "zoom in",
            "jimmy": "zoom in",
            "is all about": "zoom out",
            "you can reach out": "zoom out",
            "as about": "zoom out",
            "zone out": "zoom out",
            "you saw out": "zoom out",
            "you re out": "zoom out",
            "you are out": "zoom out",
            "you name": "zoom in",
            "likes to on the hundreds": "next one hundred",
            "bug free": "back three",
            "next him": "next ten",
            "makes ten": "next ten",
            "next time": "next ten",
            "barack five": "back five",
            "mike five": "back five",
            "but five": "back five",
            "but for it": "back five",
            "burke five": "back five",
            "previous for": "previous five",
            "but fife": "back five",
            "the mean": "zoom in",
            "sign knows": "sinus",
            "china s": "sinus",

        }

        for old, new in phrase_aliases.items():
            command = command.replace(old, new)

        # remove punctuation
        command = re.sub(r"[^\w\s]", " ", command)
        command = re.sub(r"\s+", " ", command).strip()

        filler_words = {"go", "please", "to"}
        words = command.split()
        words = [word for word in words if word not in filler_words]

        # common ASR mistakes / synonyms (single-word only)
        alias_map = {
            "forward": "next",
            "back": "previous",
            "won": "one",
            "too": "two",
            "them": "ten",
            "thing": "ten",
            "town": "ten",
            "tree": "three",
            "free": "three",
            "sex": "six",
            "hive": "five",
            "burton": "previous ten",
            "bottom": "previous ten",
            "wright": "right",
            "ride": "right",
            "nerf": "left",
            "let": "left",
            "op": "up",
            "dawn": "down",
            "time": "ten",
            "spring": "ten",
            "signs": "sinus",
            "chinas": "sinus",

        }

        normalized_words = []
        for word in words:
            mapped = alias_map.get(word, word)

            # jeśli alias zwraca kilka słów, rozbij je dalej
            normalized_words.extend(mapped.split())

        return " ".join(normalized_words)

    def _parse_number(self, words):
        word_nums = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "eleven": 11,
            "twelve": 12,
            "thirteen": 13,
            "fourteen": 14,
            "fifteen": 15,
            "sixteen": 16,
            "seventeen": 17,
            "eighteen": 18,
            "nineteen": 19,
            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "fifty": 50,
            "sixty": 60,
            "seventy": 70,
            "eighty": 80,
            "ninety": 90,
            "hundred": 100,
            "thousand": 1000,
        }

        total = 0
        current = 0
        found = False

        for word in words:
            if word.isdigit():
                return int(word)

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

    def parse_command(self, command):
        words = command.split()
        number = self._parse_number(words)

        if not words:
            return None

        # navigation
        if "first" in words:
            return {"action": "first"}

        if "last" in words:
            return {"action": "last"}

        if "middle" in words:
            return {"action": "middle"}

        if "slice" in words and number is not None:
            return {"action": "slice", "value": number}

        if "next" in words:
            return {"action": "next", "value": number or 1}

        if "previous" in words:
            return {"action": "previous", "value": number or 1}

        # presets
        if "bone" in words or ("one" in words and len(words) == 1):
            return {"action": "bone"}

        if "soft" in words or ("two" in words and len(words) == 1):
            return {"action": "soft"}

        if "sinus" in words:
            return {"action": "sinus"}

        # brightness / contrast
        if "brighter" in words or "brighten" in words:
            return {"action": "brighter"}

        if "darker" in words or "darken" in words:
            return {"action": "darker"}

        if "contrast" in words:
            if "up" in words or "increase" in words or "more" in words:
                return {"action": "contrast_up"}
            if "down" in words or "decrease" in words or "less" in words:
                return {"action": "contrast_down"}
            
        if (
            "restore" in words and "view" in words
        ) or (
            "default" in words and "view" in words
        ) or (
            "restart" in words and "view" in words
        ):
            return {"action": "restore_view"}

        # zoom / pan
        if "zoom" in words and "in" in words:
            value = 2 if "fast" in words or "more" in words else 1
            return {"action": "zoom_in", "value": value}

        if "zoom" in words and "out" in words:
            value = 2 if "fast" in words or "more" in words else 1
            return {"action": "zoom_out", "value": value}

        if "left" in words:
            return {"action": "left"}

        if "right" in words:
            return {"action": "right"}

        if "up" in words:
            return {"action": "up"}

        if "down" in words:
            return {"action": "down"}

        if "center" in words:
            return {"action": "center"}

        return None

    def handle_voice(self, command):
        self.last_voice_transcript = (command or "").strip()
        normalized = self.normalize_command(command)
        parsed = self.parse_command(normalized)

        print(f"[DEBUG] Original command: '{command}'")
        print(f"[DEBUG] Normalized command: '{normalized}'")

        if parsed is None:
            print(f"[DEBUG] Command not understood: '{normalized}'")
            return False

        print(f"[DEBUG] Parsed command: {parsed}")
        return self.execute_action(
            parsed["action"],
            parsed.get("value")
        )

    def execute_action(self, action, value=None):
        print(f"[DEBUG] Executing action: {action} with value: {value}")
        changed = False

        if action in ["next", "previous", "slice", "first", "last", "middle"]:
            self.zoom = 1.0
            self.offset_x = 0
            self.offset_y = 0

        # navigation
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
                self.model.set_slice(value - 1)
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

        # presets / image
        elif action == "bone":
            self.viewer.set_bone_window()
            changed = True

        elif action == "soft":
            self.viewer.set_soft_window()
            changed = True

        elif action == "sinus":
            self.viewer.set_sinus_window()
            changed = True

        elif action == "brighter":
            self.viewer.change_window(center_delta=-50)
            changed = True

        elif action == "darker":
            self.viewer.change_window(center_delta=50)
            changed = True

        elif action == "contrast_up":
            self.viewer.change_window(width_delta=-100)
            changed = True

        elif action == "contrast_down":
            self.viewer.change_window(width_delta=100)
            changed = True
            
        elif action == "restore_view":
            self.viewer.reset_window()
            changed = True

        # zoom / pan
        elif action == "zoom_in":
            repeats = value if value is not None else 1
            for _ in range(repeats):
                self.zoom = min(5.0, self.zoom * 1.2)
            changed = True

        elif action == "zoom_out":
            repeats = value if value is not None else 1
            for _ in range(repeats):
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
        max_x = max(0, (img_w - view_w) / 2)
        max_y = max(0, (img_h - view_h) / 2)

        self.offset_x = max(-max_x, min(self.offset_x, max_x))
        self.offset_y = max(-max_y, min(self.offset_y, max_y))