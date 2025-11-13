# ArrakisParser - PDF Table Parser

A high-accuracy PDF table parser that extracts tables with captions, contents, and footnotes using AI vision models (Gemini or Claude Sonnet).

## Features

- **AI-Powered Extraction**: Uses Gemini or Claude Sonnet APIs for accurate table detection
- **Complete Table Data**: Extracts captions, table contents, and footnotes
- **Multi-Page Support**: Automatically merges tables that span multiple pages
- **Structure Preservation**: Maintains merged cells, column alignments, and table structure with proper HTML
- **HTML Output**: Tables extracted directly as HTML with support for superscripts, subscripts, and chemical formulas
- **JSON Format**: Clean JSON output with HTML table content
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
# Using Gemini API
python main.py --pdf input.pdf --api gemini --output-dir output/

# Using Claude Sonnet API
python main.py --pdf input.pdf --api sonnet --output-dir output/

# With custom DPI for image conversion
python main.py --pdf input.pdf --api gemini --dpi 300
```

## Architecture

- `main.py`: CLI entry point
- `pdf_converter.py`: PDF to image conversion (using PyMuPDF)
- `api_clients/`: API client implementations
  - `gemini_client.py`: Google Gemini API with HTML table extraction
  - `sonnet_client.py`: Anthropic Claude API with HTML table extraction
- `table_extractor.py`: HTML table extraction and merging logic
- `json_generator.py`: JSON output generation

## Output Format

Each table is saved as a separate JSON file: `table_1_page_3.json`

JSON structure:
```json
{
  "table_number": 1,
  "page": 3,
  "page_range": "3",
  "caption": "Table caption text",
  "content": "<table>\n  <thead>\n    <tr>\n      <th>Header</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>H<sub>2</sub>O</td>\n    </tr>\n  </tbody>\n</table>",
  "footnotes": "Footnote text",
  "time_taken": 2.5,
  "tokens_used": 1250
}
```

**HTML Content Features:**
- Proper table structure with `<thead>` and `<tbody>`
- Merged cells using `rowspan` and `colspan`
- Superscripts: `<sup>` for exponents (e.g., m<sup>2</sup>)
- Subscripts: `<sub>` for chemical formulas (e.g., H<sub>2</sub>O, CO<sub>2</sub>)
- Special characters properly escaped

A `summary.json` file is also generated with all tables and aggregate statistics.
