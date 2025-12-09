from typing import Union
from fastapi import FastAPI

from models import SearchRequest
from service import natural_language_search

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/api/search_providers")
def handle_search(req: SearchRequest):
    res = natural_language_search(req.query)
    return res