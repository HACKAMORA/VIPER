from modules.osint.whois_service import WhoisService

domain = "google.com"

whois_service = WhoisService()
result = whois_service.get_whois_info(domain)

print(result)