import whois
from datetime import datetime
from typing import Optional, Dict, Any


class WhoisService:
    """
    Service responsible for retrieving and normalizing WHOIS information.
    """

    @staticmethod
    def _normalize_date(date_value) -> Optional[str]:
        """Convert WHOIS date to ISO format."""
        if not date_value:
            return None

        # Sometimes WHOIS returns a list
        if isinstance(date_value, list):
            date_value = date_value[0]

        if isinstance(date_value, datetime):
            return date_value.isoformat()

        return str(date_value)

    @staticmethod
    def get_whois_info(domain: str) -> Dict[str, Any]:
        """
        Retrieve WHOIS information for a domain.
        """

        try:
            w = whois.whois(domain)

            result = {
                "domain": domain,
                "registrar": w.registrar,
                "creation_date": WhoisService._normalize_date(w.creation_date),
                "expiration_date": WhoisService._normalize_date(w.expiration_date),
                "updated_date": WhoisService._normalize_date(w.updated_date),
                "name_servers": list(w.name_servers) if w.name_servers else [],
                "organization": getattr(w, "org", None),
                "emails": w.emails if isinstance(w.emails, list) else [w.emails] if w.emails else [],
            }

            return result

        except Exception as e:
            return {
                "domain": domain,
                "error": str(e),
                "registrar": None,
                "creation_date": None,
                "expiration_date": None,
                "updated_date": None,
                "name_servers": [],
                "organization": None,
                "emails": [],
            }