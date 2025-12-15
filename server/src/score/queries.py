from sqlalchemy import text, bindparam
from typing import cast
from ..score.models import ProviderDemographics
from ..config.db import engine


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
