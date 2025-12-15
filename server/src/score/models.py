from pydantic import BaseModel

from ..search.models import ProviderRow


class UserDemographics(BaseModel):
    age: int | None = None
    sex: str | None = None
    race: str | None = None


class ProviderDemographics(ProviderRow):
    """
    Provider demographic data
    """

    bene_feml_cnt: int | None
    bene_male_cnt: int | None

    bene_race_wht_cnt: int | None
    bene_race_black_cnt: int | None
    bene_race_api_cnt: int | None
    bene_race_hspnc_cnt: int | None
    bene_race_nat_ind_cnt: int | None
    bene_race_othr_cnt: int | None


class ScoredProvider(ProviderRow):
    score: float
    rank: int


class RankRequest(BaseModel):
    """
    Client request for provider ranking
    """

    query: str
    provider_ids: list[int]


class RankedProvidersResponse(BaseModel):
    success: bool
    parsed_params: dict
    results: list[ScoredProvider]
    error: str | None = None
