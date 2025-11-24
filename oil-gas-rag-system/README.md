# Oil & Gas RAG System

This project is a Local RAG (Retrieval-Augmented Generation) system designed to extract data from Oil & Gas Well Reports in PDF format. The system utilizes Python, Ollama (Llama 3.1), and ChromaDB to process and analyze well reports efficiently.

## Project Structure

The project is organized as follows:

```
oil-gas-rag-system
├── schemas
│   └── well_data.json          # JSON schema defining the structure of well data
├── src
│   ├── geology_extractor.py    # Extractor for geology-related data
│   ├── metadata_extractor.py    # Extractor for metadata from well reports
│   ├── specs_extractor.py       # Extractor for specifications from markdown tables
│   └── utils.py                 # Utility functions for PDF loading
├── .gitignore                   # Files and directories to ignore in Git
├── main.py                      # Integration script for processing reports
├── README.md                    # Project documentation
└── requirements.txt             # Project dependencies
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd oil-gas-rag-system
pip install -r requirements.txt
```

## Usage

To process a well report, run the `main.py` script with the path to the PDF file:

```bash
python main.py <path_to_pdf>
```

This will extract the relevant data from the PDF and print the results in JSON format.

## Dependencies

The project requires the following Python packages:

- fitz
- langchain
- chromadb
- ollama

Make sure to install these packages using the provided `requirements.txt`.

## Contributing

Feel free to contribute to the project by submitting issues or pull requests. For any questions or suggestions, please reach out to the development team.