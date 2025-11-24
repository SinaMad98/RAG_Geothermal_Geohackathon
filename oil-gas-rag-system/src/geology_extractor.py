class GeologyExtractor:
    def get_geology_section(self, full_text: str) -> str:
        """
        Extracts the geology section from the full text of the well report.
        
        This method looks for the substring starting with "4. Geology" and ending at "5.0".
        
        Args:
            full_text (str): The complete text of the well report.
        
        Returns:
            str: The extracted geology section.
        """
        start_index = full_text.find("4. Geology")
        end_index = full_text.find("5.0", start_index)
        if start_index != -1 and end_index != -1:
            return full_text[start_index:end_index].strip()
        return ""

    def summarize_problems(self, section_text: str) -> str:
        """
        Summarizes drilling problems from the geology section.
        
        This method mocks a call to ollama.chat to ask about drilling problems.
        
        Args:
            section_text (str): The text of the geology section.
        
        Returns:
            str: A mock response indicating drilling problems.
        """
        # Mocking the call to ollama.chat
        return "Mock response: Drilling problems identified include issues with gas peaks and unstable formations."