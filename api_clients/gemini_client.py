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

    EXTRACTION_PROMPT = """Analyze this PDF page image and extract ALL tables present with MAXIMUM ACCURACY.

EXTRACTION PROCESS - Follow these steps exactly:

1. **Identify Table Boundaries**: Locate the start and end of each table on the page
2. **Determine Table Structure**:
   - Count the total number of columns
   - Identify header row(s)
   - Identify data rows
   - Note any merged cells (rowspan/colspan)

3. **Extract Row-by-Row** (CRITICAL - Read each row carefully):
   - Start with the header row
   - For EACH row, go left-to-right through ALL columns
   - Verify each cell's content before moving to the next
   - Ensure column alignment is maintained across all rows
   - Double-check that no cells are skipped or merged incorrectly

4. **Verify Extraction**:
   - Count columns in each row - they should match
   - Verify all rows are captured
   - Check for any misaligned data
   - Confirm merged cells are correctly marked with rowspan/colspan

For each table found, provide:

1. **Caption**: The table's title or caption (usually appears above the table). If no caption exists, return null.

2. **Content**: The complete table in HTML format with PERFECT alignment:

   STRUCTURAL REQUIREMENTS:
   - Use <table>, <thead>, <tbody>, <tr>, <th>, <td> tags
   - Header rows: Use <thead> with <th> tags
   - Data rows: Use <tbody> with <td> tags
   - Merged cells: Use rowspan="N" and/or colspan="N" attributes

   FORMATTING REQUIREMENTS (preserve exactly as shown):
   - Superscripts: <sup>text</sup> (e.g., m<sup>2</sup>, 10<sup>-3</sup>, x<sup>n</sup>)
   - Subscripts: <sub>text</sub> (e.g., H<sub>2</sub>O, CO<sub>2</sub>, H<sub>2</sub>SO<sub>4</sub>)
   - Chemical formulas: Accurate subscripts/superscripts (e.g., Ca<sup>2+</sup>, SO<sub>4</sub><sup>2-</sup>)
   - Mathematical notation: Proper formatting (e.g., 10<sup>-3</sup>, x<sub>i</sub>)
   - Greek letters: Use HTML entities (&alpha;, &beta;, &Delta;, etc.)
   - Special characters: Proper HTML escaping (&lt;, &gt;, &amp;, etc.)

   ACCURACY CHECKS:
   - Every row must have the same number of columns (accounting for colspan)
   - No cells should be empty unless truly empty in the source
   - Text should be exactly as shown, with correct spacing
   - Numbers should match exactly, including decimal places
   - Units should be preserved (%, $, degrees, etc.)

3. **Footnotes**: Any footnotes, notes, or references below the table. If none exist, return null.

CRITICAL REQUIREMENTS:
- **ROW VERIFICATION**: After extracting each row, verify the column count matches the header
- **CONTINUATION DETECTION**: If table is cut off at bottom (incomplete rows, "continued...", etc.), set 'is_continued': true
- **NO ASSUMPTIONS**: Extract only what you see - don't infer or guess missing data
- **ACCURACY OVER SPEED**: Take time to ensure every cell is correctly placed

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

    def __init__(self, api_key: str = None, model: str = "gemini-2.5-pro"):
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
        input_tokens = 0
        output_tokens = 0
        total_tokens = 0

        try:
            print(f"Analyzing page {page_number} with Gemini...")

            # Generate content from image
            response = self.model.generate_content([self.EXTRACTION_PROMPT, image])

            # Extract token usage (input and output separately)
            try:
                if hasattr(response, 'usage_metadata'):
                    usage = response.usage_metadata
                    input_tokens = getattr(usage, 'prompt_token_count', 0)
                    output_tokens = getattr(usage, 'candidates_token_count', 0)
                    total_tokens = getattr(usage, 'total_token_count', input_tokens + output_tokens)
            except Exception:
                input_tokens = 0
                output_tokens = 0
                total_tokens = 0

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
            print(f"Tokens - Input: {input_tokens}, Output: {output_tokens}, Total: {total_tokens}")
            print(f"Time taken: {time_taken:.2f}s")

            # Add metadata
            result['input_tokens'] = input_tokens
            result['output_tokens'] = output_tokens
            result['tokens_used'] = total_tokens
            result['time_taken'] = time_taken

            return result

        except json.JSONDecodeError as e:
            time_taken = time.time() - start_time
            print(f"Error parsing JSON response: {e}")
            print(f"Response: {response.text}")
            return {
                'tables': [],
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'tokens_used': total_tokens,
                'time_taken': time_taken
            }
        except Exception as e:
            time_taken = time.time() - start_time
            print(f"Error analyzing page {page_number}: {e}")
            return {
                'tables': [],
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'tokens_used': total_tokens,
                'time_taken': time_taken
            }

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
