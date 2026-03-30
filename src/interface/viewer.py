import cv2
import numpy as np

class Viewer:

    def __init__(self):
        self.window_center = 40
        self.window_width = 400

    def apply_window(self, image):

        image = image.astype("float32")

        min_val = self.window_center - self.window_width // 2
        max_val = self.window_center + self.window_width // 2

        image = np.clip(image, min_val, max_val)

        image = (image - min_val) / (max_val - min_val)
        image = (image * 255).astype("uint8")

        return image

    def update(self, image):

        image = self.apply_window(image)

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