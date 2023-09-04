#!/usr/bin/env python3
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import chromadb
import os
import argparse
import time

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

prompt_template = """
You are a helpdesk employee on a hospital. Your job is to help answer questions from a potential patients.
Your answer should be concice and polite.

Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer:
"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

from constants import CHROMA_SETTINGS

def privateGPT(query):
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    chroma_client = chromadb.PersistentClient(
        settings=CHROMA_SETTINGS, 
        path=persist_directory
    )
    db = Chroma(
        persist_directory=persist_directory, 
        embedding_function=embeddings, 
        client_settings=CHROMA_SETTINGS, 
        client=chroma_client
    )
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})

    llm = GPT4All(
        model=model_path, 
        max_tokens=model_n_ctx, 
        backend='gptj', 
        n_batch=model_n_batch, 
        verbose=False
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever, 
        return_source_documents= False,
        chain_type_kwargs={"prompt": PROMPT}
    )
   
    if query.strip() != "":
        start = time.time()
        res = qa(query)
        answer = res['result']
        end = time.time()

        return answer
    else:
        return "No query" 