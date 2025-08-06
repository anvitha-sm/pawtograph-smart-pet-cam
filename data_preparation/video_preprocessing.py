import cv2
import numpy as np

def preprocess_frame(frame: np.ndarray, size=(224, 224), normalize=True) -> np.ndarray:
    resized = cv2.resize(frame, size)
    float_frame = resized.astype(np.float32)
    if normalize:
        float_frame /= 255.0
    return float_frame
