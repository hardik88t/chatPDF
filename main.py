#!/usr/bin/env python3
"""
ChatPDF Clone - Main Entry Point
AI-powered PDF question answering system using Gemini API
"""

import sys
import os
from cli import cli

def main():
    """Main entry point for the application"""
    try:
        # Run the CLI
        cli()
    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
