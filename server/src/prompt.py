from openai import OpenAI
from typing import Optional
import logging

from models import ProviderSearchParams, UserDemographics
from constants import HCPCS_MAPPINGS, MEDICARE_SPECIALTIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_system_prompt() -> str:
    """Generate the system prompt with current specialty list."""
    specialty_list = "\n    - ".join(sorted(MEDICARE_SPECIALTIES))
    hcpcs_list = "\n    - ".join(
        f"{k} = {v}" for k, v in sorted(HCPCS_MAPPINGS.items())
    )

    return f"""
You are a healthcare search assistant that extracts structured information from natural language queries.

Your task is to return:
- specialty: MUST be chosen EXACTLY from the Medicare specialty list below
- zipcode: If a 5-digit ZIP code is mentioned, extract it. Otherwise leave null.
- city: Proper case (e.g., "Seattle"). Only required if zipcode is not provided.
- state: Two-letter uppercase state abbreviation (e.g., "WA"). Only required if zipcode is not provided.
- hcpcs_prefix: The HCPCS code prefix that best matches the requested procedure (use most specific available)
- confidence: Rate your confidence in the specialty match as "high", "medium", or "low"

LOCATION EXTRACTION PRIORITY:
1. If a ZIP code is mentioned, extract it and leave city/state as null
2. If no ZIP code, extract city and state
3. You MUST provide either a zipcode OR both city and state

STRICT RULES FOR SPECIALTY SELECTION:
1. You MUST pick ONE AND ONLY ONE specialty EXACTLY as it appears in the list below.
2. You MUST NOT invent or shorten specialties.
3. If multiple specialties seem possible, choose the MOST appropriate for the described procedure.
4. Only use Interventional radiology for procedures involving: catheter, embolization, ablation, stent placement, angioplasty, drain placement, or other interventional/therapeutic actions.
5. Distinguish between Diagnostic radiology (imaging/scans) and Interventional radiology (procedures).

MEDICARE SPECIALTY LIST:
    - {specialty_list}

HCPCS PREFIX MAPPINGS (use most specific prefix possible):
    - {hcpcs_list}

If you cannot confidently determine a parameter, make your best educated guess and set confidence to "low".
"""


def parse_provider_query(
    user_input: str,
    client: Optional[OpenAI] = None,
    model: str = "gpt-4o-mini",
    max_retries: int = 2,
) -> ProviderSearchParams:
    """
    Parse natural language input to extract provider search parameters.

    Uses OpenAI's Responses API with Structured Outputs to guarantee schema adherence.

    Args:
        user_input: Natural language query from user
        client: OpenAI client instance (creates new one if None)
        model: OpenAI model to use (gpt-4o-mini recommended)
        max_retries: Number of retry attempts on failure

    Returns:
        ProviderSearchParams: Structured search parameters

    Raises:
        ValueError: If parsing fails after retries
    """
    if client is None:
        client = OpenAI()

    system_prompt = create_system_prompt()

    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Parsing query (attempt {attempt + 1}): {user_input[:100]}...")

            # Using Responses API with structured outputs
            response = client.responses.parse(
                model=model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                text_format=ProviderSearchParams,
            )

            # Check for incomplete response
            if response.status == "incomplete":
                reason = (
                    response.incomplete_details.reason
                    if response.incomplete_details
                    else "unknown"
                )
                logger.warning(f"Incomplete response: {reason}")
                if attempt < max_retries:
                    continue
                raise ValueError(f"Response incomplete: {reason}")

            parsed_data = response.output_parsed

            if parsed_data is None:
                raise ValueError("OpenAI returned empty parsed response")

            # Validate specialty is in approved list
            if parsed_data.specialty not in MEDICARE_SPECIALTIES:
                logger.warning(f"Invalid specialty returned: {parsed_data.specialty}")
                if attempt < max_retries:
                    continue
                raise ValueError(
                    f"Specialty '{parsed_data.specialty}' not in approved list"
                )

            # Validate location parameters
            if not parsed_data.zipcode and not (parsed_data.city and parsed_data.state):
                logger.warning("Neither zipcode nor city/state provided")
                if attempt < max_retries:
                    continue
                raise ValueError("Must provide either zipcode or both city and state")

            location_str = (
                f"zipcode={parsed_data.zipcode}"
                if parsed_data.zipcode
                else f"location={parsed_data.city}, {parsed_data.state}"
            )

            logger.info(
                f"Successfully parsed: specialty={parsed_data.specialty}, "
                f"{location_str}, "
                f"hcpcs={parsed_data.hcpcs_prefix}, confidence={parsed_data.confidence}"
            )

            return parsed_data

        except Exception as e:
            logger.error(f"Parsing attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries:
                raise ValueError(
                    f"Failed to parse query after {max_retries + 1} attempts: {str(e)}"
                )

    raise ValueError("Unexpected error in parse_provider_query")


ALLOWED_SEX = {"male", "female"}
ALLOWED_RACE = {"white", "black", "asian", "hispanic", "native", "other"}


def parse_user_demographics(
    user_input: str,
    client: Optional[OpenAI] = None,
    model: str = "gpt-4o-mini",
    max_retries: int = 2,
) -> UserDemographics:
    """
    Parse natural language input to extract age, sex, and race.

    Uses OpenAI's Responses API with structured output to guarantee schema adherence.

    Args:
        user_input: Natural language query from user
        client: OpenAI client instance (creates new one if None)
        model: OpenAI model to use
        max_retries: Number of retry attempts on failure

    Returns:
        UserDemographics: Structured demographic info

    Raises:
        ValueError: If parsing fails after retries
    """
    if client is None:
        client = OpenAI()

    system_prompt = (
        "You are an assistant that extracts demographic information from user text. "
        "Return ONLY a JSON object with fields 'age', 'sex', and 'race'. "
        "If a field is not mentioned, return null. "
        "Allowed values: sex = male, female; "
        "race = white, black, asian, hispanic, native, other."
    )

    for attempt in range(max_retries + 1):
        try:
            logger.info(
                f"Parsing demographics (attempt {attempt + 1}): {user_input[:100]}..."
            )

            response = client.responses.parse(
                model=model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                text_format=UserDemographics,
            )

            if response.status == "incomplete":
                reason = getattr(response, "incomplete_details", {}).get(
                    "reason", "unknown"
                )
                logger.warning(f"Incomplete response: {reason}")
                if attempt < max_retries:
                    continue
                raise ValueError(f"Response incomplete: {reason}")

            parsed_data = response.output_parsed
            if parsed_data is None:
                raise ValueError("OpenAI returned empty parsed response")

            # Validate sex
            if parsed_data.sex and parsed_data.sex.lower() not in ALLOWED_SEX:
                logger.warning(f"Invalid sex returned: {parsed_data.sex}")
                if attempt < max_retries:
                    continue
                parsed_data.sex = None

            # Validate race
            if parsed_data.race and parsed_data.race.lower() not in ALLOWED_RACE:
                logger.warning(f"Invalid race returned: {parsed_data.race}")
                if attempt < max_retries:
                    continue
                parsed_data.race = None

            logger.info(f"Successfully parsed demographics: {parsed_data}")
            return parsed_data

        except Exception as e:
            logger.error(f"Parsing attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries:
                raise ValueError(
                    f"Failed to parse demographics after {max_retries + 1} attempts: {str(e)}"
                )

    raise ValueError("Unexpected error in parse_user_demographics")
