from typing import TypedDict
from pydantic import BaseModel, Field, model_validator

from .constants import HCPCS_MAPPINGS


class ProviderRow(TypedDict):
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


class SearchResult(TypedDict):
    """
    Database result from provider search
    """

    result: list[ProviderRow]
    count: int


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
    hcpcs_prefix: str | None = Field(
        None,
        pattern="^[1-9]{1,2}$",
        description="HCPCS code prefix: 1 or 2 digits, each 1-9, or None",
    )
    hcpcs_description: str | None = Field(
        None,
        description="HCPCS prefix description",
    )
    confidence: str | None = Field(
        None, description="Confidence level: high, medium, low"
    )

    @model_validator(mode="after")
    def set_hcpcs_description(self):
        if self.hcpcs_prefix is None:
            self.hcpcs_description = None
        else:
            self.hcpcs_description = HCPCS_MAPPINGS.get(self.hcpcs_prefix)
        return self


class ParseRequest(BaseModel):
    """
    Client request for parsing input
    """

    query: str
