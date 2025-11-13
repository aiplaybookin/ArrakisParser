"""
Base API Client Interface

Defines the interface for AI API clients.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from PIL import Image


class BaseAPIClient(ABC):
    """Abstract base class for API clients."""

    @abstractmethod
    def extract_tables_from_image(self, image: Image.Image, page_number: int) -> Dict[str, Any]:
        """
        Extract tables from a page image.

        Args:
            image: PIL Image of the PDF page
            page_number: Page number in the PDF

        Returns:
            Dictionary containing extracted tables with structure:
            {
                'tables': [
                    {
                        'caption': str or None,
                        'content': str (HTML table),
                        'footnotes': str or None,
                        'page': int
                    },
                    ...
                ],
                'tokens_used': int,
                'time_taken': float (seconds)
            }
        """
        pass

    @abstractmethod
    def is_table_continuation(self, prev_table: Dict[str, Any], curr_table: Dict[str, Any]) -> bool:
        """
        Determine if current table is a continuation of previous table.

        Args:
            prev_table: Previous table data
            curr_table: Current table data

        Returns:
            True if curr_table continues prev_table
        """
        pass
