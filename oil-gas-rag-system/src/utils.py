import fitz  # PyMuPDF
import re
from typing import List, Dict, Any

class PDFIngestor:
    """
    Handles the ingestion of PDF documents, extracting text and tables,
    and chunking them by section.
    Requires pymupdf>=1.24.0 for table.to_markdown()
    """
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)

    def parse(self) -> List[Dict[str, Any]]:
        """
        Parses the PDF, extracting text and converting tables to Markdown.
        Returns a list of document chunks with metadata.
        """
        chunks = []
        current_section = "Header"
        
        for page_num, page in enumerate(self.doc):
            # 1. Detect and extract tables
            tables = page.find_tables()
            table_markdowns = []
            
            # We use redaction to remove the table text from the main text flow
            # so we don't have duplicates when we append the markdown.
            for table in tables:
                # Get markdown before redaction
                md = table.to_markdown()
                table_markdowns.append(md)
                
                # Redact the table area to remove its raw text
                page.add_redact_annot(table.bbox)
            
            # Apply redactions to clean the page text
            page.apply_redactions()
            
            # 2. Extract remaining text
            text = page.get_text()
            
            # 3. Detect Section Headers (Simple Heuristic)
            # Looking for lines starting with "X.Y Title"
            lines = text.split('\n')
            for line in lines:
                # Regex for "4.0 Geology" or "4. Geology"
                match = re.match(r'^(\d+(\.\d+)*)\s+([A-Z][a-zA-Z\s]+)', line.strip())
                if match:
                    current_section = f"{match.group(1)} {match.group(3)}"
            
            # 4. Combine text and tables
            # Appending tables at the end of the page text for now
            full_page_text = text + "\n\n" + "\n\n".join(table_markdowns)
            
            chunk = {
                "text": full_page_text,
                "metadata": {
                    "source": self.pdf_path,
                    "page": page_num + 1,
                    "section": current_section
                }
            }
            chunks.append(chunk)
            
        return chunks

    def close(self):
        self.doc.close()

    def get_header_text(self, max_pages: int = 3) -> str:
        """
        Extracts text from the first few pages for header analysis.
        """
        text = ""
        for i, page in enumerate(self.doc):
            if i >= max_pages:
                break
            text += page.get_text() + "\n"
        return text

def load_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Helper function to load and parse a PDF.
    """
    ingestor = PDFIngestor(pdf_path)
    try:
        return ingestor.parse()
    finally:
        ingestor.close()
