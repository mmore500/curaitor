import os

from cropPage import cropAllPdfs
from queryText import query_llm
import streamlit as st
from textMining import process_pdf, process_text_files
from textSegments import process_files

# Streamlit app
st.title("PDF Query Interface")

# File uploader
uploaded_files = st.file_uploader(
    "Upload PDF files", type="pdf", accept_multiple_files=True
)

# Display uploaded files
if uploaded_files:
    # st.write("Uploaded PDF files:")
    uploaded_file_names = [
        uploaded_file.name for uploaded_file in uploaded_files
    ]
    # for uploaded_file in uploaded_file_names:
    # st.write(uploaded_file)

    # Directory for the output
    outputDirectory = "output"
    text_output_directory = os.path.join(outputDirectory, "text_files")

    # Ensure the output directory exists
    os.makedirs(outputDirectory, exist_ok=True)
    os.makedirs(text_output_directory, exist_ok=True)

    # Total number of files uploaded
    totalFiles = len(uploaded_files)

    # Button to process PDFs
    if st.button("Process PDFs"):
        if not os.path.exists(outputDirectory):
            os.makedirs(outputDirectory)

        for uploaded_file in uploaded_files:
            file_path = os.path.join(outputDirectory, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            process_pdf(file_path, text_output_directory)

        cropAllPdfs(uploaded_file_names, outputDirectory, totalFiles)

        for uploaded_file in uploaded_files:
            file_path = os.path.join(outputDirectory, uploaded_file.name)
            process_pdf(file_path, text_output_directory)

        st.success("PDFs processed successfully.")
        st.write(f"Processed {totalFiles} PDFs.")
        # process_all_pdfs(uploaded_files, outputDirectory)
        # Process text files
        process_text_files(text_output_directory)
        st.write("Text files have been cleaned.")

        # Process cleaned text files to get embeddings and tokens
        key_file_path = (
            ""  # Replace with the actual path to your OpenAI key file
        )
        llm_type = (
            "Ollama"  # Specify the LLM type (e.g., 'GPT', 'HF', 'Ollama')
        )
        process_files(
            text_output_directory, outputDirectory, key_file_path, llm_type
        )
        st.write(
            "Text files have been processed to get embeddings and tokens."
        )

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

        # Query the LLM
        llm_type = (
            "Ollama"  # Specify the LLM type (e.g., 'GPT', 'HF', 'Ollama')
        )
        response = query_llm(question, prompt, llm_type)

        st.write("Response:")
        st.write(response)
    else:
        st.write("Please enter both a question and a prompt.")
else:
    st.write("Upload PDF files and enter a question and a prompt to proceed.")
