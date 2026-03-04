# modules/network/geo_service.py

import geoip2.database
from typing import Dict


class GeoService:

    DB_PATH = "GeoLite2-City.mmdb"

    @staticmethod
    def get_geo_info(ip: str) -> Dict:
        try:
            with geoip2.database.Reader(GeoService.DB_PATH) as reader:
                response = reader.city(ip)

                return {
                    "ip": ip,
                    "country": response.country.name,
                    "city": response.city.name,
                    "latitude": response.location.latitude,
                    "longitude": response.location.longitude,
                    "timezone": response.location.time_zone
                }
        except Exception:
            return {
                "ip": ip,
                "country": None
            }