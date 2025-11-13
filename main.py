#!/usr/bin/env python3
"""
ArrakisParser - PDF Table Parser

Main entry point for the PDF table parser.
"""

import argparse
import os
import sys
from dotenv import load_dotenv

from pdf_converter import PDFConverter
from api_clients.gemini_client import GeminiClient
from api_clients.sonnet_client import SonnetClient
from table_extractor import TableExtractor
from markdown_generator import MarkdownGenerator


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract tables from PDF files using AI vision models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using Gemini API
  python main.py --pdf document.pdf --api gemini --output-dir output/

  # Using Claude Sonnet API
  python main.py --pdf document.pdf --api sonnet --output-dir output/

  # With custom DPI
  python main.py --pdf document.pdf --api gemini --dpi 300
        """
    )

    parser.add_argument(
        '--pdf',
        type=str,
        required=True,
        help='Path to the PDF file to parse'
    )

    parser.add_argument(
        '--api',
        type=str,
        choices=['gemini', 'sonnet'],
        required=True,
        help='API to use for table extraction (gemini or sonnet)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Directory to save markdown files (default: output/)'
    )

    parser.add_argument(
        '--dpi',
        type=int,
        default=200,
        help='DPI for PDF to image conversion (default: 200)'
    )

    parser.add_argument(
        '--gemini-key',
        type=str,
        help='Gemini API key (overrides GEMINI_API_KEY env var)'
    )

    parser.add_argument(
        '--sonnet-key',
        type=str,
        help='Anthropic API key (overrides ANTHROPIC_API_KEY env var)'
    )

    parser.add_argument(
        '--no-index',
        action='store_true',
        help='Do not generate index.md file'
    )

    return parser.parse_args()


def main():
    """Main execution function."""
    # Load environment variables from .env file
    load_dotenv()

    # Parse arguments
    args = parse_arguments()

    # Validate PDF file exists
    if not os.path.exists(args.pdf):
        print(f"Error: PDF file not found: {args.pdf}")
        sys.exit(1)

    print("=" * 60)
    print("ArrakisParser - PDF Table Parser")
    print("=" * 60)
    print(f"PDF: {args.pdf}")
    print(f"API: {args.api}")
    print(f"Output: {args.output_dir}")
    print(f"DPI: {args.dpi}")
    print("=" * 60)

    try:
        # Step 1: Convert PDF to images
        print("\n[1/4] Converting PDF to images...")
        converter = PDFConverter(dpi=args.dpi)
        images = converter.convert_pdf_to_images(args.pdf)

        # Step 2: Initialize API client
        print(f"\n[2/4] Initializing {args.api} API client...")
        if args.api == 'gemini':
            api_client = GeminiClient(api_key=args.gemini_key)
        else:  # sonnet
            api_client = SonnetClient(api_key=args.sonnet_key)

        # Step 3: Extract and merge tables
        print("\n[3/4] Extracting tables from PDF...")
        extractor = TableExtractor(api_client)
        tables = extractor.extract_all_tables(images)

        if not tables:
            print("\nNo tables found in the PDF.")
            sys.exit(0)

        # Number the tables
        tables = extractor.number_tables(tables)

        # Step 4: Generate markdown files
        print("\n[4/4] Generating markdown files...")
        generator = MarkdownGenerator(args.output_dir)
        filepaths = generator.generate_all_markdown_files(tables)

        # Generate index
        if not args.no_index:
            generator.generate_index(tables)

        # Success summary
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"Extracted {len(tables)} table(s)")
        print(f"Output directory: {args.output_dir}")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
