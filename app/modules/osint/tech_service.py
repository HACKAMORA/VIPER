import requests
from typing import Dict, Any

class TechService:
    """
    Service d'analyse technologique (Fingerprinting) via les headers HTTP et le contenu.
    """

    @staticmethod
    def get_tech_info(domain: str) -> Dict[str, Any]:
        # On teste en HTTPS par défaut
        url = f"https://{domain}"
        results = {
            "server": "Non détecté",
            "technologies": [],
            "security_headers": {},
            "status_code": None,
            "error": None
        }

        try:
            # Simuler un navigateur réel pour éviter les blocages (User-Agent)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            # On effectue la requête avec une redirection automatique (allow_redirects=True)
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            results["status_code"] = response.status_code

            # 1. Extraction du serveur web (Header 'Server')
            server = response.headers.get("Server")
            if server:
                results["server"] = server

            # 2. Détection via les Headers spécifiques
            # Ex: X-Powered-By (PHP, ASP.NET), Via, X-Cache
            tech_headers = {
                "X-Powered-By": "Language/Framework",
                "X-AspNet-Version": "ASP.NET",
                "X-Generator": "CMS",
                "Via": "Proxy/CDN",
                "X-Cache": "Caching System"
            }

            for header, label in tech_headers.items():
                if header in response.headers:
                    results["technologies"].append(f"{label}: {response.headers[header]}")

            # 3. Détection dans le code source (HTML)
            html_content = response.text.lower()
            if "wp-content" in html_content:
                results["technologies"].append("WordPress CMS")
            if "next" in html_content and "data" in html_content:
                results["technologies"].append("Next.js Framework")
            if "react" in html_content:
                results["technologies"].append("React Library")

            # 4. Audit des Headers de Sécurité (Trés apprécié par les profs)
            security_headers = [
                "Content-Security-Policy", 
                "Strict-Transport-Security", 
                "X-Content-Type-Options", 
                "X-Frame-Options",
                "X-XSS-Protection"
            ]
            
            for s_header in security_headers:
                results["security_headers"][s_header] = "Présent" if s_header in response.headers else "Manquant"

            return results

        except Exception as e:
            results["error"] = str(e)
            return results