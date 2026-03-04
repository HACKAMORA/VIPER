# Script de téléchargement rapide pour GeoLite2-City.mmdb
# Utilisation: .\install_geolite2.ps1 -LicenseKey "votre_cle_ici"

param(
    [string]$LicenseKey = ""
)

$BackendPath = "$PSScriptRoot\app"
$DbPath = "$BackendPath\GeoLite2-City.mmdb"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "GeoLite2 Installation Script" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check if already installed
if (Test-Path $DbPath) {
    $Size = (Get-Item $DbPath).Length / 1MB
    Write-Host "✓ Database already installed!" -ForegroundColor Green
    Write-Host "  Path: $DbPath"
    Write-Host "  Size: $([Math]::Round($Size, 2)) MB`n"
    exit 0
}

# Get license key if not provided
if ([string]::IsNullOrEmpty($LicenseKey)) {
    Write-Host "GeoLite2 requires a free MaxMind account" -ForegroundColor Yellow
    Write-Host "Steps:" -ForegroundColor Yellow
    Write-Host "  1. Signup: https://www.maxmind.com/en/geolite2/signup"
    Write-Host "  2. Login: https://www.maxmind.com/en/account/login"
    Write-Host "  3. Click 'Manage License Keys' and copy your key`n"
    
    $LicenseKey = Read-Host "Enter your MaxMind License Key (or press Enter to skip)"
    
    if ([string]::IsNullOrEmpty($LicenseKey)) {
        Write-Host "`n⚠️  Skipped. Manual installation:" -ForegroundColor Yellow
        Write-Host "  https://github.com/yourusername/backend/GEOLITE2_INSTALLATION.md`n"
        exit 0
    }
}

# Download URL
$Url = "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=$LicenseKey&suffix=tar.gz"
$ZipPath = "$BackendPath\GeoLite2-City.tar.gz"

Write-Host "⏳ Downloading database..." -ForegroundColor Cyan
try {
    # Try with Invoke-WebRequest (PowerShell 5.1+)
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $Url -OutFile $ZipPath -TimeoutSec 60
    
    if (-Not (Test-Path $ZipPath)) {
        throw "Download failed"
    }
    
    $Size = (Get-Item $ZipPath).Length / 1MB
    Write-Host "✓ Downloaded: $([Math]::Round($Size, 2)) MB" -ForegroundColor Green
    
    # Extract using tar (Windows 10+)
    Write-Host "⏳ Extracting..." -ForegroundColor Cyan
    tar -xzf $ZipPath -C $BackendPath
    
    # Find and move the .mmdb file
    $MmdbFile = Get-ChildItem -Path $BackendPath -Filter "*.mmdb" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    
    if ($MmdbFile) {
        Move-Item -Path $MmdbFile.FullName -Destination $DbPath -Force
        Write-Host "✓ Installation complete!" -ForegroundColor Green
        Write-Host "  Location: $DbPath`n"
        
        # Cleanup
        Remove-Item $ZipPath -Force -ErrorAction SilentlyContinue
        
        # Test
        Write-Host "✓ Testing database..." -ForegroundColor Cyan
        python -c "import geoip2.database; reader=geoip2.database.Reader('$DbPath'); resp=reader.city('8.8.8.8'); print('✓ Database works! Country:', resp.country.name)" -ErrorAction SilentlyContinue
    }
    else {
        Write-Host "✗ Could not find .mmdb file in archive" -ForegroundColor Red
    }
}
catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
    Write-Host "`n💡 Try manual download:" -ForegroundColor Yellow
    Write-Host "  Open this link in your browser:"
    Write-Host "  https://www.maxmind.com/en/account/login"
    Write-Host "`n  Then save file to: $DbPath"
}
