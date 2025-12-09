from typing import List, Optional

from sqlalchemy import text
from db import engine
from models import Provider


def search_providers(specialty: str, hcpcs_prefix: str, city: Optional[str] = None, state: Optional[str] = None, zipcode: Optional[str] = None) -> List[Provider]:
    if zipcode:
        location_condition = "p.rndrng_prvdr_zip5 = :zipcode"
        location_params = {"zipcode": zipcode}
    elif city and state:
        location_condition = "p.rndrng_prvdr_state_abrvtn = :state AND p.rndrng_prvdr_city = :city"
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
        rows = conn.execute(query, params).fetchall()

    return [Provider(**dict(row._mapping)) for row in rows]
