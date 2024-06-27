"""
File name: textSegments.py
Author: Stephanie Khuu
Date created: 2024-04-16
Date last modified: 2024-05-24
Python Version: 3.11.4

Description:
This script processes existing cleaned text files and gets the number of tokens, as well as creates embeddings.
Embeddings, text and page information are then saved to .npy files.
"""

from datetime import datetime
import os

from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings, LlamaCppEmbeddings
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOllama

# import PyPDF2
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import numpy as np
from openai import OpenAI
import pandas as pd
import tiktoken
from tqdm import tqdm
import transformers
from transformers import (
    AutoModel,
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
)

tqdm.pandas()

# llama3_local = '/eagle/fallwkshp23/riteshk/Meta-Llama-3-8B-Instruct'
llama3_local = ""


def process_files(txt_directory, output_text_directory, key_file_path, llm):
    # Ensure the output directory for the text and embeddings exists
    if not os.path.exists(output_text_directory):
        os.makedirs(output_text_directory)

    client = None  # Initialize client to None
    # if llm == "GPT*":
    if llm.startswith("GPT"):
        # Configure OpenAI API client
        client = OpenAI(api_key=read_key(key_file_path))

    all_data = []  # Store data for all files
    file_list = [f for f in os.listdir(txt_directory) if f.endswith(".txt")]
    for filename in tqdm(file_list, desc="Processing files"):
        file_path = os.path.join(txt_directory, filename)
        data = get_txt_tokens(file_path)
        all_data.extend(data)

    # Convert collected data into a DataFrame
    df = pd.DataFrame(all_data)
    print("Adding embeddings...")
    # if client is not None:  # Check if client is not None before using it
    df_with_embeddings = add_embedding(df, client, llm)
    print("Saving data...")
    current_datetime = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    embeddings_file_name = current_datetime + "embeddings.npy"
    save_embeddings_to_npy(df_with_embeddings, embeddings_file_name)
    # Save processed DataFrame to CSV

    # else:  # Check if client is not None before using it
    #     df_with_embeddings = add_embedding(df, client, llm)
    #     print("Saving data...")
    #     current_datetime = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    #     embeddings_file_name = current_datetime + "embeddings.npy"
    #     save_embeddings_to_npy(df_with_embeddings, embeddings_file_name)
    #     # Save processed DataFrame to CSV


def get_txt_tokens(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as txt_content:
        text = txt_content.read()
        words = text.split()
        text_join = " ".join(words)
        text_len = len(text_join)
        num_text_parts = 15
        div_len = max(1, text_len // num_text_parts)  # Avoid division by zero
        text_parts = [
            text_join[i * div_len : (i + 1) * div_len]
            for i in range(num_text_parts)
        ]
        for i, text_part in enumerate(text_parts):
            data.append(
                {
                    "file name": os.path.basename(file_path),
                    "page number": 1,
                    "page section": i + 1,
                    "content": text_part,
                    "tokens": count_tokens(text_part),
                }
            )
    return data


def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    return num_tokens


# Retrieve OpenAI Key
def read_key(key_file_path):
    with open(key_file_path, "r") as file:
        key = file.read()
    return key


def add_embedding(df, client, llm):
    if "embedding" in df.columns:
        print("The dataframe already has embeddings. Please double check.")
        return df

    # if llm == "GPT*":
    elif llm.startswith("GPT"):
        # Define a function to get embeddings
        def get_embedding_openai(text):
            try:
                response = client.embeddings.create(
                    input=text, model="text-embedding-3-large"
                )
                return response.data[0].embedding
            except Exception as e:
                print("Failed to retrieve embedding:", e)
                return None

        # Apply the function to the 'content' column
        df["embedding"] = df["content"].progress_apply(get_embedding_openai)
        # return df

    # elif llm == "HF*":
    elif llm.startswith("HF"):
        """Adds an 'embedding' column to a dataframe using Llama2/3"""
        full_model = AutoModel.from_pretrained(llama3_local)
        tokenizer = AutoTokenizer.from_pretrained(llama3_local)

        # if 'embedding' in df.columns:
        #     print('The dataframe already has embeddings. Please double check.')
        #     return df

        embed_msgs = []
        for _, row in df.iterrows():
            context = row["content"]
            seq_id = tokenizer(context, return_tensors="pt")["input_ids"]
            embedding = (
                full_model(seq_id)["last_hidden_state"]
                .mean(axis=[0, 1])
                .detach()
                .numpy()
            )
            # inputs = tokenizer(context, return_tensors="pt")
            # outputs = model(**inputs)
            # context_emb = outputs.last_hidden_state[:, -1, :].detach().numpy()
            # embed_msgs.append(context_emb)
            embed_msgs.append(embedding)

        df = df.copy()
        df.loc[:, "embedding"] = embed_msgs
        # return df

    # elif llm == "Ollama*":
    elif llm.startswith("Ollama"):
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        embed_msgs = []
        for _, row in df.iterrows():
            context = row["content"]
            embedding = embeddings.embed_documents([context])
            embed_msgs.append(embedding)
            # embeddings.embed_documents(["Hello, how are you?", "I am fine, thank you."])
        df = df.copy()
        df.loc[:, "embedding"] = embed_msgs

    return df


def save_embeddings_to_npy(df, filename):
    # Extract embeddings into a numpy array and save to a binary file
    if "embedding" in df.columns:
        embeddings = np.vstack(
            df["embedding"].apply(lambda x: np.zeros(1024) if x is None else x)
        )
        np.save(filename, embeddings)
        # embeddings = np.vstack(df['embedding'].values)  # Stack embeddings which are in list format
    # np.save(filename, embeddings)
    if "content" in df.columns:
        content_data = np.vstack(df["content"].values)
        # Save the "content" data to `texts.npy`
        current_datetime = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        texts_file_name = current_datetime + "texts.npy"
        pages_file_name = current_datetime + "pages.npy"
        np.save(texts_file_name, content_data)

    # Save other data into separate .npy files if needed
    if {
        "file name",
        "page number",
        "page section",
        "content",
        "tokens",
    }.issubset(df.columns):
        pages_data = df[
            ["file name", "page number", "page section", "content", "tokens"]
        ].to_numpy()
        np.save(pages_file_name, pages_data)
    else:
        print("incorrect column names")

    print("Data saved successfully.")


# # List of PDF file names
# # txt_directory = 'articles/review/output/textOutput'
# txt_directory = 'articles/output/textOutput'
# output_text_directory = 'text_output'
# # Configure OpenAI API key
# key_file_path = 'api_key'
# process_files(txt_directory, output_text_directory, key_file_path)
