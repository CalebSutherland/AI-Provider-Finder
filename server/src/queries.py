from db import engine
from sqlalchemy import text


def search_providers(specialty: str, city: str, state: str, hcpcs_prefix: str):
    query = text(
        """
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
        WHERE p.rndrng_prvdr_state_abrvtn = :state
          AND p.rndrng_prvdr_city = :city
          AND p.rndrng_prvdr_type = :specialty
          AND s.hcpcs_cd LIKE :hcpcs
        GROUP BY p.rndrng_npi
        LIMIT 10000
    """
    )

    with engine.connect() as conn:
        rows = conn.execute(
            query,
            {
                "state": state,
                "city": city,
                "specialty": specialty,
                "hcpcs": f"{hcpcs_prefix}%",
            },
        ).fetchall()

    return [r._mapping for r in rows]
