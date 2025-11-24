"""
Specifications Extractor Module

Extracts technical specifications from Oil & Gas Well Reports.
This module can be run independently to extract well specifications.
"""

import json
from typing import Dict, Any, List


class SpecsExtractor:
    """
    Extracts technical specifications from well reports.
    
    This class provides functionality to extract well specifications including
    depths, casing details, hole sizes, and drilling fluid information.
    """
    
    def __init__(self):
        """Initialize the specifications extractor."""
        self.extracted_data = {}
    
    def extract(self, report_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extract specifications from well report.
        
        Args:
            report_data: Raw report data (if None, uses mock data)
            
        Returns:
            Dictionary containing extracted specifications
        """
        if report_data is None:
            # Use mock data for demonstration
            return self._extract_mock_data()
        
        # Real extraction logic would go here
        # This would parse the actual report data
        return self._parse_specs(report_data)
    
    def _extract_mock_data(self) -> Dict[str, Any]:
        """
        Generate mock specifications for testing and demonstration.
        
        Returns:
            Dictionary containing mock specifications data
        """
        mock_specs = {
            "specs": {
                "total_depth": 12500,
                "measured_depth": 12800,
                "true_vertical_depth": 12450,
                "casing": [
                    {
                        "type": "surface",
                        "diameter": 13.375,
                        "depth": 1200,
                        "weight": 68
                    },
                    {
                        "type": "intermediate",
                        "diameter": 9.625,
                        "depth": 8500,
                        "weight": 47
                    },
                    {
                        "type": "production",
                        "diameter": 7.0,
                        "depth": 12400,
                        "weight": 26
                    }
                ],
                "hole_size": 8.5,
                "drilling_fluid_type": "Water-based mud"
            }
        }
        
        self.extracted_data = mock_specs
        return mock_specs
    
    def _parse_specs(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse specifications from actual report data.
        
        Args:
            report_data: Raw report data
            
        Returns:
            Dictionary containing parsed specifications
        """
        # Implementation for parsing real data would go here
        specs = {
            "specs": {
                "total_depth": report_data.get("total_depth", 0),
                "measured_depth": report_data.get("measured_depth", 0),
                "true_vertical_depth": report_data.get("true_vertical_depth", 0),
                "casing": report_data.get("casing", []),
                "hole_size": report_data.get("hole_size", 0),
                "drilling_fluid_type": report_data.get("drilling_fluid_type", "")
            }
        }
        
        self.extracted_data = specs
        return specs
    
    def to_json(self) -> str:
        """
        Convert extracted data to JSON string.
        
        Returns:
            JSON string representation of extracted data
        """
        return json.dumps(self.extracted_data, indent=2)


def main():
    """
    Main function to run specifications extractor independently.
    """
    print("=" * 60)
    print("Oil & Gas Well Report - Specifications Extractor")
    print("=" * 60)
    
    extractor = SpecsExtractor()
    specs = extractor.extract()
    
    print("\nExtracted Specifications:")
    print(extractor.to_json())
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
