@echo off
REM Quick GeoLite2 Installation Script
REM Usage: run_install.bat

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo GeoLite2-City.mmdb Installation Helper
echo ================================================================================
echo.
echo This script will help you install the GeoLite2-City database.
echo.
echo Prerequisites:
echo   1. Free MaxMind account: https://www.maxmind.com/en/geolite2/signup
echo   2. License key from: https://www.maxmind.com/en/account/login
echo.
echo ================================================================================
echo.

REM Check if database already exists
if exist "app\GeoLite2-City.mmdb" (
    echo [OK] Database already installed at: app\GeoLite2-City.mmdb
    echo.
    pause
    exit /b 0
)

echo What would you like to do?
echo.
echo 1) Download automatically (requires license key)
echo 2) Manual installation instructions
echo 3) Skip for now (use other services)
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Enter your MaxMind License Key:
    echo (You can find it at: https://www.maxmind.com/en/account/login)
    echo.
    set /p license_key="License Key: "
    
    if not "!license_key!"=="" (
        echo.
        echo Downloading...
        echo.
        
        REM Download using PowerShell (Windows 10+)
        powershell -Command "try { $ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City^&license_key=!license_key!^&suffix=tar.gz' -OutFile 'GeoLite2.tar.gz' -TimeoutSec 60; Write-Host 'Download complete'; tar -xzf GeoLite2.tar.gz -C app; if (Test-Path 'app/*.mmdb') { Get-ChildItem -Path 'app' -Filter '*.mmdb' -Recurse | Move-Item -Destination 'app/GeoLite2-City.mmdb' -Force; Write-Host 'Installation successful!'; Remove-Item 'GeoLite2.tar.gz' -Force } } catch { Write-Host 'Error: $_' -ForegroundColor Red }"
    ) else (
        echo License key not provided. Switching to manual installation...
        goto manual
    )
) else if "%choice%"=="2" (
    goto manual
) else (
    echo Skipped. You can install GeoLite2 later.
    echo.
    pause
    exit /b 0
)

echo.
echo ================================================================================
echo.
echo Testing database...
python -c "import geoip2.database; r=geoip2.database.Reader('app/GeoLite2-City.mmdb'); print('[OK] Database is working!')" 2>nul || echo [WARNING] Database test skipped

pause
exit /b 0

:manual
cls
echo.
echo ================================================================================
echo MANUAL INSTALLATION INSTRUCTIONS
echo ================================================================================
echo.
echo Step 1: Create MaxMind Account
echo   - Go to: https://www.maxmind.com/en/geolite2/signup
echo   - Complete the free registration
echo.
echo Step 2: Get Your License Key
echo   - Login at: https://www.maxmind.com/en/account/login
echo   - Click "Manage License Keys"
echo   - Copy your license key
echo.
echo Step 3: Download the Database
echo   - Click the download link for GeoLite2-City
echo   - Save the .tar.gz or .zip file
echo.
echo Step 4: Extract the Archive
echo   - Extract using 7-Zip, WinRAR, or built-in Windows extraction
echo   - Find the file named "GeoLite2-City.mmdb"
echo.
echo Step 5: Copy to Backend Directory
echo   - Copy GeoLite2-City.mmdb to:
echo     backend\app\GeoLite2-City.mmdb
echo.
echo Step 6: Verify (Optional)
echo   - Open Python:
echo     python
echo   - Run:
echo     from app.modules.network.geo_service import GeoService
echo     result = GeoService.get_geo_info('8.8.8.8')
echo     print(result)
echo   - If you see a country name, it's working!
echo.
echo ================================================================================
echo.
echo Alternative: Continue without GeoLite2
echo   - Services that work without GeoLite2:
echo     * IP Resolution Service
echo     * ASN Service
echo     * Discovery Service (Network Scanning)
echo.
echo   - GeoService will return: {'ip': '...', 'country': None}
echo.
echo ================================================================================
echo.
pause
