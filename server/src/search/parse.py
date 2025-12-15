from openai import OpenAI
import logging

from .models import ProviderSearchParams
from ..error import LLMServiceError
from .constants import HCPCS_MAPPINGS, MEDICARE_SPECIALTIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_system_prompt() -> str:
    """Generate the system prompt with current specialty list."""
    specialty_list = "\n    - ".join(MEDICARE_SPECIALTIES)
    hcpcs_list = "\n    - ".join(f"{k} = {v}" for k, v in HCPCS_MAPPINGS.items())

    return f"""
You are a healthcare search assistant that extracts structured information from natural language queries.

Your task is to return:
- specialty: MUST be chosen EXACTLY from the Medicare specialty list below
- zipcode: If a 5-digit ZIP code is mentioned, extract it. Otherwise leave null.
- city: Proper case (e.g., "Seattle"). Optional, leave null if not mentioned.
- state: Two-letter uppercase state abbreviation (e.g., "WA"). Only required if zipcode is not provided.
- hcpcs_prefix: The HCPCS code prefix that best matches the requested procedure (use most specific available)
- confidence: Rate your confidence in the specialty match as "high", "medium", or "low"

Your task is to return:
- specialty: Choose exactly from the Medicare specialty list below.  If you cannot determine it, return null.
- zipcode: If a 5-digit ZIP code is mentioned, extract it. Otherwise return null.
- city: Proper case (e.g., "Seattle"). If not mentioned, return null.
- state: Two-letter uppercase state abbreviation (e.g., "WA"). If not mentioned, return null.
- hcpcs_prefix: The HCPCS code prefix that best matches the requested procedure (use most specific available). Return null if no procedure is detected.
- confidence: Rate your confidence in the specialty match as "high", "medium", or "low". If specialty is null, set confidence to "low".

BEFORE PROCESSING THE QUERY:
If the user input is extremely short (fewer than 2 words) OR does not contain any meaningful medical, specialty, or location information, 
THEN:
- specialty: null
- zipcode: null
- city: null
- state: null
- hcpcs_prefix: null
- confidence: "low"

Do NOT attempt to infer or guess any specialty or procedure from such inputs.

STRICT RULES FOR SPECIALTY SELECTION:
1. You MUST pick ONE AND ONLY ONE specialty EXACTLY as it appears in the list below.
2. You MUST NOT invent or shorten specialties.
3. If the query is vague but clearly a general medical request (e.g., "I need a doctor" or "I need a check-up"), default specialty to "Family Practice."
4. If multiple specialties seem possible, choose the MOST appropriate for the described procedure
5. Only use Interventional radiology for procedures involving: catheter, embolization, ablation, stent placement, angioplasty, drain placement, or other interventional/therapeutic actions.
6. Distinguish between Diagnostic radiology (imaging/scans) and Interventional radiology (procedures).


HCPCS PREFIX RULES:
- Return the HCPCS prefix KEY (e.g., "7", "30", "93"), NOT the description.
- Only return a value from the HCPCS mapping list. Return null if no procedure-related terms are detected.
- If unsure about the exact prefix, return the BEST GUESS and set confidence to "low".

MEDICARE SPECIALTY LIST:
    - {specialty_list}

HCPCS PREFIX MAPPINGS (use most specific prefix possible):
    - {hcpcs_list}

If you cannot confidently determine a parameter, make your best educated guess and set confidence to "low".
"""


def parse_provider_search(
    user_input: str,
    client: OpenAI | None = None,
    model: str = "gpt-4o-mini",
) -> ProviderSearchParams:
    """
    Parse natural language input to extract provider search parameters.

    Uses OpenAI's Responses API with Structured Outputs to guarantee schema adherence.

    Args:
        user_input: Natural language query from user
        client: OpenAI client instance (creates new one if None)
        model: OpenAI model to use (gpt-4o-mini recommended)

    Returns:
        ProviderSearchParams: Structured search parameters

    Raises:
        ValueError: If parsing fails after retries
    """
    if client is None:
        client = OpenAI()

    system_prompt = create_system_prompt()

    logger.info(f"Parsing query: {user_input[:100]}...")

    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        text_format=ProviderSearchParams,
    )

    if response.status == "incomplete":
        reason = (
            response.incomplete_details.reason
            if response.incomplete_details
            else "unknown"
        )
        logger.warning(f"Incomplete response: {reason}")
        raise LLMServiceError(f"Response incomplete: {reason}")

    parsed_data = response.output_parsed
    if parsed_data is None:
        raise LLMServiceError("Model returned empty structured output")

    if parsed_data.specialty not in MEDICARE_SPECIALTIES:
        logger.warning(f"Invalid specialty returned: {parsed_data.specialty}")

    if not parsed_data.zipcode and not parsed_data.state:
        logger.warning("Neither zipcode or state provided")

    if parsed_data.zipcode:
        location_str = f"zipcode={parsed_data.zipcode}"
    elif parsed_data.city and parsed_data.state:
        location_str = f"location={parsed_data.city}, {parsed_data.state}"
    else:
        location_str = f"location={parsed_data.state}"

    logger.info(
        f"Successfully parsed: specialty={parsed_data.specialty}, "
        f"{location_str}, "
        f"hcpcs={parsed_data.hcpcs_prefix}, confidence={parsed_data.confidence}"
    )

    return parsed_data
