#!/usr/bin/env python3
"""
GeoLite2 Quick Install - Simplified Version
Run this to download and install GeoLite2-City.mmdb
"""

import os
import sys
from pathlib import Path

def show_instructions():
    """Show simplified installation instructions"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         GeoLite2-City.mmdb - Quick Installation Guide             ║
╚════════════════════════════════════════════════════════════════════╝

⏱️  Takes ~5 minutes total

STEP 1: Create Free MaxMind Account (2 min)
────────────────────────────────────────────────────────────────────
  Go to: https://www.maxmind.com/en/geolite2/signup
  Fill in your details
  Confirm email

STEP 2: Get Your License Key (1 min)
────────────────────────────────────────────────────────────────────
  Log in: https://www.maxmind.com/en/account/login
  Click: "Account" → "Manage License Keys"
  Copy your key (e.g., starts with letters/numbers)

STEP 3: Download Database (1 min)
────────────────────────────────────────────────────────────────────
  Replace YOUR_KEY below and open in browser:
  
  https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=YOUR_KEY&suffix=tar.gz
  
  The file GeoLite2-City_XXXXX.tar.gz will download

STEP 4: Extract (1 min)
────────────────────────────────────────────────────────────────────
  Windows: Right-click → "Extract All"
  Mac/Linux: tar -xzf GeoLite2-City_*.tar.gz
  
  Look for: GeoLite2-City.mmdb inside the folder

STEP 5: Copy to Backend (1 min)
────────────────────────────────────────────────────────────────────
  Copy the file to this exact path:
  
  viper.pfa/backend/app/GeoLite2-City.mmdb
  
  Your folder structure should look like:
  backend/
    └── app/
        ├── config.py
        ├── main.py
        ├── GeoLite2-City.mmdb    ← Place it here
        └── ...

DONE! ✓
────────────────────────────────────────────────────────────────────
  Your Geo Service is now ready to use!

TEST IT:
  python
  >>> from app.modules.network.geo_service import GeoService
  >>> GeoService.get_geo_info('8.8.8.8')
  {'ip': '8.8.8.8', 'country': 'United States', ...}

═════════════════════════════════════════════════════════════════════
""")

def check_existing():
    """Check if database already exists"""
    app_dir = Path(__file__).parent / "app"
    db_file = app_dir / "GeoLite2-City.mmdb"
    
    if db_file.exists():
        size = db_file.stat().st_size / 1024 / 1024
        print(f"\n✓ Database already installed!")
        print(f"  Location: {db_file}")
        print(f"  Size: {size:.1f} MB\n")
        return True
    
    return False

def main():
    if check_existing():
        sys.exit(0)
    
    show_instructions()

if __name__ == "__main__":
    main()
