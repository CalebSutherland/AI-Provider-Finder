from typing import Dict
from queries import search_providers
from prompt import parse_provider_query


def natural_language_search(user_query: str) -> Dict:
    """
    Main function to search for providers using natural language.

    Args:
        user_query: Natural language query from the user

    Returns:
        Dictionary containing parsed parameters and search results
    """
    try:
        # Parse the natural language query
        params = parse_provider_query(user_query)

        # Validate that we have all required parameters
        missing_params = []
        if not params.specialty:
            missing_params.append("specialty")
        if not params.city:
            missing_params.append("city")
        if not params.state:
            missing_params.append("state")
        if not params.hcpcs_prefix:
            missing_params.append("procedure/service type")

        if missing_params:
            return {
                "success": False,
                "error": f"Could not determine: {', '.join(missing_params)}. Please provide more details.",
                "parsed_params": params.model_dump(),
                "results": [],
            }

        results = search_providers(
            specialty=params.specialty,
            city=params.city,
            state=params.state,
            hcpcs_prefix=params.hcpcs_prefix,
        )

        return {
            "success": True,
            "parsed_params": params.model_dump(),
            "results": results,
            "count": len(results),
        }

    except Exception as e:
        return {"success": False, "error": str(e), "parsed_params": {}, "results": []}


queries = [
    "I need a cardiologist who can do an ultrasound near downtown Chicago",
    "Find me a family doctor in Austin, Texas",
    "Looking for an orthopedic surgeon in Miami FL who does knee replacement",
    "I need someone who can do a chest X-ray in Seattle, Washington",
    "Find a cardiologist in Seattle, WA who does echocardiograms",
    "I need an orthopedic surgeon in Portland OR for knee surgery",
    "Looking for dermatologist in Miami FL for skin biopsy",
]

for query in queries:
    result = natural_language_search(query)
    print(f"Query: {query}")
    print(f"Parsed Parameters:")
    for key, value in result["parsed_params"].items():
        print(f"  {key}: {value}")

    if result["success"]:
        print(f"\nFound {result['count']} providers")
        for provider in result["results"][:5]:  # Show first 5
            name = f"{provider['rndrng_prvdr_first_name']} {provider['rndrng_prvdr_last_org_name']}"
            print(f"  - {name} ({provider['rndrng_prvdr_type']})")
    else:
        print(f"\nError: {result['error']}")
    print("\n")
