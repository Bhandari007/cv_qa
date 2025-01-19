import os
from dotenv import load_dotenv
import chromadb
from PyPDF2 import PdfReader



class VectorDatabase:
    def __init__(self, collection_name="my_pdf_collection", storage_path=None, 
                 chunk_size=512, chunk_overlap=128):
        # Load environment variables
        load_dotenv()
        self.storage_path = storage_path or os.getenv('STORAGE_PATH', './chromadb_storage')
        self.chroma_client = chromadb.PersistentClient(path=self.storage_path) 

        # Check if collection exists, otherwise create a new one
        if collection_name not in self.chroma_client.list_collections():
            self.collection = self.chroma_client.create_collection(name=collection_name)
        else:
            self.collection = self.chroma_client.get_collection(name=collection_name)

        print(f"Connected to ChromaDB collection: {collection_name}")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def add_pdfs(self, pdf_paths):
        """
        Adds PDFs to the ChromaDB collection with chunking and overlap.

        Args:
            pdf_paths (list): A list of paths to the PDF files.
        """
        documents = []
        ids = []
        for path in pdf_paths:
            try:
                with open(path, 'rb') as f:
                    pdf_reader = PdfReader(f)
                    text = ""
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()

                    # Chunk the text with overlap
                    chunks = self._chunk_text(text)
                    documents.extend(chunks)
                    ids.extend([f"{os.path.basename(path)}_{i}" for i in range(len(chunks))]) 

            except Exception as e:
                print(f"Error reading PDF {path}: {e}")

        self.add_documents(documents, ids)

    def _chunk_text(self, text):
        """
        Chunks the given text into smaller segments with overlap.

        Args:
            text (str): The text to be chunked.

        Returns:
            list: A list of text chunks.
        """
        chunks = []
        start = 0
        end = self.chunk_size
        while start < len(text):
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
            end = start + self.chunk_size
        return chunks

    def add_documents(self, documents, ids):
        # Add documents to the ChromaDB collection
        self.collection.add(documents=documents, ids=ids)
        print(f"Added {len(documents)} documents to the collection.")

    def query(self, query_texts, n_results=2): 
        # Query the collection
        results = self.collection.query(query_texts=query_texts, n_results=n_results)
        return results

    def get_collection(self):
        return self.collection

# Example Usage:
if __name__ == "__main__":
    # Initialize the ChromaDB manager with your desired collection
    chroma_db_manager = ChromaDBManager(collection_name="my_pdf_collection")

    # Add PDFs to the collection
    pdf_paths = ["/home/pa1/Documents/chatbot/data/1901841_RESUME.pdf"] 
    chroma_db_manager.add_pdfs(pdf_paths)
    print(chroma_db_manager.query("name of the person in the CV", n_results=1))