"""
Command-line interface for ChatPDF clone
"""
import click
import os
import sys
from pdf_processor import PDFProcessor
from ai_handler import AIHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatPDFCLI:
    """Command-line interface for the ChatPDF application"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.ai_handler = AIHandler()
        self.current_pdf_data = None
        self.current_pdf_path = None
    
    def load_pdf(self, pdf_path: str) -> bool:
        """Load and process a PDF file"""
        if not os.path.exists(pdf_path):
            click.echo(f"Error: PDF file '{pdf_path}' not found.", err=True)
            return False
        
        click.echo(f"Loading PDF: {pdf_path}")
        
        try:
            # Process the PDF
            result = self.pdf_processor.process_pdf(pdf_path)
            
            if result['success']:
                self.current_pdf_data = result
                self.current_pdf_path = pdf_path
                
                click.echo(f"✓ PDF loaded successfully!")
                click.echo(f"  - Total characters: {result['total_chars']:,}")
                click.echo(f"  - Text chunks: {result['num_chunks']}")
                return True
            else:
                click.echo(f"Error processing PDF: {result['error']}", err=True)
                return False
                
        except Exception as e:
            click.echo(f"Error loading PDF: {e}", err=True)
            return False
    
    def ask_question(self, question: str) -> None:
        """Process a question about the loaded PDF"""
        if not self.current_pdf_data:
            click.echo("Error: No PDF loaded. Please load a PDF first.", err=True)
            return
        
        click.echo(f"\n🤔 Question: {question}")
        click.echo("🔍 Processing...")
        
        try:
            # Query the AI handler
            result = self.ai_handler.query(question, self.current_pdf_data['chunks'])
            
            if result['success']:
                click.echo(f"\n🤖 Answer ({result['query_type']} query):")
                click.echo("-" * 50)
                click.echo(result['answer'])
                click.echo("-" * 50)
                click.echo(f"📊 Used {result['chunks_used']} text chunks, {result['prompt_tokens']} tokens")
            else:
                click.echo(f"Error: {result['error']}", err=True)
                
        except Exception as e:
            click.echo(f"Error processing question: {e}", err=True)
    
    def interactive_mode(self):
        """Start interactive question-answering session"""
        if not self.current_pdf_data:
            click.echo("Error: No PDF loaded. Please load a PDF first.", err=True)
            return
        
        click.echo(f"\n🎯 Interactive mode started for: {os.path.basename(self.current_pdf_path)}")
        click.echo("Type your questions (or 'quit' to exit):")
        click.echo("-" * 50)
        
        while True:
            try:
                question = input("\n❓ Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    click.echo("👋 Goodbye!")
                    break
                
                if not question:
                    continue
                
                self.ask_question(question)
                
            except KeyboardInterrupt:
                click.echo("\n👋 Goodbye!")
                break
            except EOFError:
                break

@click.group()
def cli():
    """ChatPDF Clone - AI-powered PDF question answering system"""
    pass

@cli.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--question', '-q', help='Ask a single question')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive mode')
def chat(pdf_path, question, interactive):
    """Chat with a PDF file"""
    app = ChatPDFCLI()
    
    # Load the PDF
    if not app.load_pdf(pdf_path):
        sys.exit(1)
    
    if question:
        # Single question mode
        app.ask_question(question)
    elif interactive:
        # Interactive mode
        app.interactive_mode()
    else:
        # Default to interactive mode
        app.interactive_mode()

@cli.command()
@click.argument('pdf_path', type=click.Path(exists=True))
def test(pdf_path):
    """Run predefined test questions on a PDF"""
    app = ChatPDFCLI()
    
    # Load the PDF
    if not app.load_pdf(pdf_path):
        sys.exit(1)
    
    # Determine test questions based on PDF name
    pdf_name = os.path.basename(pdf_path).lower()
    
    if 'bert' in pdf_name:
        test_questions = [
            "What kind of neural network architecture is used in this paper?",
            "What datasets have been used for evaluation?",
            "What are the main discoveries of this paper?",
            "What is the key insight of the proposed method?"
        ]
    else:
        # Generic test questions for other papers
        test_questions = [
            "What is the main contribution of this paper?",
            "What methodology is proposed?",
            "What are the key findings?",
            "What datasets or experiments are mentioned?"
        ]
    
    click.echo(f"\n🧪 Running test questions for: {os.path.basename(pdf_path)}")
    click.echo("=" * 60)
    
    for i, question in enumerate(test_questions, 1):
        click.echo(f"\n📝 Test Question {i}:")
        app.ask_question(question)
        click.echo("\n" + "=" * 60)

@cli.command()
def info():
    """Show system information"""
    click.echo("ChatPDF Clone - System Information")
    click.echo("-" * 40)
    click.echo(f"Python version: {sys.version}")
    click.echo("Dependencies:")
    
    try:
        import google.generativeai
        click.echo("  ✓ google-generativeai")
    except ImportError:
        click.echo("  ✗ google-generativeai (missing)")
    
    try:
        import PyPDF2
        click.echo("  ✓ PyPDF2")
    except ImportError:
        click.echo("  ✗ PyPDF2 (missing)")
    
    try:
        import pdfplumber
        click.echo("  ✓ pdfplumber")
    except ImportError:
        click.echo("  ✗ pdfplumber (missing)")

if __name__ == '__main__':
    cli()
