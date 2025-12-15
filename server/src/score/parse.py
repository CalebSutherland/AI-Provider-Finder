from openai import OpenAI
import logging

from .models import UserDemographics


ALLOWED_SEX = {"male", "female"}
ALLOWED_RACE = {"white", "black", "asian", "hispanic", "native", "other"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_user_demographics(
    user_input: str,
    client: OpenAI | None = None,
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
