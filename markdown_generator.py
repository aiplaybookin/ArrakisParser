"""
Markdown Generator Module

Generates markdown files for extracted tables.
"""

import os
from typing import Dict, Any, List


class MarkdownGenerator:
    """Generates markdown files for tables."""

    def __init__(self, output_dir: str):
        """
        Initialize markdown generator.

        Args:
            output_dir: Directory to save markdown files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_markdown_file(self, table: Dict[str, Any]) -> str:
        """
        Generate a markdown file for a single table.

        Args:
            table: Table data dictionary

        Returns:
            Path to the generated file
        """
        table_num = table.get('table_number', 0)
        page = table.get('page', 0)
        page_range = table.get('page_range', str(page))

        # Create filename
        filename = f"table_{table_num}_page_{page_range}.md"
        filepath = os.path.join(self.output_dir, filename)

        # Build markdown content
        content_parts = []

        # Add header with metadata
        content_parts.append(f"# Table {table_num}")
        content_parts.append(f"\n**Page(s):** {page_range}\n")

        # Add caption if available
        caption = table.get('caption')
        if caption and caption.strip():
            content_parts.append(f"## Caption\n\n{caption.strip()}\n")

        # Add table content
        content_parts.append("## Table Content\n")
        table_content = table.get('content', '')
        if table_content.strip():
            content_parts.append(table_content.strip())
        else:
            content_parts.append("*No table content available*")

        content_parts.append("\n")

        # Add footnotes if available
        footnotes = table.get('footnotes')
        if footnotes and footnotes.strip():
            content_parts.append(f"## Footnotes\n\n{footnotes.strip()}\n")

        # Write to file
        markdown_content = '\n'.join(content_parts)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"Generated: {filename}")
        return filepath

    def generate_all_markdown_files(self, tables: List[Dict[str, Any]]) -> List[str]:
        """
        Generate markdown files for all tables.

        Args:
            tables: List of table data dictionaries

        Returns:
            List of generated file paths
        """
        print(f"\nGenerating markdown files in {self.output_dir}...")

        filepaths = []
        for table in tables:
            filepath = self.generate_markdown_file(table)
            filepaths.append(filepath)

        print(f"\nGenerated {len(filepaths)} markdown file(s)")
        return filepaths

    def generate_index(self, tables: List[Dict[str, Any]]) -> str:
        """
        Generate an index file listing all tables.

        Args:
            tables: List of table data dictionaries

        Returns:
            Path to the index file
        """
        index_path = os.path.join(self.output_dir, "index.md")

        content = ["# Extracted Tables Index\n"]
        content.append(f"Total tables: {len(tables)}\n")

        for table in tables:
            table_num = table.get('table_number', 0)
            page_range = table.get('page_range', str(table.get('page', 0)))
            caption = table.get('caption', 'No caption')

            filename = f"table_{table_num}_page_{page_range}.md"

            content.append(f"## Table {table_num}")
            content.append(f"- **File:** [{filename}]({filename})")
            content.append(f"- **Page(s):** {page_range}")
            content.append(f"- **Caption:** {caption if caption else '*No caption*'}")
            content.append("")

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

        print(f"Generated index file: index.md")
        return index_path
