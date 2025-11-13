"""
PDF to Image Converter Module

Converts PDF pages to images for processing by AI vision models.
"""

import os
from typing import List
from pdf2image import convert_from_path
from PIL import Image
import io
import base64


class PDFConverter:
    """Handles conversion of PDF pages to images."""

    def __init__(self, dpi: int = 200):
        """
        Initialize PDF converter.

        Args:
            dpi: Resolution for image conversion (default: 200)
        """
        self.dpi = dpi

    def convert_pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """
        Convert all pages of a PDF to images.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of PIL Image objects, one per page
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        print(f"Converting PDF to images (DPI: {self.dpi})...")
        images = convert_from_path(pdf_path, dpi=self.dpi)
        print(f"Converted {len(images)} pages")

        return images

    def image_to_base64(self, image: Image.Image, format: str = "PNG") -> str:
        """
        Convert PIL Image to base64 string.

        Args:
            image: PIL Image object
            format: Image format (default: PNG)

        Returns:
            Base64 encoded string
        """
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode('utf-8')

    def save_image(self, image: Image.Image, output_path: str):
        """
        Save image to file.

        Args:
            image: PIL Image object
            output_path: Path to save the image
        """
        image.save(output_path)
        print(f"Saved image to {output_path}")
