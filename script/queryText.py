import csv
import glob
import os

from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import numpy as np
from openai import OpenAI
from transformers import AutoModel, AutoTokenizer, pipeline

# llama3_local = '/eagle/fallwkshp23/riteshk/Meta-Llama-3-8B-Instruct'
llama3_local = ""

# llm = ''

# Path to your YAML file
root_dir = os.path.dirname(os.path.dirname(__file__))
prompt_path = f"{root_dir}/prompts.yml"


def cosine_similarity(v1, v2):
    """Calculate cosine similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)


def find_most_relevant_text(embeddings, query_embedding):
    """Find the text with the highest cosine similarity to the query."""
    similarities = [
        cosine_similarity(query_embedding, emb) for emb in embeddings
    ]
    return np.argmax(similarities)


# Assuming 'texts' and 'embeddings' are loaded from files or a database
def load_texts_and_embeddings(text_filename, embedding_filename):
    texts = np.load(
        text_filename, allow_pickle=True
    )  # Load texts if saved as a NumPy array
    embeddings = np.load(embedding_filename)  # Load embeddings
    return texts, embeddings


def read_key(key_file_path):
    with open(key_file_path, "r") as file:
        key = file.read()
    return key


# Configure OpenAI API key
# if llm.startswith("GPT"):
# key_file_path = "api_key"
# key = read_key(key_file_path)
# client = OpenAI(api_key=key)


# Assume you have a function to generate or fetch your query embedding
def get_query_embedding(query_text, llm):
    if llm.startswith("GPT"):
        key_file_path = "api_key"
        key = read_key(key_file_path)
        client = OpenAI(api_key=key)

        # This should call an embedding API or use a locally hosted model
        response = client.embeddings.create(
            input=query_text, model="text-embedding-3-large"
        )
        return response.data[0].embedding

    elif llm.startswith("HF"):
        full_model = AutoModel.from_pretrained(llama3_local)
        tokenizer = AutoTokenizer.from_pretrained(llama3_local)
        response = tokenizer(query_text, return_tensors="pt")["input_ids"]
        return (
            full_model(response)["last_hidden_state"]
            .mean(axis=[0, 1])
            .detach()
            .numpy()
        )

    elif llm.startswith("Ollama"):
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        embed = embeddings.embed_documents([query_text])
        return embed


# # Example query text: Define the query text about cellular involvement in muscle repair and regeneration
# query_text = (
#     "Describe the involvement and interactions of any cell types such as satellite cells, fibroblasts, "
#     "macrophages, neutrophils, or cytokines such as TNF-a, IL-6 etc, or growth factors TGF-B, IGF-1 etc, in the process of muscle repair and regeneration."
#     "Also describe any interactions between cells or of cell secretions on other cell types, or of growth factors and cytokines on tissues"
# )

# # Create a detailed prompt for GPT-4 using the relevant text, specifying a tabular response format
# prompt = (
#     "Using the context provided below, elaborate on the roles played by different cell types as if you were creating rules for an agent-based model "
#     "and factors in muscle repair and regeneration. Structure your response in a table with three columns: "
#     "1) Embedding numbers, 2) Source text name, and 3) Detailed roles and interactions of cell types like "
#     "satellite cells, fibroblasts, macrophages, neutrophils, cytokines, and growth factors. Provide multiple entries "
#     "for each cell type or cytokine or growth factor mentioned, focusing on their specific effects during the cell cycle phases and their interactions during the process of muscle repair.\n\n"
#     f"Context: {relevant_text}"
# )


def query_llm(query_text, prompt, llm):
    # Load data
    text = glob.glob("*texts.npy")[0]
    embed = glob.glob("*embeddings.npy")[0]
    texts, embeddings = load_texts_and_embeddings(text, embed)

    # Get the embedding for the query to identify relevant texts
    query_embedding = get_query_embedding(query_text, llm)

    # Determine the index of the most relevant text from the embeddings
    most_relevant_index = find_most_relevant_text(embeddings, query_embedding)
    relevant_text = texts[most_relevant_index][0]

    prompt_ = prompt + f"Context: {relevant_text}"

    if llm.startswith("GPT"):
        key_file_path = "api_key"
        key = read_key(key_file_path)
        client = OpenAI(api_key=key)

        # Generate a response from GPT-4 based on the formulated prompt
        response = client.chat.completions.create(
            model="gpt-4", messages=[{"role": "system", "content": prompt_}]
        )
        response_text = response.choices[0].message.content

    elif llm.startswith("HF"):
        chatbot = pipeline("text-generation", model=llama3_local)
        response = chatbot(
            prompt_, max_length=4000, do_sample=True, temperature=0.1
        )
        response_text = response[0]["generated_text"]

    elif llm.startswith("Ollama"):
        chatbot = ChatOllama(model="llama3", temperature=0)
        chat_prompt = ChatPromptTemplate.from_template(prompt_)
        chain = chat_prompt | chatbot | StrOutputParser()
        full_output = chain.invoke({"Context": {relevant_text}})
        response_text = full_output

    # Debug: Print the raw response text
    print("Response Text:", response_text)

    # Extract only the table part
    table_start = full_output.find("| ")
    table_end = full_output.rfind("|") + 1
    table_text = full_output[table_start:table_end]

    # Convert the table text to a list of dictionaries
    data = []
    if table_text:
        table_lines = table_text.strip().split("\n")
        if len(table_lines) > 1:  # Ensure there are header and data lines
            headers = table_lines[0].split("|")[
                1:-1
            ]  # Extract headers, ignoring first and last empty strings
            headers = [header.strip() for header in headers]  # Clean headers
            for row in table_lines[2:]:  # Skip the header and divider lines
                columns = row.split("|")[
                    1:-1
                ]  # Split by '|' and remove the first and last empty strings
                columns = [
                    column.strip() for column in columns
                ]  # Clean column values
                row_data = dict(
                    zip(headers, columns)
                )  # Create a dictionary for the row
                data.append(row_data)
        else:
            print("Table extraction failed: Not enough lines in table text.")
    else:
        print("Table extraction failed: No table found in response text.")

    # Write the data to a CSV file if data is not empty
    if data:
        csv_file_path = "output_table.csv"
        with open(csv_file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {csv_file_path}")
    else:
        print("No data to save to CSV.")

    return response_text
