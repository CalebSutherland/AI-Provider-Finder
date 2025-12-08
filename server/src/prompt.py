from openai import OpenAI
from typing import Optional
import logging

from models import ProviderSearchParams

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Constants
MEDICARE_SPECIALTIES = {
    "General practice",
    "General surgery",
    "Allergy / immunology",
    "Otolaryngology",
    "Anesthesiology",
    "Cardiology",
    "Dermatology",
    "Family practice",
    "Interventional pain management",
    "Gastroenterology",
    "Internal medicine",
    "Osteopathic manipulative medicine",
    "Neurology",
    "Neurosurgery",
    "Obstetrics / gynecology",
    "Hospice and palliative care",
    "Ophthalmology",
    "Oral surgery (dentists only)",
    "Orthopedic surgery",
    "Cardiac electrophysiology",
    "Pathology",
    "Sports medicine",
    "Plastic and reconstructive surgery",
    "Physical medicine and rehabilitation",
    "Psychiatry",
    "Geriatric psychiatry",
    "Colorectal surgery (formerly proctology)",
    "Pulmonary disease",
    "Diagnostic radiology",
    "Thoracic surgery",
    "Urology",
    "Chiropractic",
    "Nuclear medicine",
    "Pediatric medicine",
    "Geriatric medicine",
    "Nephrology",
    "Hand surgery",
    "Optometry",
    "Infectious disease",
    "Endocrinology",
    "Podiatry",
    "Nurse practitioner",
    "Psychologist (billing independently)",
    "Audiologist (billing independently)",
    "Physical therapist in private practice",
    "Rheumatology",
    "Occupational therapist in private practice",
    "Clinical psychologist",
    "Pain management",
    "Peripheral vascular disease",
    "Vascular surgery",
    "Cardiac surgery",
    "Addiction medicine",
    "Clinical social worker",
    "Critical care (Intensivists)",
    "Hematology",
    "Hematology / oncology",
    "Preventive medicine",
    "Maxillofacial surgery",
    "Neuropsychiatry",
    "Certified clinical nurse specialist",
    "Medical oncology",
    "Surgical oncology",
    "Radiation oncology",
    "Emergency medicine",
    "Interventional radiology",
    "Physician assistant",
    "Gynecological / oncology",
    "Sleep medicine",
    "Interventional cardiology",
    "Dentist",
    "Hospitalist",
    "Advanced heart failure and transplant cardiology",
    "Medical toxicology",
    "Hematopoietic cell transplantation and cellular therapy",
    "Medical genetics and genomics",
    "Undersea and Hyperbaric Medicine",
    "Micrographic Dermatologic Surgery (MDS)",
    "Adult Congenital Heart Disease (ACHD)",
    "Single or multispecialty clinic or group practice (PA Group)",
}

HCPCS_MAPPINGS = {
    "0": "Anesthesia (00100-01999)",
    "1": "Integumentary System (10030-19499)",
    "2": "Musculoskeletal System (20100-29999)",
    "30": "Respiratory - Nose/Sinuses (30000-30999)",
    "31": "Respiratory - Larynx/Trachea (31000-31899)",
    "32": "Respiratory - Lungs/Pleura (32035-32999)",
    "33": "Cardiovascular - Heart/Pericardium (33016-33999)",
    "34": "Cardiovascular - Arteries/Veins (34001-34834)",
    "35": "Cardiovascular - Vascular Repair (35001-35907)",
    "36": "Cardiovascular - Vascular Access (36000-36598)",
    "37": "Cardiovascular - Vascular Other (37140-37799)",
    "38": "Hemic/Lymphatic Systems (38100-38999)",
    "39": "Mediastinum/Diaphragm (39000-39599)",
    "4": "Digestive System (40490-49999)",
    "50": "Urinary - Kidney (50010-50593)",
    "51": "Urinary - Bladder (51020-51999)",
    "52": "Urinary - Urethra (52000-52700)",
    "53": "Urinary - Other (53000-53899)",
    "54": "Male Genital - Penis (54000-54450)",
    "55": "Male Genital - Other (55040-55899)",
    "56": "Female Genital - Vulva/Perineum (56405-56821)",
    "57": "Female Genital - Vagina (57000-57426)",
    "58": "Female Genital - Uterus (58100-58999)",
    "59": "Maternity Care/Delivery (59000-59899)",
    "6": "Endocrine System (60000-60699)",
    "61": "Nervous - Skull/Brain (61000-61888)",
    "62": "Nervous - Spine/Spinal Cord (62263-62368)",
    "63": "Nervous - Extracranial (63001-63746)",
    "64": "Nervous - Peripheral (64400-64999)",
    "65": "Eye - Anterior Segment (65091-66990)",
    "66": "Eye - Posterior Segment (67005-67299)",
    "67": "Eye - Ocular Adnexa (67311-67999)",
    "68": "Eye - Other (68020-68899)",
    "69": "Auditory System (69000-69979)",
    "7": "Diagnostic Radiology/Imaging (70010-76499)",
    "76": "Diagnostic Ultrasound (76506-76999)",
    "78": "Nuclear Medicine - Diagnostic (78012-78999)",
    "79": "Nuclear Medicine - Therapeutic (79005-79999)",
    "8": "Pathology/Laboratory (80047-89398)",
    "82": "Chemistry Procedures (82009-82271)",
    "83": "Chemistry - Hormones/Drugs (83001-83992)",
    "84": "Chemistry - Other (84022-84999)",
    "85": "Hematology/Coagulation (85002-85999)",
    "86": "Immunology (86000-86849)",
    "87": "Microbiology (87003-87999)",
    "9": "Medicine/E&M (90281-99607, 98000-99499)",
    "93": "Cardiovascular Procedures (92920-93799)",
    "94": "Pulmonary Procedures (94002-94799)",
    "97": "Physical Medicine/Rehab (97010-97799)",
}


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
- city: Proper case (e.g., "Seattle")
- state: Two-letter uppercase state abbreviation (e.g., "WA")
- hcpcs_prefix: The HCPCS code prefix that best matches the requested procedure (use most specific available)
- confidence: Rate your confidence in the specialty match as "high", "medium", or "low"

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

            logger.info(
                f"Successfully parsed: specialty={parsed_data.specialty}, "
                f"location={parsed_data.city}, {parsed_data.state}, "
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
