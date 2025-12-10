from sqlalchemy import text, bindparam
from db import engine
from models import Provider, ProviderDemographics


def search_providers(
    specialty: str,
    hcpcs_prefix: str,
    city: str | None = None,
    state: str | None = None,
    zipcode: str | None = None,
) -> list[Provider]:
    if zipcode:
        location_condition = "p.rndrng_prvdr_zip5 = :zipcode"
        location_params = {"zipcode": zipcode}
    elif city and state:
        location_condition = (
            "p.rndrng_prvdr_state_abrvtn = :state AND p.rndrng_prvdr_city = :city"
        )
        location_params = {"state": state, "city": city}
    else:
        raise ValueError("Must provide either zipcode or both city and state")

    query = text(
        f"""
        SELECT 
            p.rndrng_npi AS id,
            p.rndrng_prvdr_last_org_name AS last_name,
            p.rndrng_prvdr_first_name AS first_name,
            p.rndrng_prvdr_crdntls AS credentials,
            p.rndrng_prvdr_st1 AS street_1,
            p.rndrng_prvdr_st2 AS street_2,
            p.rndrng_prvdr_city AS city,
            p.rndrng_prvdr_state_abrvtn AS state,
            p.rndrng_prvdr_zip5 AS zipcode,
            p.rndrng_prvdr_type AS specialty,
            p.rndrng_prvdr_mdcr_prtcptg_ind AS accepts_medicare,
            p.tot_benes AS total_benes,
            p.bene_avg_age AS avg_age
        FROM providers p
        JOIN provider_services s 
            ON p.rndrng_npi = s.rndrng_npi
        WHERE {location_condition}
          AND p.rndrng_prvdr_type = :specialty
          AND s.hcpcs_cd LIKE :hcpcs
        GROUP BY p.rndrng_npi
        LIMIT 10000
        """
    )

    params = {
        **location_params,
        "specialty": specialty,
        "hcpcs": f"{hcpcs_prefix}%",
    }

    with engine.connect() as conn:
        rows = conn.execute(query, params).mappings().all()

    return [Provider(**row) for row in rows]


def get_provider_demographics(provider_ids: list[int]) -> list[ProviderDemographics]:
    if not provider_ids:
        return []

    query = text(
        """
        SELECT
            rndrng_npi AS id,
            rndrng_prvdr_last_org_name AS last_name,
            rndrng_prvdr_first_name AS first_name,
            rndrng_prvdr_crdntls AS credentials,
            rndrng_prvdr_st1 AS street_1,
            rndrng_prvdr_st2 AS street_2,
            rndrng_prvdr_city AS city,
            rndrng_prvdr_state_abrvtn AS state,
            rndrng_prvdr_zip5 AS zipcode,
            rndrng_prvdr_type AS specialty,
            rndrng_prvdr_mdcr_prtcptg_ind AS accepts_medicare,
            tot_benes AS total_benes,
            bene_avg_age AS avg_age,
        
            bene_avg_age,
            bene_age_lt_65_cnt,
            bene_age_65_74_cnt,
            bene_age_75_84_cnt,
            bene_age_gt_84_cnt,
            bene_feml_cnt,
            bene_male_cnt,
            bene_race_wht_cnt,
            bene_race_black_cnt,
            bene_race_api_cnt,
            bene_race_hspnc_cnt,
            bene_race_nat_ind_cnt,
            bene_race_othr_cnt
        FROM providers
        WHERE rndrng_npi in :provider_ids
        """
    ).bindparams(bindparam("provider_ids", expanding=True))

    with engine.connect() as conn:
        rows = conn.execute(query, {"provider_ids": provider_ids}).mappings().all()

    return [ProviderDemographics(**row) for row in rows]
