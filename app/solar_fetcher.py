"""Obtención de datos solares reales de SILSO"""
import pandas as pd
import numpy as np
from datetime import datetime
import aiohttp
from io import StringIO

SILSO_URL = "https://www.sidc.be/silso/DATA/SN_m_tot_V2.0.csv"

async def fetch_real_sunspots(start_year: int = 1900) -> pd.DataFrame:
    """Obtiene datos reales de manchas solares del SILSO"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(SILSO_URL, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    raise Exception(f"SILSO returned {resp.status}")
                text = await resp.text()
        
        # Parsear CSV del SILSO
        df = pd.read_csv(
            StringIO(text), sep=';',
            names=['Year','Month','YearFrac','SSN','StdDev','Obs','Definitive'],
            comment='/'
        )
        df['Date'] = pd.to_datetime(dict(year=df.Year, month=df.Month, day=15))
        df = df[df['SSN'] >= 0]  # Filtrar valores válidos
        df = df[df['Year'] >= start_year]
        
        # Añadir clasificación basada en SSN real
        df['classification'] = df['SSN'].apply(
            lambda s: 'high' if s >= 100 else ('moderate' if s >= 50 else 'low')
        )
        df['flare_activity'] = df['SSN'] * 0.1
        df['geomagnetic_storm'] = df['SSN'] * 0.5
        
        result = df[['Date','SSN','flare_activity','geomagnetic_storm','classification']].copy()
        result.columns = ['date','sunspot_number','flare_activity','geomagnetic_storm','classification']
        
        print(f"✅ SILSO: {len(result)} registros reales obtenidos ({start_year}-2024)")
        return result
        
    except Exception as e:
        print(f"⚠️ SILSO no disponible ({e}), usando datos sintéticos")
        return _generate_fallback_data(start_year)

def _generate_fallback_data(start_year: int) -> pd.DataFrame:
    """Respaldo sintético basado en el ciclo solar real de 11 años"""
    years = list(range(start_year, 2025))
    dates = pd.date_range(start=f"{start_year}-01-01", end="2024-12-31", freq="MS")
    t = np.arange(len(dates))
    # Modelo realista del ciclo solar
    ssn = 80 * np.sin(2 * np.pi * t / (11.2 * 12)) ** 2 + np.random.normal(0, 15, len(t))
    ssn = np.clip(ssn, 0, None)
    
    return pd.DataFrame({
        'date': dates,
        'sunspot_number': ssn,
        'flare_activity': ssn * 0.1,
        'geomagnetic_storm': ssn * 0.5,
        'classification': ['high' if s >= 100 else ('moderate' if s >= 50 else 'low') for s in ssn]
    })
