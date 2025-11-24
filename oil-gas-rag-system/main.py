from src.metadata_extractor import MetadataExtractor
from src.specs_extractor import TechSpecsExtractor
from src.geology_extractor import GeologyExtractor
import json

def process_report(pdf_path: str) -> dict:
    # Placeholder for PDF text extraction logic
    # In a real scenario, we would read the PDF here.
    # For this test, we use a dummy text that simulates a report content.
    pdf_text = """
    WELL COMPLETION REPORT
    Operator Name: Geothermal X
    Well Name: GT-1
    Spud Date: 2023-01-15
    
    ...
    
    4. Geology
    The formation consisted primarily of sandstone and shale.
    Severe lost circulation was encountered at 3000 ft.
    5.0 Drilling Fluids
    """

    # Extract metadata
    metadata_extractor = MetadataExtractor()
    header = metadata_extractor.extract_header(pdf_text)
    # Assuming end date is today or extracted elsewhere. Using fixed date for test.
    # Handle case where spud_date might be None
    spud_date = header.get('spud_date')
    if not spud_date:
        spud_date = "2023-01-01" # Fallback for duration calc
        
    duration = metadata_extractor.calculate_duration(spud_date, "2023-02-15")
    header['duration_days'] = duration

    # Extract specs
    # Since we don't have a real PDF to extract tables from, we use mock markdown data
    # that would have been returned by extract_tables_to_markdown
    specs_extractor = TechSpecsExtractor()
    
    mock_markdown = """
    | Casing Size | Depth (ft) | Weight (lb/ft) |
    |---|---|---|
    | 13 3/8" | 1500 | 54.5 |
    | 9 5/8" | 4500 | 40.0 |
    
    | Mud Type | Density (ppg) |
    |---|---|
    | Spud Mud | 8.5 |
    """
    
    # In production: markdown = specs_extractor.extract_tables_to_markdown(pdf_path, ["Casing", "Mud"])
    specs = specs_extractor.parse_specs_with_llm(mock_markdown)

    # Extract geology
    geology_extractor = GeologyExtractor()
    geology_section = geology_extractor.get_geology_section(pdf_text)
    issues = geology_extractor.summarize_problems(geology_section)

    # Merge results
    well_data = {
        "header": header,
        "specs": specs,
        "geology": {
            "issues": issues,
            "gas_peak": "Mock gas peak"  # Placeholder for actual gas peak data
        }
    }

    return well_data

if __name__ == "__main__":
    pdf_path = "dummy_path.pdf"
    result = process_report(pdf_path)
    print(json.dumps(result, indent=4))