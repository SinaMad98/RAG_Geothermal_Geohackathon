import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database_manager import DatabaseManager

def test_db_workflow():
    print("Initializing Database Manager...")
    db = DatabaseManager(config_path="config.yaml")
    
    # Clear DB for fresh test
    print("Resetting collection...")
    db.reset_collection()

    # 1. Mock Data (Simulating Colleague 1's output)
    mock_chunks = [
        {
            "text": "4.0 Geology\nThe formation consists primarily of sandstone interbedded with shale. The top of the reservoir was encountered at 2500m.",
            "metadata": {"section": "Geology", "page": 5, "source": "mock_report.pdf"}
        },
        {
            "text": "5.0 Casing\n13-3/8 inch casing was set at 500m. 9-5/8 inch casing was set at 1500m.",
            "metadata": {"section": "Casing", "page": 8, "source": "mock_report.pdf"}
        },
        {
            "text": "The mud weight was maintained at 1.2 sg throughout the drilling of the 12-1/4 inch hole section.",
            "metadata": {"section": "Fluids", "page": 10, "source": "mock_report.pdf"}
        }
    ]

    # 2. Store
    print("Saving mock chunks...")
    db.save_chunks(mock_chunks)

    # 3. Retrieve specific sections (Simulating what Colleague 2 needs)
    print("\nTesting Retrieval by Section (Geology):")
    geo_chunks = db.get_chunks(where={"section": "Geology"})
    print(f"Retrieved {len(geo_chunks)} chunks.")
    for chunk in geo_chunks:
        print(f" - {chunk[:50]}...")

    print("\nTesting Semantic Search ('casing depth'):")
    casing_chunks = db.get_chunks(query_text="casing depth", n_results=1)
    print(f"Retrieved {len(casing_chunks)} chunks.")
    for chunk in casing_chunks:
        print(f" - {chunk[:50]}...")

    print("\nTest Complete.")

if __name__ == "__main__":
    test_db_workflow()
