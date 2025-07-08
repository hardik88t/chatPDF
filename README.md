# ChatPDF Clone

A simple question-answering system for PDF documents, similar to [chatPDF](https://www.chatpdf.com/). Upload a PDF and ask questions about its content.

## Features

The system can handle different types of questions about PDF documents:

1. **Direct questions** - Questions that can be matched directly to text in the document
   - "What is CDE?"
   - "Which datasets are used for evaluation?"

2. **Indirect questions** - Questions requiring interpretation and synthesis
   - "Why should we use the proposed method?"

3. **Reference identification** - Finding key references that inspire methodologies

## Usage

Simple command-line interface for asking questions about PDF documents.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set your Gemini API key in environment variables
3. Run: `python main.py chat your_document.pdf`

## Testing

Test with the included research papers:

**BERT Paper Questions:**
- What kind of neural network architecture is used?
- What datasets have been used for evaluation?
- What are the main discoveries?
- What is the key insight of the proposed method?

Similar questions can be asked for the other included papers.