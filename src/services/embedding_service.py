import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class EmbeddingService:
    def __init__(self):
        self.embeddings = None

    def initialize(self, api_key: str):
        if not api_key or api_key == "your_google_api_key_here":
            raise Exception("Valid GOOGLE_API_KEY is required")
        
        print("Initializing Google Embeddings...")
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key
        )
        # Test
        self.embeddings.embed_query("test")
        print("✓ Google Embeddings initialized successfully")

    def get_embeddings(self):
        if not self.embeddings:
            # Try to initialize from env if not already done
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                self.initialize(api_key)
            else:
                raise Exception("Embeddings not initialized and GOOGLE_API_KEY not found")
        return self.embeddings

embedding_service = EmbeddingService()
