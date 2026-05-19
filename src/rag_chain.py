from src.pdf_processor import PDFProcessor
from src.model import Model


class RAGChain:
    """RAG pipeline for PDF summarization and Q&A."""
    
    def __init__(self, model_name: str, gemini_model: str = "gemini-2.5-flash", 
                 openai_model: str = "gpt-4o-mini"):
        """
        Initialize RAG chain with model selection.
        
        Args:
            model_name: "Gemini" or "OpenAI"
            gemini_model: Gemini model type
            openai_model: OpenAI model type
        """
        self.model_name = model_name
        self.gemini_model = gemini_model
        self.openai_model = openai_model
        self.pdf_processor = None
    
    def initialize_with_pdf(self, pdf_file, pdf_name: str) -> dict:
        """
        Initialize RAG chain with a PDF file.
        
        Args:
            pdf_file: Streamlit uploaded file
            pdf_name: Name of the PDF
            
        Returns:
            Dictionary with extraction info (pages, chunks, etc.)
        """
        try:
            self.pdf_processor = PDFProcessor()
            
            # Extract text from PDF
            pdf_text, page_count = self.pdf_processor.extract_text_from_pdf(pdf_file)
            
            # Create vector store
            chunk_count = self.pdf_processor.create_vector_store(pdf_text, pdf_name)
            
            return {
                "success": True,
                "pages": page_count,
                "chunks": chunk_count,
                "text_length": len(pdf_text)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_pdf_summary(self, summary_type: str = "comprehensive") -> str:
        """
        Generate summary from PDF using RAG context.
        
        Args:
            summary_type: "comprehensive", "brief", or "key_points"
            
        Returns:
            Generated summary
        """
        if not self.pdf_processor:
            raise Exception("RAG chain not initialized. Upload a PDF first.")
        
        try:
            # Query for context (retrieve relevant sections)
            query = "Provide the main topics, key concepts, and important information from this document."
            context = self.pdf_processor.get_pdf_context(query, k=6)
            
            # Create summary prompt based on type
            if summary_type == "brief":
                prompt = f"""Based on the following document content, write a brief 2-3 paragraph summary covering only the most critical information:

Document Context:
{context}

Provide a concise summary."""
            elif summary_type == "key_points":
                prompt = f"""Based on the following document content, extract and list the 5-7 most important key points:

Document Context:
{context}

List the key points in a clear, numbered format."""
            else:  # comprehensive
                prompt = f"""Based on the following document content, write a comprehensive summary that covers all major topics and key information:

Document Context:
{context}

Provide a detailed summary."""
            
            # Call model
            summary = self._run_model(context, prompt)
            return summary
            
        except Exception as e:
            raise Exception(f"Failed to generate PDF summary: {str(e)}")
    
    def answer_question(self, question: str) -> str:
        """
        Answer a question about the PDF using RAG.
        
        Args:
            question: User's question about the PDF
            
        Returns:
            Answer based on PDF content
        """
        if not self.pdf_processor:
            raise Exception("RAG chain not initialized. Upload a PDF first.")
        
        try:
            # Retrieve relevant context for the question
            context = self.pdf_processor.get_pdf_context(question, k=5)
            
            prompt = f"""Answer the following question based ONLY on the provided document context. 
If the answer is not found in the context, clearly state that the information is not available in the document.

Question: {question}

Document Context:
{context}

Provide a clear and accurate answer."""
            
            answer = self._run_model(context, prompt)
            return answer
            
        except Exception as e:
            raise Exception(f"Failed to answer question: {str(e)}")
    
    def _run_model(self, context: str, prompt: str) -> str:
        """
        Run the selected model with context.
        
        Args:
            context: Retrieved context from PDF
            prompt: User prompt
            
        Returns:
            Model response
        """
        if self.model_name == "Gemini":
            return Model.google_gemini(
                transcript=context,
                prompt=prompt,
                model_type=self.gemini_model,
            )
        else:  # OpenAI
            return Model.openai_gpt(
                transcript=context,
                prompt=prompt,
                model_type=self.openai_model,
            )
