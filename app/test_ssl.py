from modules.osint.ssl_service import SSLService

# Test sur le domaine principal et un sous-domaine trouvé précédemment
target = "google.com"
print(f"Analyse SSL pour {target}...")
print(SSLService.get_ssl_details(target))