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


def detect_edges_sobel(img):
    """Apply Sobel edge detection."""
    gray = convert_to_grayscale(img)
    
    # Calculate gradients in X and Y directions
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Combine gradients
    sobel = np.sqrt(sobelx**2 + sobely**2)
    
    # Normalize to 0-255
    sobel = np.uint8(sobel / sobel.max() * 255)
    
    return sobel


def detect_edges_laplacian(img):
    """Apply Laplacian edge detection."""
    gray = convert_to_grayscale(img)
    
    # Apply Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
    
    # Convert to absolute values and normalize
    laplacian = np.absolute(laplacian)
    laplacian = np.uint8(laplacian / laplacian.max() * 255)
    
    return laplacian


def detect_edges_prewitt(img):
    """Apply Prewitt edge detection."""
    gray = convert_to_grayscale(img)
    
    # Prewitt kernels
    kernelx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernely = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    
    # Apply kernels
    prewittx = cv2.filter2D(gray, cv2.CV_64F, kernelx)
    prewitty = cv2.filter2D(gray, cv2.CV_64F, kernely)
    
    # Combine gradients
    prewitt = np.sqrt(prewittx**2 + prewitty**2)
    
    # Normalize to 0-255
    prewitt = np.uint8(prewitt / prewitt.max() * 255)
    
    return prewitt


def detect_edges_scharr(img):
    """Apply Scharr edge detection (more accurate than Sobel)."""
    gray = convert_to_grayscale(img)
    
    # Calculate gradients using Scharr operator
    scharrx = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
    scharry = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
    
    # Combine gradients
    scharr = np.sqrt(scharrx**2 + scharry**2)
    
    # Normalize to 0-255
    scharr = np.uint8(scharr / scharr.max() * 255)
    
    return scharr


def detect_edges_contour(img, threshold=127):
    """Detect edges using contour detection."""
    gray = convert_to_grayscale(img)
    
    # Apply threshold
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create empty image to draw contours
    edges = np.zeros_like(gray)
    cv2.drawContours(edges, contours, -1, (255, 255, 255), 1)
    
    return edges
