"""Line art generation processors."""
import cv2
import numpy as np


class ContourLineArtGenerator:
    """Generate contour-based line art from an ROI in an edge image."""

    def __init__(self, min_contour_area=20.0, line_thickness=1, use_morphology=True):
        self.min_contour_area = float(min_contour_area)
        self.line_thickness = int(line_thickness)
        self.use_morphology = bool(use_morphology)

    def generate(self, img, roi):
        """Generate line art and metadata from image and ROI.

        Args:
            img: Input image, expected to be an edge image or grayscale-like image.
            roi: Tuple (x1, y1, x2, y2) in image coordinates.
        """
        gray = self._to_grayscale(img)
        x1, y1, x2, y2 = self._normalize_roi(roi, gray.shape[1], gray.shape[0])
        roi_img = gray[y1:y2, x1:x2]

        if roi_img.size == 0:
            raise ValueError("Selected ROI is empty.")

        _, binary = cv2.threshold(roi_img, 1, 255, cv2.THRESH_BINARY)

        if self.use_morphology:
            kernel = np.ones((3, 3), dtype=np.uint8)
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
            binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        filtered = [cnt for cnt in contours if cv2.contourArea(cnt) >= self.min_contour_area]

        roi_line_art = np.full_like(roi_img, 255, dtype=np.uint8)
        if filtered:
            cv2.drawContours(roi_line_art, filtered, -1, 0, self.line_thickness)

        metadata = {
            "contours_found": len(contours),
            "contours_kept": len(filtered),
            "has_hierarchy": hierarchy is not None,
            "roi": (x1, y1, x2, y2),
        }
        return roi_line_art, metadata

    @staticmethod
    def _to_grayscale(img):
        if len(img.shape) == 2:
            return img
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def _normalize_roi(roi, img_width, img_height):
        if roi is None or len(roi) != 4:
            raise ValueError("ROI is required and must contain 4 values.")

        x1, y1, x2, y2 = [int(v) for v in roi]
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))

        x1 = max(0, min(x1, img_width - 1))
        y1 = max(0, min(y1, img_height - 1))
        x2 = max(1, min(x2, img_width))
        y2 = max(1, min(y2, img_height))

        if x2 - x1 < 2 or y2 - y1 < 2:
            raise ValueError("ROI is too small.")

        return x1, y1, x2, y2
