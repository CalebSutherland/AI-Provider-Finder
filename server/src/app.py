from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import NLSResponse, RankRequest, RankedProvidersResponse, SearchRequest
from .service import natural_language_search, rank_providers_nl

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
def handle_search(req: SearchRequest) -> NLSResponse:
    res = natural_language_search(req.query)
    return res


@app.post("/api/rank_providers")
def handle_rank(req: RankRequest) -> RankedProvidersResponse:
    res = rank_providers_nl(req.query, req.provider_ids)
    return res
