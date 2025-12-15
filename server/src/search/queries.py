from typing import cast
from sqlalchemy import text
from .models import ProviderRow, SearchResult
from ..config.db import engine


def fetch_providers(
    specialty: str,
    hcpcs_prefix: str | None = None,
    zipcode: str | None = None,
    state: str | None = None,
    city: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> SearchResult:

    offset = (page - 1) * page_size

    conditions = ["p.rndrng_prvdr_type = :specialty"]
    params = {
        "specialty": specialty,
        "page_size": page_size,
        "offset": offset,
    }

    if zipcode:
        conditions.append("p.rndrng_prvdr_zip5 = :zipcode")
        params["zipcode"] = zipcode
    elif city and state:
        conditions.append(
            "p.rndrng_prvdr_state_abrvtn = :state AND p.rndrng_prvdr_city = :city"
        )
        params.update({"state": state, "city": city})
    elif state:
        conditions.append("p.rndrng_prvdr_state_abrvtn = :state")
        params["state"] = state

    if hcpcs_prefix:
        conditions.append(
            """
            EXISTS (
                SELECT 1
                FROM provider_services s
                WHERE s.rndrng_npi = p.rndrng_npi
                AND s.hcpcs_cd LIKE :hcpcs
            )
            """
        )
        params["hcpcs"] = f"{hcpcs_prefix}%"

    where_clause = " AND ".join(conditions)

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
        WHERE {where_clause}
        ORDER BY p.rndrng_npi
        LIMIT :page_size OFFSET :offset
        """
    )

    count_query = text(
        f"""
        SELECT COUNT(*)
        FROM providers p
        WHERE {where_clause}
        """
    )

    with engine.connect() as conn:
        rows = conn.execute(query, params).mappings().all()
        total = conn.execute(count_query, params).scalar()

    return {"result": cast(list[ProviderRow], rows), "count": total or 0}
