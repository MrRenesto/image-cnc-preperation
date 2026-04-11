"""Image conversion utilities."""
import cv2


class ImageConverter:
    """Handles image format conversions."""
    
    @staticmethod
    def load_image(filepath):
        """Load an image from file."""
        img = cv2.imread(filepath)
        if img is None:
            raise ValueError(f"Could not load image from {filepath}")
        return img
    
    @staticmethod
    def convert_to_grayscale(img):
        """Convert image to grayscale."""
        if len(img.shape) == 2:
            return img
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    @staticmethod
    def convert_to_bw(img, threshold=127):
        """Convert grayscale image to black and white using threshold."""
        gray = ImageConverter.convert_to_grayscale(img)
        _, bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return bw
    
    @staticmethod
    def save_image(filepath, img):
        """Save image to file."""
        cv2.imwrite(filepath, img)
