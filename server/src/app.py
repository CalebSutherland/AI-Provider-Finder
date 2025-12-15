from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .search.queries import fetch_providers
from .search.service import parse_search
from .search.models import (
    ParseRequest,
    ProviderSearchParams,
    SearchResult,
)
from .error import QueryParseError, LLMServiceError


load_dotenv()
app = FastAPI()

origins = [os.getenv("CLIENT_URL", "http://localhost:5173")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/providers/search/parse", response_model=ProviderSearchParams)
def parse_user_search(req: ParseRequest):
    try:
        return parse_search(req.query)

    except QueryParseError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except LLMServiceError as e:
        raise HTTPException(status_code=502, detail=f"Parsing service failed: {e}")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal service error")


@app.post("/api/providers/search/query", response_model=SearchResult)
def handle_search(
    req: ProviderSearchParams,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=10, le=100),
):
    if not req.zipcode and not req.state:
        raise HTTPException(status_code=400, detail="zipcode or state is required")

    return fetch_providers(
        specialty=req.specialty,
        hcpcs_prefix=req.hcpcs_prefix,
        city=req.city,
        state=req.state,
        zipcode=req.zipcode,
        page=page,
        page_size=page_size,
    )


# @app.post("/api/rank_providers")
# def handle_rank(req: RankRequest) -> RankedProvidersResponse:
#     res = rank_providers_nl(req.query, req.provider_ids)
#     return res
