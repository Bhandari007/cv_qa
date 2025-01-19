import streamlit as st
import requests

# Set up the API base URL
API_BASE_URL = "http://localhost:8000"  # Adjust this if your FastAPI app is hosted elsewhere

def main():
    st.title("DOC-QA Inference Pipeline")

    st.header("Upload PDF")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        st.success("PDF uploaded successfully!")
        if st.button("Store PDF in Database"):
            response = requests.post(f"{API_BASE_URL}/store-pdf/", files={"file": pdf_file})
            if response.status_code == 200:
                st.success("PDF stored in database successfully!")
            else:
                st.error("Failed to store PDF in database.")
    
    st.header("Query Database")
    query = st.text_input("Enter your query")

    if query and st.button("Get Answer"):
        response = requests.post(f"{API_BASE_URL}/query/", data={"query": query})
        if response.status_code == 200:
            answer = response.json().get("response", "No response received.")
            st.success(f"Answer: {answer}")
        else:
            st.error("Failed to get an answer from the database.")

if __name__ == "__main__":
    main()