from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path
import time
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import laion_clap
from typing import List
from transformers import RobertaModel

model: laion_clap.CLAP_Module | None = None

# Loads the model when the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # anything before yield is loaded on startup
    model = laion_clap.CLAP_Module(enable_fusion=False, amodel="HTSAT-base")
    # Make sure you've downloaded this checkpoint from here and store it in the /clap-data directory in this project
    # https://huggingface.co/lukewys/laion_clap/resolve/main/music_speech_audioset_epoch_15_esc_89.98.pt?download=true 
    model.load_ckpt("/clap-data/music_speech_audioset_epoch_15_esc_89.98.pt")  
    yield
    # Anything after yield is run on teardown

app = FastAPI(lifespan=lifespan)

class TextEmbeddingModel(BaseModel):
    queries: List[str]

# API expects a body of
# {
#    queries: ["query 1", "query 2"]
# }
@app.post("/text-embedding")
def post_text_embedding(body: TextEmbeddingModel): 

    embeddings = []

    if model is not None:
        embeddings = model.get_text_embedding(body.queries)
        embeddings = embeddings.tolist()

    return {"embedding": embeddings}
