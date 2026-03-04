"""
Test script for modules/network/
Tests each service to identify import errors, missing dependencies, and runtime issues.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("TESTING NETWORK MODULES")
print("=" * 70)

# Test 1: IP Resolution Service
print("\n[1] Testing IPResolutionService...")
try:
    from app.modules.network.ip_resolution_service import IPResolutionService
    print("✓ Import successful")
    
    # Test validate_ip
    print("  - Testing validate_ip('8.8.8.8')...")
    result = IPResolutionService.validate_ip('8.8.8.8')
    print(f"    ✓ Result: {result}")
    
    # Test resolve_domain (with timeout to avoid hanging)
    print("  - Testing resolve_domain('google.com')...")
    result = IPResolutionService.resolve_domain('google.com')
    print(f"    ✓ Result: {result}")
    
except ImportError as e:
    print(f"✗ Import Error: {e}")
except Exception as e:
    print(f"✗ Runtime Error: {e}")

# Test 2: ASN Service
print("\n[2] Testing ASNService...")
try:
    from app.modules.network.asn_service import ASNService
    print("✓ Import successful")
    
    # Test ASN lookup
    print("  - Testing lookup_asn('8.8.8.8')...")
    result = ASNService.lookup_asn('8.8.8.8')
    print(f"    ✓ Result: {result}")
    
except ImportError as e:
    print(f"✗ Import Error: {e}")
except Exception as e:
    print(f"✗ Runtime Error: {e}")

# Test 3: Geo Service
print("\n[3] Testing GeoService...")
try:
    from app.modules.network.geo_service import GeoService
    print("✓ Import successful")
    
    # Check if GeoLite2 database exists
    import os
    db_path = GeoService.DB_PATH
    exists = os.path.exists(db_path)
    print(f"  - GeoLite2-City.mmdb exists: {exists}")
    
    if exists:
        print("  - Testing get_geo_info('8.8.8.8')...")
        result = GeoService.get_geo_info('8.8.8.8')
        print(f"    ✓ Result: {result}")
    else:
        print(f"    ⚠ Database not found at '{db_path}'")
        print(f"    This service will return {'ip': '...', 'country': None}")
    
except ImportError as e:
    print(f"✗ Import Error: {e}")
except Exception as e:
    print(f"✗ Runtime Error: {e}")

# Test 4: Discovery Service
print("\n[4] Testing DiscoveryService...")
try:
    from app.modules.network.discovery_service import DiscoveryService
    print("✓ Import successful")
    
    # Test CIDR detection
    print("  - Testing detect_cidr_from_ip('192.168.1.1')...")
    result = DiscoveryService.detect_cidr_from_ip('192.168.1.1')
    print(f"    ✓ Result: {result}")
    
    # Test ping on localhost (should work on all platforms)
    print("  - Testing ping_host('127.0.0.1')...")
    result = DiscoveryService.ping_host('127.0.0.1')
    print(f"    ✓ Result: {result}")
    print(f"    ⚠ Note: ping command uses Unix syntax (-c, -W). May fail on Windows.")
    
except ImportError as e:
    print(f"✗ Import Error: {e}")
except Exception as e:
    print(f"✗ Runtime Error: {e}")

print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print("""
Dependencies needed (install with pip):
  - dnspython     (for IPResolutionService)
  - ipwhois       (for ASNService)
  - geoip2        (for GeoService)

Additional requirements:
  - GeoLite2-City.mmdb database (required by GeoService)
    Download from: https://dev.maxmind.com/geoip/geolite2-city/
    Place it in the backend/app directory

Platform issues:
  - discovery_service.ping_host() uses Unix ping syntax (-c, -W)
    Not compatible with Windows. Need conditional logic.
""")
