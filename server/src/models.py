from pydantic import BaseModel, Field


class ProviderSearchParams(BaseModel):
    """
    Structured output for provider search parameters
    """

    specialty: str = Field(..., description="Medicare specialty exactly as listed")
    zipcode: str | None = Field(
        None, pattern="^[0-9]{5}$", description="5-digit ZIP code if provided"
    )
    city: str | None = Field(None, description="City name in proper case")
    state: str | None = Field(
        None, pattern="^[A-Z]{2}$", description="Two-letter state code"
    )
    hcpcs_prefix: str = Field(..., description="HCPCS code prefix")
    confidence: str | None = Field(
        None, description="Confidence level: high, medium, low"
    )


class UserDemographics(BaseModel):
    age: int | None = None
    sex: str | None = None
    race: str | None = None


class Provider(BaseModel):
    """
    Provider data retrieved from the database
    """

    id: int
    last_name: str
    first_name: str | None
    credentials: str | None
    street_1: str
    street_2: str | None
    city: str
    state: str
    zipcode: str
    specialty: str
    accepts_medicare: str
    total_benes: int
    avg_age: float


class ProviderDemographics(Provider):
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


class ScoredProvider(Provider):
    score: float
    rank: int = 0


class SearchRequest(BaseModel):
    """
    Client request for provider search
    """

    query: str


class RankRequest(BaseModel):
    """
    Client request for provider ranking
    """

    query: str
    provider_ids: list[int]


class NLSResponse(BaseModel):
    success: bool
    parsed_params: dict
    results: list[Provider]
    hcpcs_desc: str | None = None
    count: int | None = None
    error: str | None = None


class RankedProvidersResponse(BaseModel):
    success: bool
    parsed_params: dict
    results: list[ScoredProvider]
    error: str | None = None
