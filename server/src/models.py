from pydantic import BaseModel, Field
from typing import Optional


class ProviderSearchParams(BaseModel):
    """Structured output for provider search parameters"""

    specialty: str = Field(..., description="Medicare specialty exactly as listed")
    zipcode: Optional[str] = Field(
        None, pattern="^[0-9]{5}$", description="5-digit ZIP code if provided"
    )
    city: Optional[str] = Field(None, description="City name in proper case")
    state: Optional[str] = Field(None, pattern="^[A-Z]{2}$", description="Two-letter state code")
    hcpcs_prefix: str = Field(..., description="HCPCS code prefix")
    confidence: Optional[str] = Field(
        None, description="Confidence level: high, medium, low"
    )

class SearchRequest(BaseModel):
    query: str
    