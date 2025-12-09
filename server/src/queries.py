from typing import Optional

from sqlalchemy import text
from db import engine


def search_providers(specialty: str, hcpcs_prefix: str, city: Optional[str] = None, state: Optional[str] = None, zipcode: Optional[str] = None):
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
            p.rndrng_npi,
            p.rndrng_prvdr_last_org_name,
            p.rndrng_prvdr_first_name,
            p.rndrng_prvdr_city,
            p.rndrng_prvdr_state_abrvtn,
            p.rndrng_prvdr_type
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

    return [r._mapping for r in rows]
