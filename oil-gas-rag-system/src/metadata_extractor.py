class MetadataExtractor:
    import re
    from datetime import datetime
    from typing import Dict, Tuple

    def extract_header(self, pdf_text: str) -> Dict[str, str]:
        """
        Extracts well header information from the provided PDF text using regex.
        
        Args:
            pdf_text (str): The text content of the PDF report.
        
        Returns:
            Dict[str, str]: A dictionary containing the well name and spud date.
        """
        well_name = re.search(r'Well Name:\s*(.*)', pdf_text)
        spud_date = re.search(r'Spud Date:\s*(.*)', pdf_text)

        return {
            "well_name": well_name.group(1) if well_name else "",
            "spud_date": spud_date.group(1) if spud_date else ""
        }

    def calculate_duration(self, start_date: str, end_date: str) -> int:
        """
        Calculates the duration in days between two dates.
        
        Args:
            start_date (str): The start date in string format.
            end_date (str): The end date in string format.
        
        Returns:
            int: The number of days between the two dates.
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return (end - start).days

if __name__ == "__main__":
    # Dummy string for testing
    dummy_pdf_text = """
    Well Name: Example Well
    Spud Date: 2023-01-01
    """
    extractor = MetadataExtractor()
    header = extractor.extract_header(dummy_pdf_text)
    print(header)  # Output: {'well_name': 'Example Well', 'spud_date': '2023-01-01'}
    duration = extractor.calculate_duration("2023-01-01", "2023-01-10")
    print(duration)  # Output: 9