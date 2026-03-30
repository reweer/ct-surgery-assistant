import pydicom
import os
import numpy as np
from collections import defaultdict

def load_dicom_series(folder):

    series = defaultdict(list)

    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)

            try:
                ds = pydicom.dcmread(path)

                if hasattr(ds, "PixelData"):
                    series_id = getattr(ds, "SeriesInstanceUID", "unknown")
                    series[series_id].append(ds)

            except:
                continue

    print(f"Found {len(series)} series")

    # 🔥 wybieramy NAJWIĘKSZĄ serię (najwięcej slice)
    largest_series = max(series.values(), key=len)

    print(f"Using series with {len(largest_series)} slices")

    # sortowanie (jeśli możliwe)
    try:
        largest_series.sort(key=lambda x: float(x.ImagePositionPatient[2]))
    except:
        print("Warning: no ImagePositionPatient")


    images = []

    for s in largest_series:

        image = s.pixel_array.astype("float32")

        slope = getattr(s, "RescaleSlope", 1)
        intercept = getattr(s, "RescaleIntercept", 0)

        image = image * slope + intercept

        images.append(image)

    return np.array(images)