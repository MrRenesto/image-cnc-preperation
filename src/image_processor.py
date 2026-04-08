import cv2
import numpy as np


def load_image(filepath):
    """Load an image from file."""
    img = cv2.imread(filepath)
    if img is None:
        raise ValueError(f"Could not load image from {filepath}")
    return img


def convert_to_grayscale(img):
    """Convert image to grayscale."""
    if len(img.shape) == 2:
        return img
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def convert_to_bw(img, threshold=127):
    """Convert grayscale image to black and white using threshold."""
    gray = convert_to_grayscale(img)
    _, bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return bw


def detect_edges_canny(img, threshold1=50, threshold2=150):
    """Apply Canny edge detection."""
    gray = convert_to_grayscale(img)
    edges = cv2.Canny(gray, threshold1, threshold2)
    return edges
