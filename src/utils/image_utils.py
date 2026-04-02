import numpy as np
import cv2

def rotate_image(image, angle):
    """Rotates image by given angle (degrees)."""
    if angle == 0:
        return image
        
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return rotated

def apply_window(image, center, width):
    """Apply CT windowing (HU → 0-255)."""

    image = image.astype("float32")

    min_val = center - width / 2
    max_val = center + width / 2

    image = np.clip(image, min_val, max_val)
    image = (image - min_val) / (max_val - min_val)

    return (image * 255).astype("uint8")