# import os
import streamlit as st
from cropPage import cropAllPdfs
from textMining import process_all_pdfs, process_text_files
import textSegments
# import queryText

# Streamlit app
st.title("PDF Query Interface")

# File uploader
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

# Display uploaded files
if uploaded_files:
    st.write("Uploaded PDF files:")
    for uploaded_file in uploaded_files:
        st.write(uploaded_file.name)

    # Directory for the output
    outputDirectory = 'output'
    
    # Total number of files uploaded
    totalFiles = len(uploaded_files)
    
    # Button to process PDFs
    if st.button("Process PDFs"):
        cropAllPdfs(uploaded_files, outputDirectory, totalFiles)
        process_all_pdfs(uploaded_files, outputDirectory)
        # process_text_files(text_files_directory)


# Text input for question
question = st.text_area("Ask a question based on the uploaded PDFs:")

# Text input for prompt
prompt = st.text_area("Enter the prompt for the model:")

# Button to submit the question and prompt
if st.button("Ask"):
    if question and prompt:
        st.write("Question:")
        st.write(question)
        st.write("Prompt:")
        st.write(prompt)
        # Placeholder for the response (this would be replaced with your OpenAI code)
        st.write("Response will be displayed here.")
    else:
        st.write("Please enter both a question and a prompt.")
else:
    st.write("Upload PDF files and enter a question and a prompt to proceed.")
