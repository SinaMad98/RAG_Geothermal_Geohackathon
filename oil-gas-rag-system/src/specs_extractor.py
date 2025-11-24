class SpecsExtractor:
    """Extracts specifications from Markdown tables for Oil & Gas Well Reports using Llama 3.1 via Ollama."""

    # Mock Data: A raw markdown string of a casing table for testing
    mock_data = """
    | Size | Depth |
    |------|-------|
    | 9.5  | 1000  |
    | 7.0  | 2000  |
    | 5.5  | 3000  |
    """

    def extract_casing(self, markdown_table_text: str) -> list:
        """
        Extracts casing information from a Markdown table.

        Args:
            markdown_table_text (str): The Markdown table text containing casing information.

        Returns:
            list: A list of dictionaries containing casing size and depth.
        """
        lines = markdown_table_text.strip().split('\n')[2:]  # Skip header
        casing_list = []

        for line in lines:
            size, depth = line.split('|')[1:3]  # Extract size and depth
            casing_list.append({
                "size": size.strip(),
                "depth": int(depth.strip())
            })

        return casing_list

if __name__ == "__main__":
    extractor = SpecsExtractor()
    result = extractor.extract_casing(SpecsExtractor.mock_data)
    print(result)  # For testing purposes