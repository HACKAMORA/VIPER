import time
from datetime import datetime
from modules.osint.whois_service import WhoisService
from modules.osint.dns_service import DNSService
from modules.osint.subdomain_service import SubdomainService
from modules.osint.ssl_service import SSLService
from modules.osint.tech_service import TechService

class OSINTOrchestrator:
    """
    Chef d'orchestre OSINT - Centralise la collecte d'informations
    """
    
    @staticmethod
    def run_full_analysis(domain: str):
        start_time = time.time()
        print(f"[*] [{datetime.now().strftime('%H:%M:%S')}] Début de l'analyse globale : {domain}")
        
        # Exécution des modules
        results = {}
        
        # 1. WHOIS
        print("[+] Récupération des données WHOIS...")
        results['whois'] = WhoisService.get_whois_info(domain)
        
        # 2. DNS
        print("[+] Interrogation des serveurs DNS (A, MX, TXT)...")
        results['dns'] = DNSService.get_dns_info(domain)
        
        # 3. Subdomains (La partie passive crt.sh)
        print("[+] Recherche de sous-domaines (Certificate Transparency)...")
        results['subdomains'] = SubdomainService.get_subdomains(domain)
        
        # 4. SSL
        print("[+] Analyse du certificat SSL/TLS...")
        results['ssl'] = SSLService.get_ssl_details(domain)
        
        # 5. Tech Stack
        print("[+] Fingerprinting technologique (Headers HTTP)...")
        results['tech'] = TechService.get_tech_info(domain)
        
        # Calcul de la durée
        duration = round(time.time() - start_time, 2)
        
        # Compilation du rapport final professionnel
        report = {
            "scan_info": {
                "target": domain,
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": duration,
                "status": "completed"
            },
            "data": results,
            "summary": {
                "subdomains_count": results['subdomains'].get("count", 0),
                "is_ssl_valid": results['ssl'].get("is_valid", False),
                "web_server": results['tech'].get("server", "N/A"),
                "detected_techs": results['tech'].get("technologies", [])
            }
        }
        
        print(f"[*] [{datetime.now().strftime('%H:%M:%S')}] Analyse terminée en {duration}s.")
        return report