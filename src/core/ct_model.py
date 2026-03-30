class CTModel:

    def __init__(self, volume):
        self.volume = volume
        self.index = len(volume) // 2

    def next_slice(self):
        self.index = min(self.index + 1, len(self.volume) - 1)

    def previous_slice(self):
        self.index = max(self.index - 1, 0)

    def get_current_slice(self):
        return self.volume[self.index]