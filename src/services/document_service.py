from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MemoryVectorStore
import os
import shutil

class DocumentService:
    def __init__(self):
        self.vector_store = None

    async def process_pdf(self, file_path: str, embeddings):
        try:
            # Load PDF
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            if not docs:
                raise Exception("PDF appears to be empty or unreadable")
            
            print(f"Extracted {len(docs)} pages from PDF")

            # Split text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(docs)
            print(f"Split into {len(splits)} chunks")

            # Create vector store
            self.vector_store = MemoryVectorStore.from_documents(splits, embeddings)
            print("✓ Vector store created")

            return len(splits)
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise e

    async def search_similar_documents(self, query: str, k: int = 4):
        if not self.vector_store:
            raise Exception("No document uploaded. Please upload a PDF first.")
        
        relevant_docs = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in relevant_docs]

    def has_document(self):
        return self.vector_store is not None

    def clear_document(self):
        self.vector_store = None

document_service = DocumentService()
