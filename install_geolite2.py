"""
GeoLite2 Database Installation Script
Downloads and installs the GeoLite2-City.mmdb database for Geo Service

Requirements:
1. Free MaxMind account (https://www.maxmind.com/en/geolite2/signup)
2. License key (available after signup)
"""

import os
import urllib.request
import urllib.error
import zipfile
import shutil
import sys
from pathlib import Path

# Configuration
BACKEND_APP_DIR = Path(__file__).parent / "app"
DB_DESTINATION = BACKEND_APP_DIR / "GeoLite2-City.mmdb"

# MaxMind Download URL (requires license key)
# Get your license key from: https://www.maxmind.com/en/account/login
MAXMIND_DOWNLOAD_URL = "https://download.maxmind.com/app/geoip_download"

def install_geolite2(license_key=None):
    """
    Download and install GeoLite2-City.mmdb
    
    Args:
        license_key: Your MaxMind license key (optional, will prompt if not provided)
    """
    
    print("=" * 70)
    print("GeoLite2-City Database Installation")
    print("=" * 70)
    
    # Check if already installed
    if DB_DESTINATION.exists():
        file_size = DB_DESTINATION.stat().st_size / (1024*1024)  # MB
        print(f"\n✓ Database already installed: {DB_DESTINATION}")
        print(f"  File size: {file_size:.2f} MB")
        return True
    
    # Get license key if not provided
    if not license_key:
        print("\n⚠️  You need a MaxMind license key to download GeoLite2-City database.")
        print("\nSteps to get your license key:")
        print("  1. Create free account: https://www.maxmind.com/en/geolite2/signup")
        print("  2. Go to: https://www.maxmind.com/en/account/login")
        print("  3. Click 'Manage License Keys'")
        print("  4. Copy your license key")
        print("\nEnter your license key (or 'skip' to proceed manually):")
        license_key = input("> ").strip()
        
        if license_key.lower() == 'skip':
            print("\n⚠️  Skipping automatic download.")
            print("\nTo install manually:")
            print("  1. Download from: https://www.maxmind.com/en/account/login")
            print("  2. Extract GeoLite2-City.mmdb")
            print(f"  3. Copy to: {DB_DESTINATION}")
            return False
    
    # Download the database
    print(f"\n⏳ Downloading GeoLite2-City.mmdb...")
    
    try:
        # Build download URL with license key
        url = f"{MAXMIND_DOWNLOAD_URL}?edition_id=GeoLite2-City&license_key={license_key}&suffix=tar.gz"
        
        # Alternative: tar.gz instead of zip
        zip_file = BACKEND_APP_DIR / "GeoLite2-City.tar.gz"
        
        print(f"  URL: {url[:80]}...")
        
        # Download file
        import subprocess
        result = subprocess.run(
            ["curl", "-L", "-o", str(zip_file), url],
            capture_output=True,
            timeout=60
        )
        
        if result.returncode != 0:
            # Fallback: Try with urllib
            print("  Using urllib (curl not available)...")
            urllib.request.urlretrieve(url, zip_file)
        
        if not zip_file.exists():
            print("✗ Download failed!")
            return False
        
        print(f"✓ Downloaded: {zip_file.stat().st_size / (1024*1024):.2f} MB")
        
        # Extract the database
        print(f"\n⏳ Extracting database...")
        
        if str(zip_file).endswith('.tar.gz'):
            import tarfile
            with tarfile.open(zip_file, 'r:gz') as tar:
                # Find the .mmdb file in the archive
                for member in tar.getmembers():
                    if member.name.endswith('GeoLite2-City.mmdb'):
                        # Extract to destination
                        tar.extract(member, path=BACKEND_APP_DIR)
                        extracted_path = BACKEND_APP_DIR / member.name
                        # Move to final location
                        shutil.move(str(extracted_path), str(DB_DESTINATION))
                        break
        else:
            # Handle zip files
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                for name in zip_ref.namelist():
                    if name.endswith('GeoLite2-City.mmdb'):
                        # Extract directly to destination
                        with zip_ref.open(name) as source, open(DB_DESTINATION, 'wb') as target:
                            target.write(source.read())
                        break
        
        # Clean up
        zip_file.unlink()
        
        # Verify
        if DB_DESTINATION.exists():
            file_size = DB_DESTINATION.stat().st_size / (1024*1024)
            print(f"✓ Installation complete!")
            print(f"✓ Database size: {file_size:.2f} MB")
            print(f"✓ Location: {DB_DESTINATION}")
            return True
        else:
            print("✗ Extraction failed - database file not found!")
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nManual installation instead:")
        print("  1. Visit: https://www.maxmind.com/en/account/login")
        print("  2. Download GeoLite2-City database")
        print("  3. Extract the .mmdb file")
        print(f"  4. Copy to: {DB_DESTINATION}")
        return False

def manual_install_instructions():
    """Print manual installation instructions"""
    print("\n" + "=" * 70)
    print("Manual Installation Instructions")
    print("=" * 70)
    print("""
1. Create a MaxMind account (free):
   https://www.maxmind.com/en/geolite2/signup

2. Log in to your account:
   https://www.maxmind.com/en/account/login

3. Download GeoLite2-City database:
   - Look for "Download" link in GeoLite2-City section
   - Choose .tar.gz or .zip format

4. Extract the archive:
   - On Windows: Use 7-Zip, WinRAR, or built-in extraction
   - On Linux/Mac: tar -xzf GeoLite2-City_*.tar.gz

5. Copy GeoLite2-City.mmdb to:
   """ + str(DB_DESTINATION) + """

6. Verify installation by running geo_service:
   python -c "from app.modules.network.geo_service import GeoService; print(GeoService.get_geo_info('8.8.8.8'))"
    """)

def verify_installation():
    """Verify the database is working"""
    print("\n" + "=" * 70)
    print("Verifying Installation...")
    print("=" * 70)
    
    if not DB_DESTINATION.exists():
        print(f"\n✗ Database not found at: {DB_DESTINATION}")
        return False
    
    try:
        import geoip2.database
        
        with geoip2.database.Reader(str(DB_DESTINATION)) as reader:
            # Test with Google DNS
            response = reader.city('8.8.8.8')
            print(f"\n✓ Database is working!")
            print(f"  Test IP: 8.8.8.8")
            print(f"  Country: {response.country.name}")
            print(f"  City: {response.city.name}")
            print(f"  Coordinates: {response.location.latitude}, {response.location.longitude}")
            return True
            
    except Exception as e:
        print(f"\n✗ Error reading database: {e}")
        return False

if __name__ == "__main__":
    print("\nGeoLite2 Database Installer")
    print("-" * 70)
    
    # Check if we have curl or internet connectivity
    license_key = None
    
    # Try to get license key from environment variable
    if 'MAXMIND_LICENSE_KEY' in os.environ:
        license_key = os.environ['MAXMIND_LICENSE_KEY']
        print("✓ Using license key from MAXMIND_LICENSE_KEY environment variable")
    
    # Attempt automatic installation
    success = install_geolite2(license_key)
    
    if success:
        # Verify
        verify_installation()
        print("\n✓ GeoLite2-City.mmdb is ready to use!")
    else:
        print("\n" + "=" * 70)
        print("ALTERNATIVE: Manual Installation")
        print("=" * 70)
        manual_install_instructions()
        print("\n" + "=" * 70)
        print("After manual installation, run this command to verify:")
        print(f"  python {__file__} --verify")
        print("=" * 70)
    
    # Accept command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--verify':
            verify_installation()
        elif sys.argv[1] == '--license-key':
            if len(sys.argv) > 2:
                install_geolite2(sys.argv[2])
            else:
                print("Usage: python install_geolite2.py --license-key YOUR_KEY")
