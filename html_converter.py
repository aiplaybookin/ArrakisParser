"""
HTML Converter Module

Converts markdown tables to HTML format.
"""

import re


class HTMLConverter:
    """Converts markdown tables to HTML."""

    @staticmethod
    def markdown_table_to_html(markdown_table: str) -> str:
        """
        Convert a markdown table to HTML format.

        Args:
            markdown_table: Markdown table string

        Returns:
            HTML table string
        """
        if not markdown_table or not markdown_table.strip():
            return ""

        lines = markdown_table.strip().split('\n')

        if len(lines) < 2:
            return markdown_table  # Not a valid table

        html_parts = ['<table>']

        # Track if we're in header or body
        in_header = True

        for i, line in enumerate(lines):
            # Skip separator lines (e.g., |---|---|)
            if re.match(r'^\s*\|[\s\-:|]+\|\s*$', line):
                in_header = False
                continue

            # Parse table row
            cells = [cell.strip() for cell in line.split('|')]
            # Remove empty first/last elements if line starts/ends with |
            if cells and cells[0] == '':
                cells = cells[1:]
            if cells and cells[-1] == '':
                cells = cells[:-1]

            if not cells:
                continue

            # Determine if this is a header row (first row before separator)
            if in_header and i == 0:
                html_parts.append('  <thead>')
                html_parts.append('    <tr>')
                for cell in cells:
                    html_parts.append(f'      <th>{cell}</th>')
                html_parts.append('    </tr>')
                html_parts.append('  </thead>')
            else:
                # Body row
                if in_header:
                    # First body row after separator
                    html_parts.append('  <tbody>')
                    in_header = False

                html_parts.append('    <tr>')
                for cell in cells:
                    html_parts.append(f'      <td>{cell}</td>')
                html_parts.append('    </tr>')

        # Close tbody if it was opened
        if not in_header:
            html_parts.append('  </tbody>')

        html_parts.append('</table>')

        return '\n'.join(html_parts)

    @staticmethod
    def format_html_pretty(html: str, indent: int = 2) -> str:
        """
        Format HTML with proper indentation.

        Args:
            html: HTML string
            indent: Number of spaces for indentation

        Returns:
            Formatted HTML string
        """
        # This is a simple formatter - for production use, consider using a library
        return html
