from fastapi import APIRouter
from app.modules.osint.whois_service import WhoisService

router = APIRouter(prefix="/osint", tags=["OSINT"])


@router.get("/whois")
def get_whois(domain: str):
    """
    Retrieve WHOIS information for a given domain.
    Example: /osint/whois?domain=example.com
    """
    result = WhoisService.get_whois_info(domain)
    return result
