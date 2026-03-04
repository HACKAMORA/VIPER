# routes/network_routes.py

from fastapi import APIRouter, Query
from typing import List
from modules.network.network_collector import NetworkCollector
from schemas.network_schema import NetworkResponse

router = APIRouter(
    prefix="/network",
    tags=["Network"]
)


@router.post("/collect", response_model=List[NetworkResponse])
def collect_network(domain: str = Query(..., description="Target domain")):
    return NetworkCollector.collect(domain)
    
@router.post("/collect")
def collect_network(domain: str):

    if not validate_domain(domain):
        raise HTTPException(status_code=400, detail="Invalid domain")

    result = NetworkCollector.collect(domain)

    return success_response(result)