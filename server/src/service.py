from .models import (
    NLSResponse,
    ProviderDemographics,
    RankedProvidersResponse,
    UserDemographics,
    ScoredProvider,
)
from .queries import get_provider_demographics, search_providers
from .prompt import parse_provider_query, parse_user_demographics
from .constants import HCPCS_MAPPINGS


def natural_language_search(user_query: str) -> NLSResponse:
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
        if not params.zipcode and not (params.city and params.state):
            missing_params.append("location (zipcode or city and state)")
        if not params.hcpcs_prefix:
            missing_params.append("procedure/service type")

        if missing_params:
            return NLSResponse(
                success=False,
                parsed_params=params.model_dump(),
                results=[],
                error=f"Could not determine: {', '.join(missing_params)}. Please provide more details.",
            )

        results = search_providers(
            specialty=params.specialty,
            hcpcs_prefix=params.hcpcs_prefix,
            city=params.city,
            state=params.state,
            zipcode=params.zipcode,
        )

        return NLSResponse(
            success=True,
            parsed_params=params.model_dump(),
            results=results,
            hcpcs_desc=HCPCS_MAPPINGS.get(params.hcpcs_prefix),
            count=len(results),
        )

    except Exception:
        return NLSResponse(
            success=False,
            parsed_params={},
            results=[],
            error="Internal error. Please try again",
        )


def rank_providers_nl(user_input: str, providers: list[int]) -> RankedProvidersResponse:
    """
    Main function to rank providers based on natural language input.

    Args:
        user_input: Natural language input from the user
        provider_ids: List of provider IDs to consider for ranking

    Returns:
        Dictionary containing parsed demographics, ranked providers, and scores
    """
    try:
        user_demographics = parse_user_demographics(user_input)

        if not any(
            [user_demographics.age, user_demographics.sex, user_demographics.race]
        ):
            return RankedProvidersResponse(
                success=False,
                parsed_params=user_demographics.model_dump(),
                results=[],
                error="Could not determine age, sex, or race from input. Please provide more details.",
            )

        provider_demographics = get_provider_demographics(providers)
        score_results: list[ScoredProvider] = []

        for prov in provider_demographics:
            score = compute_score(prov, user_demographics)
            scored = ScoredProvider(**prov.model_dump(), score=score)
            score_results.append(scored)

        score_results.sort(key=lambda p: p.score, reverse=True)

        # Normalize so top is 100
        top_score = score_results[0].score if score_results else 0
        if top_score > 0:
            for p in score_results:
                p.score = (p.score / top_score) * 100

        score_results.sort(key=lambda p: p.score, reverse=True)
        for i, p in enumerate(score_results):
            p.rank = i + 1

        return RankedProvidersResponse(
            success=True,
            parsed_params=user_demographics.model_dump(),
            results=score_results,
        )

    except Exception:
        return RankedProvidersResponse(
            success=False,
            parsed_params={},
            results=[],
            error="Internal error. Please try again",
        )


def compute_score(provider: ProviderDemographics, user: UserDemographics):
    sex_score = 0
    age_score = 0
    race_score = 0

    if user.sex:
        male = provider.bene_male_cnt
        female = provider.bene_feml_cnt

        if male and female and male + female != 0:
            total = male + female

            if user.sex == "male":
                sex_score = (male / total) * 100
            else:
                sex_score = (female / total) * 100

    if user.age and provider.avg_age:
        diff = abs(user.age - provider.avg_age)
        max_diff = 30
        age_score = max(0, ((max_diff - diff) / max_diff) * 100)

    if user.race:
        total = 0
        user_race = 0

        if provider.bene_race_wht_cnt:
            total += provider.bene_race_wht_cnt
            if user.race == "white":
                user_race = provider.bene_race_wht_cnt

        if provider.bene_race_black_cnt:
            total += provider.bene_race_black_cnt
            if user.race == "black":
                user_race = provider.bene_race_black_cnt

        if provider.bene_race_api_cnt:
            total += provider.bene_race_api_cnt
            if user.race == "asian":
                user_race = provider.bene_race_api_cnt

        if provider.bene_race_hspnc_cnt:
            total += provider.bene_race_hspnc_cnt
            if user.race == "hispanic":
                user_race = provider.bene_race_hspnc_cnt

        if provider.bene_race_nat_ind_cnt:
            total += provider.bene_race_nat_ind_cnt
            if user.race == "native":
                user_race = provider.bene_race_nat_ind_cnt

        if provider.bene_race_othr_cnt:
            total += provider.bene_race_othr_cnt
            if user.race == "other":
                user_race = provider.bene_race_othr_cnt

        if total != 0:
            race_score = (user_race / total) * 100

    return (sex_score * 0.4) + (race_score * 0.4) + (age_score * 0.2)
