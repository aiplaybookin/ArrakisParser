"""
Table Extractor Module

Handles extraction and merging of tables from PDF pages.
"""

from typing import List, Dict, Any
from PIL import Image
from api_clients.base_client import BaseAPIClient


class TableExtractor:
    """Extracts and merges tables from PDF pages."""

    def __init__(self, api_client: BaseAPIClient):
        """
        Initialize table extractor.

        Args:
            api_client: API client for table extraction
        """
        self.api_client = api_client

    def extract_all_tables(self, images: List[Image.Image]) -> List[Dict[str, Any]]:
        """
        Extract all tables from PDF pages.

        Args:
            images: List of PDF page images

        Returns:
            List of extracted and merged tables
        """
        all_tables = []

        # Extract tables from each page
        for page_num, image in enumerate(images, start=1):
            result = self.api_client.extract_tables_from_image(image, page_num)
            page_tables = result.get('tables', [])

            for table in page_tables:
                all_tables.append(table)

        print(f"\nTotal tables extracted (before merging): {len(all_tables)}")

        # Merge tables that continue across pages
        merged_tables = self._merge_continued_tables(all_tables)

        print(f"Total tables after merging: {len(merged_tables)}")

        return merged_tables

    def _merge_continued_tables(self, tables: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge tables that continue across pages.

        Args:
            tables: List of extracted tables

        Returns:
            List of merged tables
        """
        if not tables:
            return []

        merged = []
        i = 0

        while i < len(tables):
            current_table = tables[i]

            # Check if this table continues to next pages
            if current_table.get('is_continued', False) and i + 1 < len(tables):
                next_table = tables[i + 1]

                # Check if next table is a continuation
                if self.api_client.is_table_continuation(current_table, next_table):
                    print(f"Merging table from page {current_table['page']} with continuation on page {next_table['page']}")

                    # Merge the tables
                    merged_table = self._merge_two_tables(current_table, next_table)

                    # Continue checking for more continuations
                    j = i + 2
                    while j < len(tables):
                        if merged_table.get('is_continued', False):
                            candidate = tables[j]
                            if self.api_client.is_table_continuation(merged_table, candidate):
                                print(f"Merging continuation from page {candidate['page']}")
                                merged_table = self._merge_two_tables(merged_table, candidate)
                                j += 1
                            else:
                                break
                        else:
                            break

                    merged.append(merged_table)
                    i = j
                else:
                    merged.append(current_table)
                    i += 1
            else:
                merged.append(current_table)
                i += 1

        return merged

    def _merge_two_tables(self, table1: Dict[str, Any], table2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two consecutive tables.

        Args:
            table1: First table
            table2: Second table (continuation)

        Returns:
            Merged table
        """
        # Parse table contents
        content1 = table1.get('content', '').strip()
        content2 = table2.get('content', '').strip()

        lines1 = content1.split('\n')
        lines2 = content2.split('\n')

        # Remove separator line from first table if present
        if len(lines1) >= 2 and '---' in lines1[-1]:
            lines1 = lines1[:-1]

        # Skip header and separator from continuation table
        if len(lines2) >= 3:
            # Typically: header | separator | data...
            # We want to skip header and separator, keep only data
            lines2 = lines2[2:]
        elif len(lines2) >= 2:
            lines2 = lines2[1:]

        # Merge content
        merged_content = '\n'.join(lines1 + lines2)

        # Create merged table
        merged_table = {
            'caption': table1.get('caption'),  # Keep caption from first table
            'content': merged_content,
            'footnotes': table2.get('footnotes') or table1.get('footnotes'),  # Prefer footnotes from last table
            'page': table1.get('page'),  # Keep original page
            'page_range': f"{table1.get('page')}-{table2.get('page')}",  # Track page range
            'is_continued': table2.get('is_continued', False)  # Check if still continued
        }

        return merged_table

    def number_tables(self, tables: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add sequential numbering to tables.

        Args:
            tables: List of tables

        Returns:
            Tables with table_number field added
        """
        for i, table in enumerate(tables, start=1):
            table['table_number'] = i

        return tables
