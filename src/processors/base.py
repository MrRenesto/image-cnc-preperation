"""Base classes for image processors."""
from abc import ABC, abstractmethod
import cv2
import numpy as np


class EdgeDetector(ABC):
    """Abstract base class for edge detection algorithms."""
    
    @abstractmethod
    def detect(self, img):
        """Apply edge detection to the image."""
        pass
    
    @staticmethod
    def convert_to_grayscale(img):
        """Convert image to grayscale if needed."""
        if len(img.shape) == 2:
            return img
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    @staticmethod
    def normalize_to_uint8(img):
        """Normalize image values to 0-255 range."""
        if img.max() > 0:
            return np.uint8(img / img.max() * 255)
        return np.uint8(img)
