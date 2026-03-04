import ssl
import socket
from datetime import datetime
from typing import Dict, Any

class SSLService:
    """
    Service pour analyser la validité et la configuration des certificats SSL/TLS.
    """

    @staticmethod
    def get_ssl_details(hostname: str) -> Dict[str, Any]:
        context = ssl.create_default_context()
        result = {
            "hostname": hostname,
            "is_valid": False,
            "issuer": None,
            "expires": None,
            "version": None,
            "error": None
        }

        try:
            # Connexion au serveur sur le port HTTPS (443)
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Extraction de l'émetteur
                    issuer = dict(x[0] for x in cert['issuer'])
                    result["issuer"] = issuer.get('organizationName', 'Unknown')
                    
                    # Conversion des dates
                    expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    result["expires"] = expire_date.isoformat()
                    result["is_valid"] = expire_date > datetime.now()
                    result["version"] = ssock.version()
                    
            return result

        except Exception as e:
            result["error"] = str(e)
            return result