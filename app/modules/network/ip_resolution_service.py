# modules/network/ip_resolution_service.py

import socket
import dns.resolver
from typing import List, Dict


class IPResolutionService:

    @staticmethod
    def resolve_domain(domain: str) -> List[str]:
        """Resolve domain to IPv4 addresses"""
        try:
            answers = dns.resolver.resolve(domain, 'A')
            return [rdata.to_text() for rdata in answers]
        except Exception:
            return []

    @staticmethod
    def reverse_dns(ip: str) -> str:
        """Reverse DNS lookup"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return None

    @staticmethod
    def validate_ip(ip: str) -> bool:
        """Validate IPv4 format"""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    @staticmethod
    def get_ip_info(domain: str) -> Dict:
        ips = IPResolutionService.resolve_domain(domain)

        results = []
        for ip in ips:
            results.append({
                "ip": ip,
                "reverse_dns": IPResolutionService.reverse_dns(ip)
            })

        return {
            "domain": domain,
            "resolved_ips": results
        }