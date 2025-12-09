from typing import List, Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import Provider, SearchRequest
from service import natural_language_search

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/search_providers")
def handle_search(req: SearchRequest):
    res = natural_language_search(req.query)
    return res