from dotenv import load_dotenv
import os
import google.generativeai as genai

# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# Load environment variables from the .env file
load_dotenv()

# Get the Hugging Face API key
api_key = os.getenv("GEMINI_API") 
 




class Chatbot:
    def __init__(self):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    
    
    def generate_response(self, context):
        response = self.model.generate_content(context)
        return response.text
