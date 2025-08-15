#!/usr/bin/env python3
"""
Test script to verify filename handling
"""

from datetime import datetime

def test_filename():
    """Test the filename generation logic"""
    
    # Simulate the filename generation from main.py
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_news_article"
    
    print(f"Generated filename: '{filename}'")
    print(f"Filename type: {type(filename)}")
    print(f"Filename length: {len(filename)}")
    
    # Test what happens when we add .pdf
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    
    print(f"Final filename: '{filename}'")

if __name__ == "__main__":
    test_filename()
