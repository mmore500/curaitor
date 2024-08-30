import os
import shutil
from cropPage import cropAllPdfs
from queryText import query_llm
import streamlit as st
from textMining import process_pdf, process_text_files
from textSegments import process_files

# Streamlit app setup
st.title("curAItor Query Interface")

# File uploader for PDFs
uploaded_files = st.file_uploader(
    "Upload PDF files", type="pdf", accept_multiple_files=True
)

# Define output directories
outputDirectory = "output"
text_output_directory = os.path.join(outputDirectory, "text_files")

# Model selection dropdown
llm_type = st.selectbox("Select the model type:", ("GPT-3.5", "Ollama-Llama3"))

# Path to API key file
key_file_path = "/Users/riteshk/Library/CloudStorage/Box-Box/Research-postdoc/oxRSE-project/API_KEY"

# Handle uploaded files
if uploaded_files:
    uploaded_file_names = [uploaded_file.name for uploaded_file in uploaded_files]
    
    # Create output directories
    os.makedirs(outputDirectory, exist_ok=True)
    os.makedirs(text_output_directory, exist_ok=True)
    
    totalFiles = len(uploaded_files)
    
    # PDF processing button
    if st.button("Process PDFs"):
        # Process and crop PDFs
        for uploaded_file in uploaded_files:
            file_path = os.path.join(outputDirectory, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            process_pdf(file_path, text_output_directory)
        
        cropAllPdfs(uploaded_file_names, outputDirectory, totalFiles)
        
        # Re-process cropped PDFs
        for uploaded_file in uploaded_files:
            file_path = os.path.join(outputDirectory, uploaded_file.name)
            process_pdf(file_path, text_output_directory)
        
        st.success(f"Processed {totalFiles} PDFs successfully.")
        
        # Process text files
        process_text_files(text_output_directory)
        st.write("Text files have been cleaned.")
        
        # Generate embeddings and tokens
        process_files(text_output_directory, outputDirectory, key_file_path, llm_type)
        st.write("Text files processed for embeddings and tokens.")

# Question and prompt inputs
question = st.text_area("Ask a question based on the uploaded PDFs:")
prompt = st.text_area("Enter the prompt for the model:")

# Query submission
if st.button("Ask"):
    if question and prompt:
        st.write("Question:", question)
        st.write("Prompt:", prompt)
        
        # Query LLM and display response
        response = query_llm(question, prompt, key_file_path, llm_type)
        st.write("Response:", response)
    else:
        st.write("Please enter both a question and a prompt.")

# Delete embedding files button
if st.button("Delete embedding files"):
    npy_files_deleted = 0
    embedding_directory = "./"
    for root, dirs, files in os.walk(embedding_directory):
        for file in files:
            if file.endswith(".npy"):
                os.remove(os.path.join(root, file))
                npy_files_deleted += 1
    st.success(f"Deleted {npy_files_deleted} embedding files.")

# Delete output folder button
if st.button("Delete output folder"):
    if os.path.exists(outputDirectory):
        shutil.rmtree(outputDirectory)
        st.success("Output folder deleted successfully.")
    else:
        st.warning("Output folder does not exist.")