"""Image processing service - business logic layer."""
import numpy as np
from processors import EdgeDetectorFactory, ImageConverter, ContourLineArtGenerator


class ImageService:
    """Service layer for image processing operations."""
    
    def __init__(self):
        self.converter = ImageConverter()
        self.edge_detector_factory = EdgeDetectorFactory()
    
    def load_image(self, filepath):
        """Load an image from file."""
        return self.converter.load_image(filepath)
    
    def save_image(self, filepath, img):
        """Save image to file."""
        self.converter.save_image(filepath, img)
    
    def convert_to_bw(self, img, threshold=127):
        """Convert image to black and white."""
        return self.converter.convert_to_bw(img, threshold)
    
    def detect_edges(self, img, algorithm):
        """Apply edge detection using specified algorithm."""
        detector = self.edge_detector_factory.create(algorithm)
        return detector.detect(img)
    
    def get_available_algorithms(self):
        """Get list of available edge detection algorithms."""
        return self.edge_detector_factory.get_available_algorithms()

    def generate_line_art_from_roi(
        self,
        img,
        roi,
        min_contour_area=20.0,
        line_thickness=1,
        use_morphology=True,
    ):
        """Generate line art for a selected ROI and compose a full output image."""
        generator = ContourLineArtGenerator(
            min_contour_area=min_contour_area,
            line_thickness=line_thickness,
            use_morphology=use_morphology,
        )

        roi_line_art, metadata = generator.generate(img, roi)
        x1, y1, x2, y2 = metadata["roi"]

        composed = np.full((img.shape[0], img.shape[1]), 255, dtype=np.uint8)
        composed[y1:y2, x1:x2] = roi_line_art
        return composed, metadata
