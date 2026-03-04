import dns.resolver
from typing import Dict, Any

class DNSService:
    @staticmethod
    def get_dns_info(domain: str) -> Dict[str, Any]:
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
        results = {"domain": domain, "records": {}, "status": "success"}

        # On crée un résolveur personnalisé
        resolver = dns.resolver.Resolver()
        
        # ON FORCE DES SERVEURS DNS PUBLICS (Google et Cloudflare)
        resolver.nameservers = ['8.8.8.8', '1.1.1.1']
        
        # On augmente un peu le temps d'attente
        resolver.timeout = 10
        resolver.lifetime = 10

        for record in record_types:
            try:
                answers = resolver.resolve(domain, record)
                results["records"][record] = [str(rdata) for rdata in answers]
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                results["records"][record] = []
            except Exception as e:
                results["records"][record] = [f"Error: {str(e)}"]

        return results