import os
from config.config import RAG_CONFIG 
os.environ['HF_ENDPOINT'] = RAG_CONFIG["HF_MIRROR"]

from langchain_huggingface import HuggingFaceEmbeddings




MODEL_NAME = RAG_CONFIG["MODEL_NAME"]
DEVICE = RAG_CONFIG["DEVICE"]
NORMALIZE_EMBEDDINGS = RAG_CONFIG["NORMALIZE_EMBEDDINGS"]
CACHE_FOLDER = RAG_CONFIG["CACHE_FOLDER"]

def get_bge_embeddings():
   
    model_kwargs = {
        "device": DEVICE
    }

    encode_kwargs = {
        "normalize_embeddings": NORMALIZE_EMBEDDINGS
    }

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        cache_folder=CACHE_FOLDER
    )

    return embeddings
