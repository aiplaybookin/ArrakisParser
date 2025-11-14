# ArrakisParser Usage Guide

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ArrakisParser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Note: This project uses PyMuPDF which doesn't require external dependencies like poppler.

3. **Configure API keys**

   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```env
   GEMINI_API_KEY=your_actual_gemini_key
   ANTHROPIC_API_KEY=your_actual_anthropic_key
   ```

## Basic Usage

### Using Gemini API

```bash
python main.py --pdf document.pdf --api gemini --output-dir output/
```

### Using Claude Sonnet API

```bash
python main.py --pdf document.pdf --api sonnet --output-dir output/
```

## Advanced Options

### Custom DPI for Higher Quality

Higher DPI produces better image quality but larger files:

```bash
python main.py --pdf document.pdf --api gemini --dpi 300
```

### Custom Output Directory

```bash
python main.py --pdf document.pdf --api gemini --output-dir my_tables/
```

### Pass API Key via Command Line

Instead of using .env file:

```bash
python main.py --pdf document.pdf --api gemini --gemini-key YOUR_KEY
```

```bash
python main.py --pdf document.pdf --api sonnet --sonnet-key YOUR_KEY
```

## Output Format

The parser generates JSON output with HTML tables using an enhanced 4-step extraction process with row-by-row verification for maximum accuracy:

1. **Individual table files**: `table_N_page_X.json` or `table_N_page_X-Y.json` (for multi-page tables)
2. **Summary file**: `summary.json` with all tables and aggregate statistics
3. **Token tracking**: Separate input and output token counts for detailed cost analysis

### Example JSON File Structure

```json
{
  "table_number": 1,
  "page": 3,
  "page_range": "3",
  "caption": "Table 1: Sample data showing quarterly results",
  "content": "<table>\n  <thead>\n    <tr>\n      <th>Quarter</th>\n      <th>Revenue</th>\n      <th>Expenses</th>\n      <th>Profit</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>Q1</td>\n      <td>$100K</td>\n      <td>$60K</td>\n      <td>$40K</td>\n    </tr>\n    <tr>\n      <td>Q2</td>\n      <td>$120K</td>\n      <td>$65K</td>\n      <td>$55K</td>\n    </tr>\n  </tbody>\n</table>",
  "footnotes": "Revenue figures are in USD thousands. Expenses include operational costs only.",
  "time_taken": 2.5,
  "input_tokens": 850,
  "output_tokens": 400,
  "tokens_used": 1250
}
```

### HTML Content Features

The parser extracts tables directly as HTML with special support for:

- **Superscripts**: `<sup>` tags for exponents, powers (e.g., `m<sup>2</sup>`, `10<sup>-3</sup>`)
- **Subscripts**: `<sub>` tags for chemical formulas (e.g., `H<sub>2</sub>O`, `CO<sub>2</sub>`, `H<sub>2</sub>SO<sub>4</sub>`)
- **Merged cells**: `rowspan` and `colspan` attributes
- **Proper structure**: `<thead>`, `<tbody>`, `<th>`, `<td>` tags
- **Chemical formulas**: Accurate representation with subscripts/superscripts
- **Mathematical expressions**: Scientific notation with proper formatting

### Summary File Structure

```json
{
  "total_tables": 5,
  "total_time_taken": 12.5,
  "total_input_tokens": 4250,
  "total_output_tokens": 2000,
  "total_tokens_used": 6250,
  "tables": [
    { /* table 1 data */ },
    { /* table 2 data */ },
    ...
  ]
}
```

## API Comparison

### Gemini API
- **Model**: gemini-1.5-flash
- **Pros**: Fast, cost-effective
- **Best for**: Large documents, batch processing

### Claude Sonnet API
- **Model**: claude-sonnet-4-20250514
- **Pros**: High accuracy, excellent structure preservation
- **Best for**: Complex tables, critical accuracy requirements

## Enhanced Accuracy Features

The parser uses a 4-step extraction process with explicit row-by-row verification:

1. **Boundary Detection**: Identifies table start/end including caption and footnotes
2. **Structure Analysis**: Determines column count, header rows, and merged cells
3. **Row-by-Row Extraction**: Processes each row individually with column count verification
4. **Accuracy Verification**: Reviews extracted data for misalignment before finalizing

This approach ensures:
- Correct column alignment across all rows
- Proper handling of merged cells (rowspan/colspan)
- Accurate preservation of superscripts and subscripts
- Consistent table structure throughout

## Tips for Best Results

1. **Use higher DPI (300)** for documents with small text or complex tables
2. **Claude Sonnet** typically provides better accuracy for complex table structures
3. **Gemini** is faster and more cost-effective for simpler tables
4. Ensure good PDF quality - scanned documents should be high resolution
5. **Token tracking** helps estimate costs - review input/output token usage in summary.json

## Troubleshooting

### "PDF file not found" error
- Check the path to your PDF file
- Use absolute paths if relative paths don't work

### API key errors
- Verify your API keys in the .env file
- Check that you have sufficient API credits
- Ensure no extra spaces or quotes around keys

### Missing tables
- Try increasing DPI to 300
- Check if tables are actually in the PDF (some PDFs have images of tables)
- Try different API (Gemini vs Sonnet)

### Poor table quality
- Increase DPI (--dpi 300)
- Use Claude Sonnet for better accuracy
- Ensure source PDF has good quality

## Examples

### Process academic paper
```bash
python main.py --pdf research_paper.pdf --api sonnet --dpi 300 --output-dir research_tables/
```

### Process financial report
```bash
python main.py --pdf annual_report.pdf --api gemini --output-dir financial_tables/
```

### Batch processing (shell script)
```bash
for pdf in *.pdf; do
    python main.py --pdf "$pdf" --api gemini --output-dir "output/${pdf%.pdf}/"
done
```
