import cv2
import numpy as np
from PIL import Image, ImageOps
import random
import base64
from io import BytesIO
import os
from imports.baseclass import BaseClass
import PIL
from typing import Dict, List

class ImageDataSet(BaseClass):
    def __init__(self, file_path):
        # Load the image
        self.file_path = file_path
        self.image = Image.open(file_path)
        self.cv_image = cv2.imread(file_path)
    
    @property
    def contents(self) -> str:
        # returns file name for displaying the image
        return os.path.basename(self.file_path)
    
    # function to convert PIP images to base64
    def image_to_base64(self, image: PIL.Image.Image) -> str:
        """Convert a PIL image to a base64 string."""

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    # Preprocessing Methods
    def preprocess_all(self) -> Dict[str, str]:

        # 1. Resize to 256x256
        resized_image = self.image.resize((256, 256))
        
        # 2. Convert to grayscale
        grayscale_image = ImageOps.grayscale(resized_image)
        
        # 3. Normalize image pixel values (0-255 -> 0-1)
        normalized_image = np.array(grayscale_image) / 255.0
        normalized_image = Image.fromarray((normalized_image * 255).astype(np.uint8))
        
        # return {
        #     'resized': resized_image,
        #     'grayscale': grayscale_image,
        #     'normalized': normalized_image
        # }
        
        preprocessed_images = {
            key: self.image_to_base64(img) for key, img in {
                'resized': resized_image,
                'grayscale': grayscale_image,
                'normalized': normalized_image
            }.items()
        }
        return preprocessed_images
    
    # Augmentation Methods
    def augment_all(self) -> Dict[str, str]:
        # 1. Random Rotation between -30 and 30 degrees
        angle = random.uniform(-30, 30)
        rotated_image = self.image.rotate(angle)
        
        # 2. Horizontal Flip
        flipped_image = ImageOps.mirror(self.image)
        
        # 3. Add Gaussian Noise
        noisy_image = self._add_gaussian_noise(self.cv_image)
        noisy_image = Image.fromarray(noisy_image)
        
        # return {
        #     'rotated': rotated_image,
        #     'flipped': flipped_image,
        #     'noisy': noisy_image
        # }
        augmented_images = {
            key: self.image_to_base64(img) for key, img in {
                'rotated': rotated_image,
                'flipped': flipped_image,
                'noisy': noisy_image
            }.items()
        }
        return augmented_images

    # Helper method to add Gaussian noise to an image
    def _add_gaussian_noise(self, img: np.ndarray, mean=0, var=0.01) -> np.ndarray:
        '''take input as cv image and add noise to it'''
        
        row, col, ch = img.shape
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy = img + gauss.reshape(row, col, ch) * 255
        return np.clip(noisy, 0, 255).astype(np.uint8)

# Example usage:
# dataset = ImageDataSet('path/to/image.jpg')
# preprocessed_images = dataset.preprocess_image()
# augmented_images = dataset.augment_image()
