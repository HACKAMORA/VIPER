import requests
import re
from typing import Set, Dict, Any

class SubdomainService:
    """
    Service OSINT Avancé : Extraction via Certificate Transparency (crt.sh)
    """

    @staticmethod
    def get_subdomains(domain: str) -> Dict[str, Any]:
        subdomains: Set[str] = set()
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        
        try:
            # On interroge les logs de certificats publics
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                for entry in data:
                    # Le champ 'name_value' contient souvent plusieurs domaines séparés par \n
                    names = entry['name_value'].split('\n')
                    for name in names:
                        # Nettoyage : enlever les wildcards (*.) et mettre en minuscule
                        name = name.replace('*.', '').lower().strip()
                        if name.endswith(domain) and name != domain:
                            subdomains.add(name)
            
            return {
                "domain": domain,
                "method": "Certificate Transparency (Passive)",
                "count": len(subdomains),
                "subdomains": sorted(list(subdomains))
            }

        except Exception as e:
            return {"domain": domain, "error": str(e), "subdomains": []}
