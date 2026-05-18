"""Datos de clima espacial en tiempo real de NOAA"""
import aiohttp
from datetime import datetime
from typing import Dict, Any

NOAA_SPACE_WEATHER_URL = "https://services.swpc.noaa.gov/products/summary.json"

async def fetch_real_space_weather() -> Dict[str, Any]:
    """Obtiene datos reales del clima espacial actual de NOAA"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(NOAA_SPACE_WEATHER_URL, 
                                  timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "timestamp": datetime.now().isoformat(),
                        "solar_activity": data.get("SolarActivity", "N/A"),
                        "geomagnetic_activity": data.get("GeomagneticActivity", "N/A"),
                        "solar_wind_speed": data.get("SolarWindSpeed", None),
                        "proton_flux": data.get("ProtonFlux", None),
                        "xray_flux": data.get("XRayFlux", None),
                        "source": "NOAA Space Weather Prediction Center",
                        "url": "https://www.swpc.noaa.gov/"
                    }
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "unavailable",
            "error": str(e),
            "message": "NOAA data temporarily unavailable",
            "source": "NOAA Space Weather Prediction Center"
        }
