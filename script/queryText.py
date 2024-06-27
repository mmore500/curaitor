import numpy as np
from openai import OpenAI
from script.readPrompts import read_prompts, choose_prompt
import os

# Path to your YAML file
root_dir = os.path.dirname(os.path.dirname(__file__))
prompt_path = f'{root_dir}/prompts.yml'

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

# Load data
text = glob.glob("*texts.npy")[0]
embed = glob.glob("*embeddings.npy")[0]
texts, embeddings = load_texts_and_embeddings(
    text, embed
)

# Assume you have a function to generate or fetch your query embedding

def get_query_embedding(query_text):
    # This should call an embedding API or use a locally hosted model
    response = client.embeddings.create(
        input=query_text, model="text-embedding-3-large"
    )
    return response.data[0].embedding


# Define the query text about cellular involvement in muscle repair and regeneration
query_text = (
    "Describe the involvement and interactions of any cell types such as satellite cells, fibroblasts, "
    "macrophages, neutrophils, or cytokines such as TNF-a, IL-6 etc, or growth factors TGF-B, IGF-1 etc, in the process of muscle repair and regeneration."
    "Also describe any interactions between cells or of cell secretions on other cell types, or of growth factors and cytokines on tissues"
)

# Get the embedding for the query to identify relevant texts
query_embedding = get_query_embedding(query_text)

# Determine the index of the most relevant text from the embeddings
most_relevant_index = find_most_relevant_text(embeddings, query_embedding)
relevant_text = texts[most_relevant_index]

# Create a detailed prompt for GPT-4 using the relevant text, specifying a tabular response format

# prompt = (
#     "Using the context provided below, elaborate on the roles played by different cell types as if you were creating rules for an agent-based model "
#     "and factors in muscle repair and regeneration. Structure your response in a table with three columns: "
#     "1) Embedding numbers, 2) Source text name, and 3) Detailed roles and interactions of cell types like "
#     "satellite cells, fibroblasts, macrophages, neutrophils, cytokines, and growth factors. Provide multiple entries "
#     "for each cell type or cytokine or growth factor mentioned, focusing on their specific effects during the cell cycle phases and their interactions during the process of muscle repair.\n\n"
#     f"Context: {relevant_text}"
# )



prompt = choose_prompt(prompts=read_prompts(prompt_path))

# Generate a response from GPT-4 based on the formulated prompt
response = client.chat.completions.create(
    model="gpt-4", messages=[{"role": "system", "content": prompt}]
)


print("GPT-4 Response:", response.choices[0].message.content)

