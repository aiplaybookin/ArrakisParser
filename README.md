# ArrakisParser - PDF Table Parser

A high-accuracy PDF table parser that extracts tables with captions, contents, and footnotes using AI vision models (Gemini or Claude Sonnet).

## Features

- **AI-Powered Extraction**: Uses Gemini or Claude Sonnet APIs for accurate table detection
- **Complete Table Data**: Extracts captions, table contents, and footnotes
- **Multi-Page Support**: Automatically merges tables that span multiple pages
- **Structure Preservation**: Maintains merged cells, column alignments, and table structure
- **Multiple Output Formats**: JSON (with HTML tables) or Markdown output
- **Performance Tracking**: Records time taken and tokens used per table
- **No External Dependencies**: Uses PyMuPDF (no poppler required)

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
# Using Gemini API with JSON output (default)
python main.py --pdf input.pdf --api gemini --output-dir output/

# Using Claude Sonnet API with markdown output
python main.py --pdf input.pdf --api sonnet --output-format markdown

# Generate both JSON and markdown
python main.py --pdf input.pdf --api gemini --output-format both

# With custom DPI for image conversion
python main.py --pdf input.pdf --api gemini --dpi 300
```

## Architecture

- `main.py`: CLI entry point
- `pdf_converter.py`: PDF to image conversion (using PyMuPDF)
- `api_clients/`: API client implementations
  - `gemini_client.py`: Google Gemini API
  - `sonnet_client.py`: Anthropic Claude API
- `table_extractor.py`: Table extraction and merging logic
- `json_generator.py`: JSON output with HTML tables
- `markdown_generator.py`: Markdown output generation
- `html_converter.py`: Markdown to HTML table conversion

## Output Formats

### JSON Output (Default)
Each table is saved as a separate JSON file: `table_1_page_3.json`

JSON structure:
```json
{
  "table_number": 1,
  "page": 3,
  "page_range": "3",
  "caption": "Table caption text",
  "content": "<table>...</table>",
  "footnotes": "Footnote text",
  "time_taken": 2.5,
  "tokens_used": 1250
}
```

A `summary.json` file is also generated with all tables and totals.

### Markdown Output
Each table is saved as: `table_1_page_3.md`

Contains:
- Table caption (if available)
- Table contents in markdown format
- Table footnotes (if available)
