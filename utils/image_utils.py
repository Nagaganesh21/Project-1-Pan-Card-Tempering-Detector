import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity

def resize_image(image, width, height):
    """Resize the input image to the specified width and height."""
    image_np = np.array(image)  # Convert PIL Image to NumPy array
    resized_image = cv2.resize(image_np, (width, height))  # Resize the NumPy array
    return Image.fromarray(resized_image)  # Convert resized NumPy array back to PIL Image

def convert_to_grayscale(image):
    """Convert the input image to grayscale."""
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

def calculate_similarity(original_image, tampered_image):
    """Calculate the structural similarity between two images."""
    # Convert images to grayscale
    original_gray = convert_to_grayscale(original_image)
    tampered_gray = convert_to_grayscale(tampered_image)

    # Calculate the structural similarity
    (score, _) = structural_similarity(original_gray, tampered_gray, full=True)

    return score
