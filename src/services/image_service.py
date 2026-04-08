"""Image processing service - business logic layer."""
from processors import EdgeDetectorFactory, ImageConverter


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
