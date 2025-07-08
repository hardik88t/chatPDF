# ChatPDF Clone - Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configuration
The Gemini API key is already configured in the code, but you can override it:
```bash
# Optional: Create .env file for custom configuration
cp .env.example .env
# Edit .env with your preferred settings
```

### 3. Run Basic Tests
```bash
# Test the system
python test_basic.py
```

### 4. Start Using the Application

#### Interactive Mode (Recommended)
```bash
# Chat with BERT paper
python main.py chat bert_research_paper.pdf --interactive

# Or simply
python main.py chat bert_research_paper.pdf
```

#### Single Question Mode
```bash
python main.py chat bert_research_paper.pdf -q "What is BERT?"
```

#### Run Predefined Tests
```bash
# Test with BERT paper (includes specific test questions)
python main.py test bert_research_paper.pdf

# Test with other papers
python main.py test ai_application_research_paper.pdf
python main.py test ml_in_ai_research_paper.pdf
```

## Usage Examples

### Example Session
```bash
$ python main.py chat bert_research_paper.pdf

Loading PDF: bert_research_paper.pdf
✓ PDF loaded successfully!
  - Total characters: 45,231
  - Text chunks: 23

🎯 Interactive mode started for: bert_research_paper.pdf
Type your questions (or 'quit' to exit):
--------------------------------------------------

❓ Your question: What kind of neural network architecture is used in this paper?

🤔 Question: What kind of neural network architecture is used in this paper?
🔍 Processing...

🤖 Answer (direct query):
--------------------------------------------------
BERT uses a Transformer architecture, specifically a bidirectional encoder...
--------------------------------------------------
📊 Used 3 text chunks, 245 tokens
```

## Project Structure

```
chatPDF/
├── PROJECT_GOALS.md          # Project goals and progress tracking
├── SETUP.md                  # This setup guide
├── main.py                   # Main entry point
├── cli.py                    # Command-line interface
├── pdf_processor.py          # PDF text extraction and processing
├── ai_handler.py             # Gemini API integration
├── config.py                 # Configuration management
├── test_basic.py             # Basic functionality tests
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── *.pdf                     # Research papers for testing
```

## Features

- **Smart PDF Processing**: Extracts and chunks text optimally for AI processing
- **Query Classification**: Automatically detects direct, indirect, and reference queries
- **Token Optimization**: Stays within 800-token limit for cost efficiency
- **Interactive CLI**: User-friendly command-line interface
- **Batch Testing**: Predefined test questions for validation
- **Multiple PDF Support**: Works with any research paper PDF

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **PDF Not Loading**: Check file path and permissions
   ```bash
   ls -la *.pdf
   ```

3. **API Errors**: Verify the Gemini API key is working
   ```bash
   python -c "from config import Config; Config().validate()"
   ```

4. **No Text Extracted**: Try with a different PDF or check if PDF is text-based

### Getting Help
```bash
# Show system information
python main.py info

# Show CLI help
python main.py --help
python main.py chat --help
```

## Next Steps

1. Run the basic tests to ensure everything works
2. Try the interactive mode with the BERT paper
3. Test with your own research papers
4. Check PROJECT_GOALS.md for development progress
5. Contribute improvements or report issues

## Development

To contribute to the project:

1. Check PROJECT_GOALS.md for current status and next tasks
2. Run tests before making changes: `python test_basic.py`
3. Follow the existing code structure and documentation style
4. Update PROJECT_GOALS.md with your progress
