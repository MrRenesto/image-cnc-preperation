"""Edge detection algorithms using Strategy pattern."""
import cv2
import numpy as np
from .base import EdgeDetector


class CannyEdgeDetector(EdgeDetector):
    """Canny edge detection algorithm."""
    
    def __init__(self, threshold1=50, threshold2=150):
        self.threshold1 = threshold1
        self.threshold2 = threshold2
    
    def detect(self, img):
        gray = self.convert_to_grayscale(img)
        return cv2.Canny(gray, self.threshold1, self.threshold2)


class SobelEdgeDetector(EdgeDetector):
    """Sobel edge detection algorithm."""
    
    def detect(self, img):
        gray = self.convert_to_grayscale(img)
        
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        sobel = np.sqrt(sobelx**2 + sobely**2)
        return self.normalize_to_uint8(sobel)


class LaplacianEdgeDetector(EdgeDetector):
    """Laplacian edge detection algorithm."""
    
    def detect(self, img):
        gray = self.convert_to_grayscale(img)
        
        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
        laplacian = np.absolute(laplacian)
        return self.normalize_to_uint8(laplacian)


class PrewittEdgeDetector(EdgeDetector):
    """Prewitt edge detection algorithm."""
    
    def detect(self, img):
        gray = self.convert_to_grayscale(img)
        
        kernelx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
        kernely = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
        
        prewittx = cv2.filter2D(gray, cv2.CV_64F, kernelx)
        prewitty = cv2.filter2D(gray, cv2.CV_64F, kernely)
        
        prewitt = np.sqrt(prewittx**2 + prewitty**2)
        return self.normalize_to_uint8(prewitt)


class ScharrEdgeDetector(EdgeDetector):
    """Scharr edge detection algorithm (more accurate than Sobel)."""
    
    def detect(self, img):
        gray = self.convert_to_grayscale(img)
        
        scharrx = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
        scharry = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
        
        scharr = np.sqrt(scharrx**2 + scharry**2)
        return self.normalize_to_uint8(scharr)


class ContourEdgeDetector(EdgeDetector):
    """Contour-based edge detection algorithm."""
    
    def __init__(self, threshold=127):
        self.threshold = threshold
    
    def detect(self, img):
        gray = self.convert_to_grayscale(img)
        
        _, binary = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        edges = np.zeros_like(gray)
        cv2.drawContours(edges, contours, -1, (255, 255, 255), 1)
        return edges


class EdgeDetectorFactory:
    """Factory for creating edge detector instances."""
    
    _detectors = {
        'Canny': CannyEdgeDetector,
        'Sobel': SobelEdgeDetector,
        'Laplacian': LaplacianEdgeDetector,
        'Prewitt': PrewittEdgeDetector,
        'Scharr': ScharrEdgeDetector,
        'Contour': ContourEdgeDetector,
    }
    
    @classmethod
    def create(cls, algorithm_name):
        """Create an edge detector by name."""
        detector_class = cls._detectors.get(algorithm_name)
        if detector_class is None:
            raise ValueError(f"Unknown edge detection algorithm: {algorithm_name}")
        return detector_class()
    
    @classmethod
    def get_available_algorithms(cls):
        """Get list of available algorithm names."""
        return list(cls._detectors.keys())
