class CTModel:

    def __init__(self, volume):
        self.volume = volume
        self.index = len(volume) // 2

    def next_slice(self):
        self.index = min(self.index + 1, len(self.volume) - 1)

    def previous_slice(self):
        self.index = max(self.index - 1, 0)

    def move_by(self, step):
        self.index = max(0, min(self.index + step, len(self.volume) - 1))

    def set_slice(self, index):
        self.index = max(0, min(index, len(self.volume) - 1))

    def go_to_first(self):
        self.index = 0

    def go_to_last(self):
        self.index = len(self.volume) - 1

    def go_to_middle(self):
        self.index = len(self.volume) // 2

    def get_current_slice(self):
        return self.volume[self.index]

    def get_current_index(self):
        return self.index

    def get_total_slices(self):
        return len(self.volume)