from inference.chat import Chatbot 
from database.database import VectorDatabase



class InferencePipeline: 
    """
    Inference Pipeline for the DOC-QA

    """
    def __init__(self): 
        self.chat_model = Chatbot()
        self.vector_db = VectorDatabase() 

    def store_pdf_db(self, pdf_path): 
        """
        Stores the content of the pdf to the vector database 
        """ 
        self.vector_db.add_pdfs(pdf_path)
    
    def retrive_subsequent_chunk(self, query, top_k): 
        """
        Retrives the top k chunks for the given query from the vector database 
        """
        retrieved_docs = self.vector_db.query(query_texts=[query], n_results=top_k)
        # Flatten the nested list of documents
        retrieved_docs = [doc for sublist in retrieved_docs['documents'] for doc in sublist] 
        return retrieved_docs
        

    def result(self, query): 
        retrieved_docs = self.retrive_subsequent_chunk(query,5) # Defaulting to the top 5 chunks
        # Combine the query text with the retrieved context
        combined_input = f"{query}\n\nContext:\n" + "\n".join(retrieved_docs)
        # Generate response using Gemini API
        response = self.chat_model.generate_response(combined_input)
        return response

def main() : 
    pdf_path = ["/home/pa1/Documents/cv_qa/data/raw/1901841_RESUME.pdf"]
    question = "What is the candidate's educational background?"
    pipe = InferencePipeline()
    pipe.store_pdf_db(pdf_path)
    final_result = pipe.result(question)
    print(final_result)

if __name__ == "__main__": 
    main() 
