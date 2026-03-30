class Controller:

    def __init__(self, model, viewer):
        self.model = model
        self.viewer = viewer

    def handle_key(self, key):

        if key == ord("d"):
            self.model.next_slice()

        elif key == ord("a"):
            self.model.previous_slice()

        elif key == ord("1"):
            self.viewer.set_bone_window()

        elif key == ord("2"):
            self.viewer.set_soft_window()

        self.update_view()

    def update_view(self):
        self.viewer.update(self.model.get_current_slice())