"""
Oil & Gas Well Report Data Extraction - Main Integration Module

This module integrates all extractor modules (metadata, specifications, and geology)
and merges their JSON outputs into a complete well report data structure.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add src directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from metadata_extractor import MetadataExtractor
from specs_extractor import SpecsExtractor
from geology_extractor import GeologyExtractor


class WellReportExtractor:
    """
    Main class that orchestrates all extraction modules.
    
    This class integrates the metadata, specifications, and geology extractors
    to produce a complete well report data structure.
    """
    
    def __init__(self):
        """Initialize the well report extractor with all sub-extractors."""
        self.metadata_extractor = MetadataExtractor()
        self.specs_extractor = SpecsExtractor()
        self.geology_extractor = GeologyExtractor()
        self.complete_data = {}
    
    def extract_all(self, report_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extract all data from well report using all extractors.
        
        Args:
            report_data: Raw report data (if None, uses mock data from all extractors)
            
        Returns:
            Complete dictionary containing all extracted data
        """
        print("Extracting metadata...")
        metadata = self.metadata_extractor.extract(report_data)
        
        print("Extracting specifications...")
        specs = self.specs_extractor.extract(report_data)
        
        print("Extracting geological data...")
        geology = self.geology_extractor.extract(report_data)
        
        # Merge all extracted data
        self.complete_data = self._merge_data(metadata, specs, geology)
        
        return self.complete_data
    
    def _merge_data(self, metadata: Dict[str, Any], 
                    specs: Dict[str, Any], 
                    geology: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge data from all extractors into a single structure.
        
        Args:
            metadata: Extracted metadata
            specs: Extracted specifications
            geology: Extracted geology data
            
        Returns:
            Merged complete data structure
        """
        merged_data = {}
        
        # Merge all sections
        if "header" in metadata:
            merged_data["header"] = metadata["header"]
        
        if "specs" in specs:
            merged_data["specs"] = specs["specs"]
        
        if "geology" in geology:
            merged_data["geology"] = geology["geology"]
        
        return merged_data
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert complete extracted data to JSON string.
        
        Args:
            indent: Number of spaces for JSON indentation
            
        Returns:
            JSON string representation of complete data
        """
        return json.dumps(self.complete_data, indent=indent)
    
    def save_to_file(self, filepath: str) -> None:
        """
        Save extracted data to a JSON file.
        
        Args:
            filepath: Path where the JSON file should be saved
        """
        with open(filepath, 'w') as f:
            f.write(self.to_json())
        print(f"\nData saved to: {filepath}")


def main():
    """
    Main function to run the complete well report extraction process.
    """
    print("=" * 70)
    print("Oil & Gas Well Report - Complete Data Extraction")
    print("=" * 70)
    print("\nIntegrating all extraction modules...\n")
    
    # Create main extractor instance
    extractor = WellReportExtractor()
    
    # Extract all data (using mock data for demonstration)
    complete_data = extractor.extract_all()
    
    # Display results
    print("\n" + "=" * 70)
    print("Complete Extracted Data:")
    print("=" * 70)
    print(extractor.to_json())
    
    # Optionally save to file
    output_file = "extracted_well_data.json"
    extractor.save_to_file(output_file)
    
    print("\n" + "=" * 70)
    print("Extraction Complete!")
    print("=" * 70)
    
    # Summary statistics
    print("\nExtraction Summary:")
    print(f"  - Header fields extracted: {len(complete_data.get('header', {}))}")
    print(f"  - Specification fields extracted: {len(complete_data.get('specs', {}))}")
    print(f"  - Geological formations found: {len(complete_data.get('geology', {}).get('formations', []))}")
    print(f"  - Hydrocarbon shows recorded: {len(complete_data.get('geology', {}).get('hydrocarbon_shows', []))}")


if __name__ == "__main__":
    main()
