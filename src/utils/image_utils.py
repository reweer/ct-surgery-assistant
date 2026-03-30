import numpy as np

def apply_window(image, center, width):
    """Apply CT windowing (HU → 0-255)."""

    image = image.astype("float32")

    min_val = center - width / 2
    max_val = center + width / 2

    image = np.clip(image, min_val, max_val)
    image = (image - min_val) / (max_val - min_val)

    return (image * 255).astype("uint8")