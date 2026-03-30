import cv2
from utils.image_utils import apply_window

class Viewer:

    def __init__(self):
        self.window_center = 40
        self.window_width = 400

    def update(self, image):

        image = apply_window(
            image,
            self.window_center,
            self.window_width
        )

        cv2.imshow("CT Viewer", image)
        cv2.waitKey(1)

    def set_bone_window(self):
        print("Bone window")
        self.window_center = 300
        self.window_width = 1500

    def set_soft_window(self):
        print("Soft tissue window")
        self.window_center = 40
        self.window_width = 400