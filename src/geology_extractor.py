"""
Geology Extractor Module

Extracts geological information from Oil & Gas Well Reports.
This module can be run independently to extract geological data.
"""

import json
from typing import Dict, Any, List


class GeologyExtractor:
    """
    Extracts geological information from well reports.
    
    This class provides functionality to extract geological data including
    formations encountered, lithology, hydrocarbon shows, and reservoir properties.
    """
    
    def __init__(self):
        """Initialize the geology extractor."""
        self.extracted_data = {}
    
    def extract(self, report_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extract geological information from well report.
        
        Args:
            report_data: Raw report data (if None, uses mock data)
            
        Returns:
            Dictionary containing extracted geological data
        """
        if report_data is None:
            # Use mock data for demonstration
            return self._extract_mock_data()
        
        # Real extraction logic would go here
        # This would parse the actual report data
        return self._parse_geology(report_data)
    
    def _extract_mock_data(self) -> Dict[str, Any]:
        """
        Generate mock geological data for testing and demonstration.
        
        Returns:
            Dictionary containing mock geology data
        """
        mock_geology = {
            "geology": {
                "formations": [
                    {
                        "name": "Wolfcamp Formation",
                        "top_depth": 8500,
                        "bottom_depth": 10200,
                        "lithology": "Shale",
                        "porosity": 8.5,
                        "permeability": 0.0015
                    },
                    {
                        "name": "Bone Spring Formation",
                        "top_depth": 10200,
                        "bottom_depth": 11800,
                        "lithology": "Limestone",
                        "porosity": 12.3,
                        "permeability": 0.85
                    },
                    {
                        "name": "Delaware Mountain Group",
                        "top_depth": 11800,
                        "bottom_depth": 12500,
                        "lithology": "Sandstone",
                        "porosity": 15.7,
                        "permeability": 25.4
                    }
                ],
                "hydrocarbon_shows": [
                    {
                        "depth": 9850,
                        "type": "oil",
                        "description": "Light oil show with gas cut, fluorescence observed"
                    },
                    {
                        "depth": 11500,
                        "type": "gas",
                        "description": "Strong gas show, significant increase in background gas"
                    },
                    {
                        "depth": 12100,
                        "type": "oil",
                        "description": "Oil show in sandstone, good porosity and permeability"
                    }
                ],
                "target_formation": "Bone Spring Formation"
            }
        }
        
        self.extracted_data = mock_geology
        return mock_geology
    
    def _parse_geology(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse geological information from actual report data.
        
        Args:
            report_data: Raw report data
            
        Returns:
            Dictionary containing parsed geological data
        """
        # Implementation for parsing real data would go here
        geology = {
            "geology": {
                "formations": report_data.get("formations", []),
                "hydrocarbon_shows": report_data.get("hydrocarbon_shows", []),
                "target_formation": report_data.get("target_formation", "")
            }
        }
        
        self.extracted_data = geology
        return geology
    
    def to_json(self) -> str:
        """
        Convert extracted data to JSON string.
        
        Returns:
            JSON string representation of extracted data
        """
        return json.dumps(self.extracted_data, indent=2)


def main():
    """
    Main function to run geology extractor independently.
    """
    print("=" * 60)
    print("Oil & Gas Well Report - Geology Extractor")
    print("=" * 60)
    
    extractor = GeologyExtractor()
    geology = extractor.extract()
    
    print("\nExtracted Geological Data:")
    print(extractor.to_json())
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
