"""
Gemini API Client

Uses Google's Gemini vision model to extract tables from PDF pages.
"""

import os
import json
import time
from typing import Dict, Any
from PIL import Image
import google.generativeai as genai
from .base_client import BaseAPIClient


class GeminiClient(BaseAPIClient):
    """Client for Google Gemini API."""

    EXTRACTION_PROMPT = """Analyze this PDF page image and extract ALL tables present.

For each table found, provide:
1. **Caption**: The table's title or caption (usually appears above the table). If no caption exists, return null.
2. **Content**: The complete table content in HTML format. Preserve:
   - All rows and columns exactly as they appear
   - Merged cells using rowspan and colspan attributes
   - Column alignments
   - Header rows using <thead> and <th> tags
   - Body rows using <tbody> and <td> tags
   - **Special formatting**: Use proper HTML entities for:
     * Superscripts: <sup>text</sup> (e.g., m<sup>2</sup>, 10<sup>-3</sup>)
     * Subscripts: <sub>text</sub> (e.g., H<sub>2</sub>O, CO<sub>2</sub>)
     * Chemical formulas: preserve subscripts/superscripts (e.g., H<sub>2</sub>SO<sub>4</sub>)
     * Greek letters and special symbols using HTML entities
   - All data accurately with proper HTML escaping
3. **Footnotes**: Any footnotes, notes, or references associated with this table (usually appear below the table). If none exist, return null.

CRITICAL REQUIREMENTS:
- If a table appears to be cut off at the bottom of the page (incomplete rows, continuation markers like "continued...", etc.), note this in a special field 'is_continued': true
- Preserve exact structure and content - accuracy is critical
- Use proper HTML table structure with <table>, <thead>, <tbody>, <tr>, <th>, <td> tags
- Pay special attention to scientific notation, chemical formulas, and mathematical expressions
- Return data in JSON format

Return format:
{
  "tables": [
    {
      "caption": "Table caption text or null",
      "content": "<table>\\n  <thead>\\n    <tr>\\n      <th>Header 1</th>\\n      <th>Header 2</th>\\n    </tr>\\n  </thead>\\n  <tbody>\\n    <tr>\\n      <td>Data 1</td>\\n      <td>Data 2</td>\\n    </tr>\\n  </tbody>\\n</table>",
      "footnotes": "Footnote text or null",
      "is_continued": false
    }
  ]
}

If no tables are found, return: {"tables": []}
"""

    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        """
        Initialize Gemini client.

        Args:
            api_key: Gemini API key (if None, uses GEMINI_API_KEY env var)
            model: Model name to use
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)

    def extract_tables_from_image(self, image: Image.Image, page_number: int) -> Dict[str, Any]:
        """
        Extract tables from a page image using Gemini.

        Args:
            image: PIL Image of the PDF page
            page_number: Page number in the PDF

        Returns:
            Dictionary containing extracted tables, tokens used, and time taken
        """
        start_time = time.time()
        tokens_used = 0

        try:
            print(f"Analyzing page {page_number} with Gemini...")

            # Generate content from image
            response = self.model.generate_content([self.EXTRACTION_PROMPT, image])

            # Extract token usage
            try:
                if hasattr(response, 'usage_metadata'):
                    tokens_used = response.usage_metadata.total_token_count
            except Exception:
                tokens_used = 0

            # Parse response
            response_text = response.text.strip()

            # Try to extract JSON from the response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            result = json.loads(response_text)

            # Add page number to each table
            for table in result.get('tables', []):
                table['page'] = page_number

            time_taken = time.time() - start_time

            print(f"Found {len(result.get('tables', []))} table(s) on page {page_number}")
            print(f"Tokens used: {tokens_used}, Time taken: {time_taken:.2f}s")

            # Add metadata
            result['tokens_used'] = tokens_used
            result['time_taken'] = time_taken

            return result

        except json.JSONDecodeError as e:
            time_taken = time.time() - start_time
            print(f"Error parsing JSON response: {e}")
            print(f"Response: {response.text}")
            return {'tables': [], 'tokens_used': tokens_used, 'time_taken': time_taken}
        except Exception as e:
            time_taken = time.time() - start_time
            print(f"Error analyzing page {page_number}: {e}")
            return {'tables': [], 'tokens_used': tokens_used, 'time_taken': time_taken}

    def is_table_continuation(self, prev_table: Dict[str, Any], curr_table: Dict[str, Any]) -> bool:
        """
        Determine if current table continues previous table.

        Args:
            prev_table: Previous table data
            curr_table: Current table data

        Returns:
            True if curr_table continues prev_table
        """
        import re

        # Check if previous table is marked as continued
        if not prev_table.get('is_continued', False):
            return False

        # Check if current table has no caption (likely continuation)
        if curr_table.get('caption'):
            return False

        # Additional heuristic: compare column structure (HTML tables)
        prev_content = prev_table.get('content', '')
        curr_content = curr_table.get('content', '')

        if not prev_content or not curr_content:
            return False

        # Count number of <th> or <td> tags in first row to determine columns
        prev_cols = len(re.findall(r'<th[^>]*>|<td[^>]*>', prev_content.split('</tr>')[0] if '</tr>' in prev_content else prev_content))
        curr_cols = len(re.findall(r'<th[^>]*>|<td[^>]*>', curr_content.split('</tr>')[0] if '</tr>' in curr_content else curr_content))

        # If column counts match and previous is marked as continued, it's likely a continuation
        return prev_cols == curr_cols and prev_cols > 0
