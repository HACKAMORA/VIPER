from modules.osint.dns_service import DNSService

data = DNSService.get_dns_info("google.com")
print(data)