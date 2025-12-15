from ..error import QueryParseError
from .parse import parse_provider_search
from .constants import MEDICARE_SPECIALTIES


def parse_search(query: str):
    params = parse_provider_search(query)

    if params.specialty not in MEDICARE_SPECIALTIES:
        raise QueryParseError(f"Provider specialty not recognized")

    if not params.zipcode and not params.state:
        raise QueryParseError("Must provide zipcode or state")

    return params
