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

3. **Install system dependencies** (for pdf2image)

   On Ubuntu/Debian:
   ```bash
   sudo apt-get install poppler-utils
   ```

   On macOS:
   ```bash
   brew install poppler
   ```

   On Windows:
   Download and install poppler from: http://blog.alivate.com.au/poppler-windows/

4. **Configure API keys**

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

### Disable Index Generation

```bash
python main.py --pdf document.pdf --api gemini --no-index
```

## Output Format

The parser generates:

1. **Individual table files**: `table_N_page_X.md` or `table_N_page_X-Y.md` (for multi-page tables)
2. **Index file**: `index.md` (unless --no-index is used)

### Example Table File Structure

```markdown
# Table 1

**Page(s):** 3

## Caption

Table 1: Sample data showing quarterly results

## Table Content

| Quarter | Revenue | Expenses | Profit |
|---------|---------|----------|--------|
| Q1      | $100K   | $60K     | $40K   |
| Q2      | $120K   | $65K     | $55K   |

## Footnotes

* Revenue figures are in USD thousands
* Expenses include operational costs only
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

## Tips for Best Results

1. **Use higher DPI (300)** for documents with small text or complex tables
2. **Claude Sonnet** typically provides better accuracy for complex table structures
3. **Gemini** is faster and more cost-effective for simpler tables
4. Ensure good PDF quality - scanned documents should be high resolution

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
