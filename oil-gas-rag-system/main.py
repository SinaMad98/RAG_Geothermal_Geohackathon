from src.metadata_extractor import MetadataExtractor
from src.specs_extractor import SpecsExtractor
from src.geology_extractor import GeologyExtractor
import json

def process_report(pdf_path: str) -> dict:
    # Placeholder for PDF text extraction logic
    pdf_text = "Dummy PDF text for testing."  # Replace with actual PDF extraction logic

    # Extract metadata
    metadata_extractor = MetadataExtractor()
    header = metadata_extractor.extract_header(pdf_text)
    duration = metadata_extractor.calculate_duration(header['spud_date'], "2023-10-01")  # Example end date
    header['duration_days'] = duration

    # Extract specs
    specs_extractor = SpecsExtractor()
    specs = specs_extractor.extract_casing(SpecsExtractor.MOCK_DATA)

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
    pdf_path = "path/to/well_report.pdf"  # Replace with actual PDF path
    result = process_report(pdf_path)
    print(json.dumps(result, indent=4))