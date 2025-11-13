"""
PDF to Image Converter Module

Converts PDF pages to images for processing by AI vision models.
Uses PyMuPDF (fitz) which doesn't require external dependencies like poppler.
"""

import os
from typing import List
import fitz  # PyMuPDF
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
        # PyMuPDF uses zoom factor, calculate from DPI (72 is default PDF DPI)
        self.zoom = dpi / 72.0

    def convert_pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """
        Convert all pages of a PDF to images using PyMuPDF.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of PIL Image objects, one per page
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        print(f"Converting PDF to images (DPI: {self.dpi})...")

        images = []

        # Open the PDF
        pdf_document = fitz.open(pdf_path)

        try:
            # Convert each page to an image
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]

                # Create a transformation matrix for the desired DPI
                mat = fitz.Matrix(self.zoom, self.zoom)

                # Render page to a pixmap
                pix = page.get_pixmap(matrix=mat)

                # Convert pixmap to PIL Image
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))

                images.append(img)

        finally:
            pdf_document.close()

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
