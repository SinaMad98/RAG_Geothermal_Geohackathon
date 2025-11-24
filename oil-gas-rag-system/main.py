import json
import os
import sys

# Add src to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database_manager import DatabaseManager
from src.utils import PDFIngestor
from src.metadata_extractor import MetadataExtractor
from src.geology_extractor import GeologyExtractor
from src.specs_extractor import TechSpecsExtractor

# --- MOCKS for Colleague 1 (Ingestion) & Colleague 2 (Extraction) ---
# We keep these as fallbacks or for testing without dependencies

def mock_parse_pdf(pdf_path: str):
    """
    Colleague 1's responsibility:
    Input: PDF Path
    Output: List of chunks with metadata
    """
    print(f"[C1 Mock] Parsing PDF: {pdf_path}")
    # Simulating extracted text chunks
    return [
        {
            "text": "4.0 Geology\nThe formation consists primarily of sandstone interbedded with shale. The top of the reservoir was encountered at 2500m.",
            "metadata": {"section": "Geology", "page": 5, "source": os.path.basename(pdf_path)}
        },
        {
            "text": "5.0 Casing\n13-3/8 inch casing was set at 500m. 9-5/8 inch casing was set at 1500m.",
            "metadata": {"section": "Casing", "page": 8, "source": os.path.basename(pdf_path)}
        },
        {
            "text": "The mud weight was maintained at 1.2 sg throughout the drilling of the 12-1/4 inch hole section.",
            "metadata": {"section": "Fluids", "page": 10, "source": os.path.basename(pdf_path)}
        }
    ]

# --- Colleague 3: The Architect (Pipeline) ---

def process_well_report(pdf_path: str) -> dict:
    print(f"--- Starting Pipeline for {pdf_path} ---")
    
    # 0. Setup
    db = DatabaseManager(config_path="config.yaml")
    
    # 1. Ingest (Colleague 1)
    print("[C1] Ingesting PDF...")
    try:
        if os.path.exists(pdf_path):
            ingestor = PDFIngestor(pdf_path)
            chunks = ingestor.parse()
            ingestor.close()
            print(f"Parsed {len(chunks)} chunks from PDF.")
        else:
            print(f"PDF not found at {pdf_path}, using mock data.")
            chunks = mock_parse_pdf(pdf_path)
    except Exception as e:
        print(f"Error during ingestion: {e}. Using mock data.")
        chunks = mock_parse_pdf(pdf_path)
    
    # 2. Store (Colleague 3)
    print("[C3] Storing chunks in ChromaDB...")
    db.save_chunks(chunks)
    
    # 3. Retrieve & Extract (Colleague 3 & 2)
    print("[C3] Retrieving and Extracting Data...")
    
    # A. Header / Metadata
    # Strategy: Get the first few pages for header info
    header_chunks = db.get_chunks(where={"page": 1}, n_results=1) # Simplified: assume page 1 has header
    if not header_chunks:
        # Fallback if page metadata isn't int or query fails
        header_text = chunks[0]['text'] if chunks else ""
    else:
        header_text = header_chunks[0]
        
    metadata_extractor = MetadataExtractor()
    # Note: extract_header might fail if Ollama is down, handle gracefully?
    # For now we assume it works or prints error
    header_data = metadata_extractor.extract_header(header_text)
    
    # Computed Field: Duration
    # We need an end date. Let's assume we find it or use current date.
    # For this demo, we'll just use a fixed date or try to find 'TD Date'
    spud_date = header_data.get('spud_date')
    if spud_date:
        header_data['duration_days'] = metadata_extractor.calculate_duration(spud_date, "2023-12-31")
    else:
        header_data['duration_days'] = 0


    # B. Geology
    # Retrieve chunks tagged as "Geology"
    geo_chunks = db.get_chunks(where={"section": "Geology"}, n_results=5)
    geo_text = "\n".join(geo_chunks)
    
    geology_extractor = GeologyExtractor()
    # summarize_problems expects text
    geo_issues = geology_extractor.summarize_problems(geo_text)
    
    # C. Specs (Casing, etc.)
    # Use TechSpecsExtractor to extract tables directly from PDF if available, 
    # or use mock data if PDF is not present/readable.
    specs_extractor = TechSpecsExtractor()
    
    if os.path.exists(pdf_path):
        print("[C2] Extracting tables from PDF...")
        markdown_tables = specs_extractor.extract_tables_to_markdown(pdf_path, ["Casing", "Mud"])
    else:
        print("[C2] PDF not found, using mock markdown for specs...")
        markdown_tables = """
        | Casing Size | Depth (ft) | Weight (lb/ft) |
        |---|---|---|
        | 13 3/8" | 1500 | 54.5 |
        | 9 5/8" | 4500 | 40.0 |
        
        | Mud Type | Density (ppg) |
        |---|---|
        | Spud Mud | 8.5 |
        """
    
    specs_data = specs_extractor.parse_specs_with_llm(markdown_tables)

    # 4. Assemble Final Result
    well_data = {
        "header": header_data,
        "specs": specs_data,
        "geology": {
            "issues": [geo_issues], # summarize_problems returns a string
            "gas_peak": "N/A" # Placeholder
        }
    }
    
    print("--- Pipeline Complete ---")
    return well_data

if __name__ == "__main__":
    # Example usage
    # Ensure we have a dummy PDF or use the mock path
    report_path = "data/mock_report.pdf"
    
    # Create a dummy PDF file if it doesn't exist to test the real ingestor?
    # Or just rely on the mock fallback.
    # Let's rely on the mock fallback for now if file doesn't exist.
    
    result = process_well_report(report_path)
    print("\nFinal Result:")
    print(json.dumps(result, indent=2))
