"""
JSON Generator Module

Generates JSON output files for extracted tables with HTML content.
"""

import os
import json
from typing import Dict, Any, List


class JSONGenerator:
    """Generates JSON files for tables."""

    def __init__(self, output_dir: str):
        """
        Initialize JSON generator.

        Args:
            output_dir: Directory to save JSON files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_json_file(self, table: Dict[str, Any]) -> str:
        """
        Generate a JSON file for a single table.

        Args:
            table: Table data dictionary

        Returns:
            Path to the generated file
        """
        table_num = table.get('table_number', 0)
        page = table.get('page', 0)
        page_range = table.get('page_range', str(page))

        # Create filename
        filename = f"table_{table_num}_page_{page_range}.json"
        filepath = os.path.join(self.output_dir, filename)

        # Get HTML content directly (already in HTML format from API)
        html_content = table.get('content', '')

        # Build JSON structure
        json_data = {
            "table_number": table_num,
            "page": page,
            "page_range": page_range,
            "caption": table.get('caption'),
            "content": html_content,
            "footnotes": table.get('footnotes'),
            "time_taken": table.get('time_taken', 0),
            "tokens_used": table.get('tokens_used', 0)
        }

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print(f"Generated: {filename}")
        return filepath

    def generate_all_json_files(self, tables: List[Dict[str, Any]]) -> List[str]:
        """
        Generate JSON files for all tables.

        Args:
            tables: List of table data dictionaries

        Returns:
            List of generated file paths
        """
        print(f"\nGenerating JSON files in {self.output_dir}...")

        filepaths = []
        for table in tables:
            filepath = self.generate_json_file(table)
            filepaths.append(filepath)

        print(f"\nGenerated {len(filepaths)} JSON file(s)")
        return filepaths

    def generate_summary(self, tables: List[Dict[str, Any]], total_time: float, total_tokens: int) -> str:
        """
        Generate a summary JSON file with all tables.

        Args:
            tables: List of table data dictionaries
            total_time: Total processing time
            total_tokens: Total tokens used

        Returns:
            Path to the summary file
        """
        summary_path = os.path.join(self.output_dir, "summary.json")

        # Build summary data
        tables_summary = []
        for table in tables:
            # Get HTML content directly (already in HTML format from API)
            html_content = table.get('content', '')

            table_summary = {
                "table_number": table.get('table_number', 0),
                "page": table.get('page', 0),
                "page_range": table.get('page_range', str(table.get('page', 0))),
                "caption": table.get('caption'),
                "content": html_content,
                "footnotes": table.get('footnotes'),
                "time_taken": table.get('time_taken', 0),
                "tokens_used": table.get('tokens_used', 0)
            }
            tables_summary.append(table_summary)

        summary = {
            "total_tables": len(tables),
            "total_time_taken": total_time,
            "total_tokens_used": total_tokens,
            "tables": tables_summary
        }

        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"Generated summary file: summary.json")
        return summary_path
