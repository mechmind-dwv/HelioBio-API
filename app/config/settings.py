### app/config/settings.py
#!/usr/bin/env python3
"""
Configuración central del sistema HelioBio-API
"""
from pydantic import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Información del proyecto
    PROJECT_NAME: str = "HelioBio-API"
    PROJECT_VERSION: str = "3.0.0"
    PROJECT_DESCRIPTION: str = "Sistema Avanzado de Análisis Heliobiológico"
    
    # Información del autor (siguiendo las especificaciones)
    AUTHOR_NAME: str = "mechmind-dwv"
    AUTHOR_EMAIL: str = "ia.mechmind@gmail.com"
    GITHUB_REPO: str = "https://github.com/mechmind-dwv/HelioBio-API"
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True
    
    # Base de datos
    DATABASE_URL: str = "sqlite:///./data/heliobio_database.db"
    
    # URLs de fuentes de datos oficiales
    SILSO_SUNSPOT_URL: str = "https://www.sidc.be/silso/DATA/SN_m_tot_V2.0.csv"
    NOAA_SOLAR_URL: str = "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json"
    NOAA_GEOMAG_URL: str = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    NOAA_SPACE_WEATHER_URL: str = "https://services.swpc.noaa.gov/products/summary.json"
    
    # Configuración de cache
    CACHE_DURATION_HOURS: int = 1
    MAX_CACHE_SIZE_MB: int = 100
    
    # Configuración de análisis
    MIN_DATA_POINTS: int = 50
    DEFAULT_FORECAST_MONTHS: int = 24
    CORRELATION_SIGNIFICANCE_LEVEL: float = 0.05
    
    # Configuración de alertas
    ALERT_EXPIRY_DAYS: int = 30
    MAX_ACTIVE_ALERTS: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./data/logs/heliobio.log"
    
    class Config:
        env_file = ".env"

settings = Settings()
