# ArrakisParser - PDF Table Parser

A high-accuracy PDF table parser that extracts tables with captions, contents, and footnotes using AI vision models (Gemini or Claude Sonnet).

## Features

- **AI-Powered Extraction**: Uses Gemini or Claude Sonnet APIs for accurate table detection
- **Complete Table Data**: Extracts captions, table contents, and footnotes
- **Multi-Page Support**: Automatically merges tables that span multiple pages
- **Structure Preservation**: Maintains merged cells, column alignments, and table structure
- **Markdown Output**: Generates clean markdown files for each table

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Usage

```bash
# Using Gemini API
python main.py --pdf input.pdf --api gemini --output-dir output/

# Using Claude Sonnet API
python main.py --pdf input.pdf --api sonnet --output-dir output/

# With custom DPI for image conversion
python main.py --pdf input.pdf --api gemini --dpi 300
```

## Architecture

- `main.py`: CLI entry point
- `pdf_converter.py`: PDF to image conversion
- `api_clients/`: API client implementations
- `table_extractor.py`: Table extraction and merging logic
- `markdown_generator.py`: Markdown output generation

## Output Format

Each table is saved as a separate markdown file with naming convention:
`table_1_page_3.md`, `table_2_page_5.md`, etc.

Each file contains:
- Table caption (if available)
- Table contents in markdown format
- Table footnotes (if available)
