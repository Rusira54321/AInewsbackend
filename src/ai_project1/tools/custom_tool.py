from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from fpdf import FPDF
from datetime import datetime

class PDFWriterTool(BaseTool):
    name :str = "PDF Writer Tool"
    description :str = "Writes text content into a PDF file"

    def _run(self,filename:str,content: str):
        print(f"DEBUG: PDFWriterTool received filename: '{filename}'")
        print(f"DEBUG: PDFWriterTool received content length: {len(content)} characters")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in content.split("\n"):
            pdf.multi_cell(0, 10, line)
        
        # Get the absolute path to the news folder within the project
        # Navigate from current file location to project root, then to news folder
        current_dir = os.path.dirname(os.path.abspath(__file__))  # tools folder
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))  # go up 3 levels to project root
        news_folder = os.path.join(project_root, "news")
        
        # Create news folder if it doesn't exist
        os.makedirs(news_folder, exist_ok=True)
        
        # Clean up the filename - remove any path components and ensure it ends with .pdf
        clean_filename = os.path.basename(filename)  # Remove any path components
        if not clean_filename.endswith('.pdf'):
            clean_filename += '.pdf'
        
        print(f"DEBUG: Clean filename: '{clean_filename}'")
        print(f"DEBUG: News folder: '{news_folder}'")
        
        # Create the full PDF file path
        pdf_file_path = os.path.join(news_folder, clean_filename)
        print(f"DEBUG: Final PDF path: '{pdf_file_path}'")
        
        pdf.output(pdf_file_path)

        return f"PDF saved at {pdf_file_path}"