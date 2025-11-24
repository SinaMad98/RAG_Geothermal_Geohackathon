import re
import json
import ollama
from datetime import datetime
from typing import Dict, Any, Optional

class MetadataExtractor:
    def __init__(self, model: str = "llama3.1"):
        self.model = model

    def extract_header(self, header_text: str) -> Dict[str, Any]:
        """
        Extracts well header information (Well Name, Operator) using Llama 3.1
        and dates using Regex.
        
        Args:
            header_text (str): The text content from the first few pages of the PDF.
        
        Returns:
            Dict[str, Any]: A dictionary containing well_name, operator, and spud_date.
        """
        # 1. Regex for Spud Date (Priority: Regex)
        # Patterns: YYYY-MM-DD, DD-MM-YYYY, DD/MM/YYYY
        date_pattern = r'(?i)spud date[:\s]+(\d{4}-\d{2}-\d{2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        spud_match = re.search(date_pattern, header_text)
        spud_date = spud_match.group(1) if spud_match else None

        # 2. LLM for Text Extraction (Well Name, Operator)
        # We use the LLM because these fields are often formatted inconsistently.
        prompt = f"""
        You are a data extraction assistant. Extract the 'Operator Name' and 'Well Name' from the text below.
        Return ONLY a valid JSON object with keys "operator" and "well_name". Do not add any markdown formatting or explanation.

        Text:
        {header_text[:3000]}
        """

        well_name = "Unknown"
        operator = "Unknown"

        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            content = response['message']['content'].strip()
            
            # Attempt to parse JSON
            # Find the first '{' and last '}' to handle potential chatty output
            start_idx = content.find('{')
            end_idx = content.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx+1]
                data = json.loads(json_str)
                well_name = data.get("well_name", "Unknown")
                operator = data.get("operator", "Unknown")
            
        except Exception as e:
            print(f"Error calling Ollama or parsing JSON: {e}")

        return {
            "well_name": well_name,
            "operator": operator,
            "spud_date": spud_date
        }

    def calculate_duration(self, start_date: str, end_date: str) -> int:
        """
        Calculates the duration in days between two dates.
        Handles common date formats.
        
        Args:
            start_date (str): The start date string.
            end_date (str): The end date string.
        
        Returns:
            int: The number of days between the two dates.
        """
        formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"]
        
        start = None
        end = None
        
        for fmt in formats:
            try:
                if not start:
                    start = datetime.strptime(start_date, fmt)
                if not end:
                    end = datetime.strptime(end_date, fmt)
            except ValueError:
                continue
                
        if start and end:
            return abs((end - start).days)
        else:
            # Fallback or error handling
            return 0

if __name__ == "__main__":
    # Mock data for testing
    dummy_text = """
    DRILLING REPORT
    Operator: Big Oil Corp
    Well Name: Deep Earth 1
    Spud Date: 2023-05-15
    """
    
    extractor = MetadataExtractor()
    
    # Note: This will fail if Ollama is not running or model is not pulled.
    # For testing purposes in this environment, we might see an error print.
    print("Running extraction...")
    result = extractor.extract_header(dummy_text)
    print("Extracted:", result)
    
    days = extractor.calculate_duration("2023-01-01", "2023-01-10")
    print(f"Duration: {days} days")
