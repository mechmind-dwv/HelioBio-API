#!/usr/bin/env python3
"""
Módulo 3: Sistema de Obtención de Datos - HelioBio-API
Sistema robusto para obtener datos de fuentes oficiales:
- SILSO (Royal Observatory Belgium) - Manchas solares
- NOAA Space Weather - Actividad solar y geomagnética  
- OMS/WHO - Datos epidemiológicos
- Otras fuentes científicas verificadas

Autor: mechmind-dwv
Email: ia.mechmind@gmail.com
GitHub: https://github.com/mechmind-dwv/HelioBio-API
"""

import asyncio
import aiohttp
import aiofiles
import pandas as pd
import numpy as np
import json
import csv
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import hashlib
import logging
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from enum import Enum
import time
import gzip
import io

# Configuración de logging
logger = logging.getLogger(__name__)

class DataSource(Enum):
    """Fuentes de datos oficiales"""
    SILSO = "silso"
    NOAA_SOLAR = "noaa_solar"
    NOAA_GEOMAG = "noaa_geomagnetic"
    NOAA_SPACE_WEATHER = "noaa_space_weather"
    WHO_HEALTH = "who_health"
    CDC_EPIDEMIO = "cdc_epidemiological"

@dataclass
class DataSourceConfig:
    """Configuración para cada fuente de datos"""
    name: str
    base_url: str
    endpoints: Dict[str, str]
    update_frequency_hours: int
    timeout_seconds: int
    retry_attempts: int
    requires_api_key: bool
    rate_limit_per_hour: int
    cache_duration_hours: int

class OfficialDataSources:
    """Configuraciones de fuentes de datos oficiales"""
    
    SOURCES = {
        DataSource.SILSO: DataSourceConfig(
            name="SILSO - Royal Observatory of Belgium",
            base_url="https://www.sidc.be/silso/",
            endpoints={
                "monthly_sunspots": "DATA/SN_m_tot_V2.0.csv",
                "daily_sunspots": "DATA/SN_d_tot_V2.0.csv",
                "yearly_sunspots": "DATA/SN_y_tot_V2.0.csv",
                "solar_cycles": "DATA/table_cycle.txt"
            },
            update_frequency_hours=24,
            timeout_seconds=30,
            retry_attempts=3,
            requires_api_key=False,
            rate_limit_per_hour=100,
            cache_duration_hours=6
        ),
        
        DataSource.NOAA_SOLAR: DataSourceConfig(
            name="NOAA Space Weather Prediction Center",
            base_url="https://services.swpc.noaa.gov/",
            endpoints={
                "solar_cycle_indices": "json/solar-cycle/observed-solar-cycle-indices.json",
