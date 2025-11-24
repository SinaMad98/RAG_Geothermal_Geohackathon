import pdfplumber
import ollama
import json
import re
from typing import List, Dict, Any, Optional

class TechSpecsExtractor:
    """
    Extracts technical specifications (Casing, Mud) from PDF reports using
    table extraction and LLM parsing.
    """

    def extract_tables_to_markdown(self, pdf_path: str, keywords: List[str]) -> str:
        """
        Scans a PDF for pages containing specific keywords, extracts tables found on those pages,
        and converts them into a Markdown string.

        Args:
            pdf_path (str): Path to the PDF file.
            keywords (List[str]): List of keywords to search for on pages (e.g., ["Casing", "Mud"]).

        Returns:
            str: Combined Markdown representation of the extracted tables.
        """
        markdown_output = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    
                    # Check if any keyword is present on the page (case-insensitive)
                    if any(keyword.lower() in text.lower() for keyword in keywords):
                        tables = page.extract_tables()
                        
                        for table in tables:
                            if not table:
                                continue
                            
                            # Clean table data: replace None with empty string
                            cleaned_table = [[cell if cell is not None else "" for cell in row] for row in table]
                            
                            if not cleaned_table:
                                continue

                            # Create header
                            header = cleaned_table[0]
                            # Format header row
                            markdown_table = "| " + " | ".join(str(x).replace("\n", " ") for x in header) + " |\n"
                            # Add separator row
                            markdown_table += "| " + " | ".join(["---"] * len(header)) + " |\n"
                            
                            # Create data rows
                            for row in cleaned_table[1:]:
                                markdown_table += "| " + " | ".join(str(x).replace("\n", " ") for x in row) + " |\n"
                            
                            markdown_output.append(markdown_table)
                            markdown_output.append("\n")
                            
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""

        return "\n".join(markdown_output)

    def parse_specs_with_llm(self, markdown_content: str) -> Dict[str, Any]:
        """
        Uses an LLM to parse technical specifications from Markdown table content.

        Args:
            markdown_content (str): Markdown string containing table data.

        Returns:
            Dict[str, Any]: Dictionary containing 'casing_data' and 'mud_data'.
        """
        if not markdown_content.strip():
            return {"casing_data": [], "mud_data": []}

        prompt = f"""
        You are a Drilling Data Engineer. Analyze the following Markdown table data extracted from a well report.
        
        Extract two specific lists of data:
        1. casing_data: A list of objects containing 'size', 'depth', and 'weight'.
        2. mud_data: A list of objects containing 'type' and 'density'.

        Return the output as strictly valid JSON with the following structure:
        {{
            "casing_data": [
                {{"size": "...", "depth": "...", "weight": "..."}},
                ...
            ],
            "mud_data": [
                {{"type": "...", "density": "..."}},
                ...
            ]
        }}

        If a field is missing, use null. Do not include any explanation, only the JSON.

        Markdown Content:
        {markdown_content}
        """

        try:
            response = ollama.chat(model='llama3.1', messages=[
                {'role': 'user', 'content': prompt},
            ])
            
            content = response['message']['content']
            
            # Attempt to parse JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback: find first { and last } to handle potential markdown code blocks or extra text
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    return json.loads(json_str)
                else:
                    print("Failed to extract JSON from LLM response.")
                    return {"casing_data": [], "mud_data": []}

        except Exception as e:
            print(f"Error calling LLM: {e}")
            return {"casing_data": [], "mud_data": []}

if __name__ == "__main__":
    # Mock Markdown String for testing
    mock_markdown = """
    | Casing Size | Depth (ft) | Weight (lb/ft) |
    |---|---|---|
    | 13 3/8" | 1500 | 54.5 |
    | 9 5/8" | 4500 | 40.0 |
    | 7" | 8200 | 29.0 |
    
    | Mud Type | Density (ppg) | Viscosity |
    |---|---|---|
    | Spud Mud | 8.5 | 40 |
    | Water Based | 9.2 | 45 |
    """

    print("Testing TechSpecsExtractor with mock data...")
    extractor = TechSpecsExtractor()
    
    # We are skipping extract_tables_to_markdown as we don't have a PDF here
    # directly testing the LLM parsing part.
    
    result = extractor.parse_specs_with_llm(mock_markdown)
    
    print("\nExtracted Data:")
    print(json.dumps(result, indent=2))