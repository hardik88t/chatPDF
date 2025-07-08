"""
PDF processing module for extracting and preprocessing text from research papers
"""
import PyPDF2
import pdfplumber
from typing import List, Dict, Optional
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF text extraction and preprocessing"""
    
    def __init__(self):
        self.text_content = ""
        self.pages = []
        
    def extract_text_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2 (fallback method)"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting text with PyPDF2: {e}")
            return ""
    
    def extract_text_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber (primary method)"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber: {e}")
            return ""
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF using the best available method"""
        logger.info(f"Extracting text from {pdf_path}")
        
        # Try pdfplumber first (better quality)
        text = self.extract_text_pdfplumber(pdf_path)
        
        # Fallback to PyPDF2 if pdfplumber fails
        if not text.strip():
            logger.warning("pdfplumber failed, trying PyPDF2")
            text = self.extract_text_pypdf2(pdf_path)
        
        if not text.strip():
            raise ValueError(f"Could not extract text from {pdf_path}")
        
        self.text_content = text
        return text
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers (basic patterns)
        text = re.sub(r'\n\d+\n', '\n', text)
        
        # Fix common OCR issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between words
        
        # Remove excessive newlines
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict]:
        """Split text into overlapping chunks for processing"""
        if not text:
            return []
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings near the chunk boundary
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size // 2:
                    end = sentence_end + 1
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'start_pos': start,
                    'end_pos': end
                })
                chunk_id += 1
            
            # Move start position with overlap
            start = end - overlap
            
        logger.info(f"Created {len(chunks)} text chunks")
        return chunks
    
    def process_pdf(self, pdf_path: str, chunk_size: int = 1000, overlap: int = 200) -> Dict:
        """Complete PDF processing pipeline"""
        try:
            # Extract text
            raw_text = self.extract_text(pdf_path)
            
            # Clean text
            clean_text = self.clean_text(raw_text)
            
            # Create chunks
            chunks = self.chunk_text(clean_text, chunk_size, overlap)
            
            return {
                'success': True,
                'raw_text': raw_text,
                'clean_text': clean_text,
                'chunks': chunks,
                'total_chars': len(clean_text),
                'num_chunks': len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
