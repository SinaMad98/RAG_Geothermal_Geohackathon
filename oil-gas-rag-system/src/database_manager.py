import chromadb
from chromadb.config import Settings
import yaml
import os
from typing import List, Dict, Any
import uuid

class DatabaseManager:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.client = chromadb.PersistentClient(path=self.config.get("chroma_db_path", "./chroma_db"))
        self.collection = self.client.get_or_create_collection(name=self.config.get("collection_name", "well_reports"))

    def _load_config(self, config_path: str) -> dict:
        if not os.path.exists(config_path):
            # Fallback if config file is missing, though it should exist
            return {}
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def save_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Stores chunks into ChromaDB.
        Expected format for chunks:
        [
            {"text": "...", "metadata": {"section": "Geology", "page": 5, "source": "report.pdf"}}
        ]
        """
        if not chunks:
            return

        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:
            text = chunk.get("text", "")
            metadata = chunk.get("metadata", {})
            
            # Ensure metadata values are strings, ints, floats, or bools (Chroma requirement)
            # We might need to flatten or clean metadata if it's complex
            clean_metadata = {k: v for k, v in metadata.items() if isinstance(v, (str, int, float, bool))}

            documents.append(text)
            metadatas.append(clean_metadata)
            ids.append(str(uuid.uuid4()))

        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Saved {len(documents)} chunks to database.")

    def get_chunks(self, query_text: str = "", n_results: int = 5, where: Dict[str, Any] = None) -> List[str]:
        """
        Retrieves chunks based on semantic search or metadata filtering.
        
        Args:
            query_text: The text to search for (semantic search).
            n_results: Number of results to return.
            where: Metadata filter (e.g., {"section": "Geology"}).
        
        Returns:
            List of text chunks.
        """
        if not query_text and not where:
            return []

        # If query_text is empty but we have a filter, we might want to fetch by filter only.
        # ChromaDB query requires query_embeddings or query_texts usually.
        # If we just want to filter by metadata without semantic search, we can use `get`.
        
        if not query_text and where:
            results = self.collection.get(where=where, limit=n_results)
            return results['documents'] if results['documents'] else []

        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where
        )
        
        # results['documents'] is a list of lists (one list per query)
        return results['documents'][0] if results['documents'] else []

    def get_all_documents(self):
        """Helper to inspect DB content"""
        return self.collection.get()

    def reset_collection(self):
        """Clears the collection (useful for testing)"""
        self.client.delete_collection(self.config.get("collection_name", "well_reports"))
        self.collection = self.client.get_or_create_collection(name=self.config.get("collection_name", "well_reports"))
