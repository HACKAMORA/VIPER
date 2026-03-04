# core/security.py

import re


def validate_domain(domain: str) -> bool:
    pattern = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    return re.match(pattern, domain) is not None