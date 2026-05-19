import os
import tempfile
from pypdf import PdfReader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document


class PDFProcessor:
    """Handle PDF upload, text extraction, and vector storage for RAG."""
    
    def __init__(self, persist_dir: str = "./chroma_db"):
        """
        Initialize PDF processor with persistent vector store.
        
        Args:
            persist_dir: Directory to persist Chroma database
        """
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore = None
        self.pdf_metadata = {}
    
    def extract_text_from_pdf(self, pdf_file) -> tuple[str, int]:
        """
        Extract text from uploaded PDF file.
        
        Args:
            pdf_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (full_text, page_count)
        """
        try:
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(pdf_file.getbuffer())
                tmp_path = tmp.name
            
            reader = PdfReader(tmp_path)
            page_count = len(reader.pages)
            
            text_content = []
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    text_content.append(page_text)
            
            os.unlink(tmp_path)
            
            full_text = "\n\n---PAGE BREAK---\n\n".join(text_content)
            return full_text, page_count
            
        except Exception as e:
            raise Exception(f"Failed to extract PDF text: {str(e)}")
    
    def create_vector_store(self, pdf_text: str, pdf_name: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Create embeddings and store in vector database.
        
        Args:
            pdf_text: Full extracted text from PDF
            pdf_name: Name of the PDF for metadata
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        try:
            # Split text into chunks
            chunks = self._chunk_text(pdf_text, chunk_size, chunk_overlap)
            
            # Create documents with metadata
            documents = [
                Document(
                    page_content=chunk,
                    metadata={"source": pdf_name, "chunk_index": i}
                )
                for i, chunk in enumerate(chunks)
            ]
            
            # Create or update vector store
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_dir,
                collection_name=pdf_name.replace(".pdf", "")
            )
            
            # Save metadata
            self.pdf_metadata[pdf_name] = {
                "chunk_count": len(chunks),
                "text_length": len(pdf_text)
            }
            
            return len(chunks)
            
        except Exception as e:
            raise Exception(f"Failed to create vector store: {str(e)}")
    
    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> list[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Full text to split
            chunk_size: Size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        
        return chunks
    
    def query_vector_store(self, query: str, k: int = 4) -> list[str]:
        """
        Retrieve relevant documents from vector store.
        
        Args:
            query: User query
            k: Number of results to return
            
        Returns:
            List of relevant document chunks
        """
        if not self.vectorstore:
            raise Exception("Vector store not initialized. Upload and process a PDF first.")
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            raise Exception(f"Failed to query vector store: {str(e)}")
    
    def get_pdf_context(self, query: str, k: int = 4) -> str:
        """
        Get formatted context from PDF for a query.
        
        Args:
            query: User query
            k: Number of chunks to retrieve
            
        Returns:
            Formatted context string
        """
        try:
            relevant_chunks = self.query_vector_store(query, k)
            context = "\n\n---\n\n".join(relevant_chunks)
            return context
        except Exception as e:
            raise Exception(f"Failed to get context: {str(e)}")
