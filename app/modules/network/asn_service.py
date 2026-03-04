# modules/network/asn_service.py

from ipwhois import IPWhois
from typing import Dict


class ASNService:

    @staticmethod
    def lookup_asn(ip: str) -> Dict:
        try:
            obj = IPWhois(ip)
            result = obj.lookup_rdap()

            return {
                "ip": ip,
                "asn": result.get("asn"),
                "asn_description": result.get("asn_description"),
                "network_name": result.get("network", {}).get("name"),
                "cidr": result.get("network", {}).get("cidr"),
                "country": result.get("network", {}).get("country")
            }
        except Exception:
            return {
                "ip": ip,
                "asn": None
            }