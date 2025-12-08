from pydantic import BaseModel, Field
from typing import Optional


class ProviderSearchParams(BaseModel):
    """Structured output for provider search parameters"""

    specialty: str = Field(..., description="Medicare specialty exactly as listed")
    city: str = Field(..., description="City name in proper case")
    state: str = Field(..., pattern="^[A-Z]{2}$", description="Two-letter state code")
    hcpcs_prefix: str = Field(..., description="HCPCS code prefix")
    confidence: Optional[str] = Field(
        None, description="Confidence level: high, medium, low"
    )
