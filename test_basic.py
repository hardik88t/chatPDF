#!/usr/bin/env python3
"""
Basic tests for ChatPDF clone functionality
"""

import os
import sys
import unittest
from pdf_processor import PDFProcessor
from ai_handler import AIHandler
from config import Config

class TestBasicFunctionality(unittest.TestCase):
    """Basic functionality tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.pdf_processor = PDFProcessor()
        self.test_pdfs = [
            'bert_research_paper.pdf',
            'ai_application_research_paper.pdf', 
            'ml_in_ai_research_paper.pdf'
        ]
    
    def test_config_validation(self):
        """Test configuration validation"""
        config = Config()
        self.assertTrue(config.validate())
        self.assertIsNotNone(config.GEMINI_API_KEY)
    
    def test_pdf_files_exist(self):
        """Test that required PDF files exist"""
        for pdf_file in self.test_pdfs:
            self.assertTrue(os.path.exists(pdf_file), f"PDF file {pdf_file} not found")
    
    def test_pdf_text_extraction(self):
        """Test PDF text extraction"""
        if os.path.exists('bert_research_paper.pdf'):
            result = self.pdf_processor.process_pdf('bert_research_paper.pdf')
            self.assertTrue(result['success'], f"PDF processing failed: {result.get('error', 'Unknown error')}")
            self.assertGreater(len(result['clean_text']), 0, "No text extracted from PDF")
            self.assertGreater(result['num_chunks'], 0, "No text chunks created")
    
    def test_text_chunking(self):
        """Test text chunking functionality"""
        sample_text = "This is a test sentence. " * 100  # Create long text
        chunks = self.pdf_processor.chunk_text(sample_text, chunk_size=200, overlap=50)
        self.assertGreater(len(chunks), 0, "No chunks created")
        self.assertIn('id', chunks[0], "Chunk missing ID")
        self.assertIn('text', chunks[0], "Chunk missing text")

class TestAIHandler(unittest.TestCase):
    """Test AI handler functionality"""
    
    def setUp(self):
        """Set up AI handler test"""
        try:
            self.ai_handler = AIHandler()
        except Exception as e:
            self.skipTest(f"Could not initialize AI handler: {e}")
    
    def test_query_classification(self):
        """Test query type classification"""
        test_cases = [
            ("What is BERT?", "direct"),
            ("Why should we use this method?", "indirect"),
            ("What references inspire this methodology?", "references")
        ]
        
        for query, expected_type in test_cases:
            classified_type = self.ai_handler.classify_query_type(query)
            self.assertEqual(classified_type, expected_type, 
                           f"Query '{query}' classified as '{classified_type}', expected '{expected_type}'")
    
    def test_token_counting(self):
        """Test token counting functionality"""
        test_text = "This is a simple test sentence."
        token_count = self.ai_handler.count_tokens(test_text)
        self.assertGreater(token_count, 0, "Token count should be greater than 0")

def run_tests():
    """Run all tests"""
    print("🧪 Running basic functionality tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestBasicFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestAIHandler))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False
    
    return True

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
