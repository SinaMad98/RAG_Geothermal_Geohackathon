# RAG_Geothermal_Geohackathon

## Oil & Gas Well Report Data Extraction

A Python project for extracting structured data from Oil & Gas Well Reports. This project provides modular extractors for metadata, specifications, and geological information.

## Project Structure

```
RAG_Geothermal_Geohackathon/
├── schemas/
│   └── well_data.json          # JSON schema defining the data contract
├── src/
│   ├── __init__.py             # Package initialization
│   ├── metadata_extractor.py  # Extracts header/metadata information
│   ├── specs_extractor.py     # Extracts technical specifications
│   └── geology_extractor.py   # Extracts geological data
├── main.py                     # Main integration module
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Features

- **Modular Design**: Three independent extractor modules that can run standalone or integrated
- **JSON Schema Contract**: Well-defined data structure for consistency
- **Mock Data**: Each module includes mock data for testing and demonstration
- **Complete Integration**: Main module combines all extractors and merges outputs

## Data Schema

The JSON schema defines three main sections:

1. **Header**: Well identification, location, operator, and key dates
2. **Specs**: Technical specifications including depths, casing, and drilling details
3. **Geology**: Geological formations, lithology, and hydrocarbon shows

## Installation

```bash
# Clone the repository
git clone https://github.com/SinaMad98/RAG_Geothermal_Geohackathon.git
cd RAG_Geothermal_Geohackathon

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run Individual Extractors

Each extractor can be run independently:

```bash
# Extract metadata only
python src/metadata_extractor.py

# Extract specifications only
python src/specs_extractor.py

# Extract geological data only
python src/geology_extractor.py
```

### Run Complete Integration

Run the main module to extract and merge all data:

```bash
python main.py
```

This will:
1. Extract data from all three modules
2. Merge the JSON outputs
3. Display the complete data structure
4. Save the result to `extracted_well_data.json`

## Example Output

```json
{
  "header": {
    "well_name": "Discovery Well #1",
    "well_id": "API-42-123-45678",
    "operator": "Example Energy Corporation",
    ...
  },
  "specs": {
    "total_depth": 12500,
    "measured_depth": 12800,
    ...
  },
  "geology": {
    "formations": [...],
    "hydrocarbon_shows": [...],
    ...
  }
}
```

## Development

### Extending the Extractors

To add real data extraction logic, modify the `_parse_*` methods in each extractor class. The mock data demonstrates the expected output structure.

### Adding New Fields

1. Update the JSON schema in `schemas/well_data.json`
2. Update the corresponding extractor module
3. Test with the integrated main module

## License

This project is part of the RAG Geothermal Geohackathon.