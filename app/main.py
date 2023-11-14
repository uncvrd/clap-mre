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

# model: laion_clap.CLAP_Module | None = None

ml_models = {}

# Loads the model when the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):

    # took ml_models concept from https://fastapi.tiangolo.com/advanced/events/#lifespan
    # anything before yield is loaded on startup
    ml_models["clap"] = laion_clap.CLAP_Module(enable_fusion=False, amodel="HTSAT-base")
    # Make sure you've downloaded this checkpoint from here and store it in the /clap-data directory in this project
    # https://huggingface.co/lukewys/laion_clap/resolve/main/music_speech_audioset_epoch_15_esc_89.98.pt?download=true 
    ml_models["clap"].load_ckpt("/clap-data/music_speech_audioset_epoch_15_esc_89.98.pt")
    yield
    # Anything after yield is run on teardown
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

class TextEmbeddingModel(BaseModel):
    queries: List[str]

# API expects a body of
# {
#    queries: ["query 1", "query 2"]
# }
@app.post("/text-embedding")
def post_text_embedding(body: TextEmbeddingModel): 

    embeddings = ml_models["clap"].get_text_embedding(body.queries).tolist()

    return {"embedding": embeddings}
