#!/usr/bin/env python3
"""
Sistema avanzado de obtención de datos de actividad solar
Integra múltiples fuentes oficiales: SILSO, NOAA, SWPC
"""
import aiohttp
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import logging
from pathlib import Path
import json
import hashlib
from app.config.settings import settings
from app.models.solar import SolarActivity, SolarCyclePhase, SolarActivityLevel

logger = logging.getLogger(__name__)

class DataFetcherError(Exception):
    """Excepciones específicas del sistema de obtención de datos"""
    pass

class SolarDataFetcher:
    """Fetcher principal para datos de actividad solar"""
    
    def __init__(self):
        self.cache_dir = Path("data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': f'{settings.PROJECT_NAME}/{settings.PROJECT_VERSION}'}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _get_cache_path(self, url: str, params: Dict = None) -> Path:
        """Genera ruta de cache única basada en URL y parámetros"""
        cache_key = f"{url}_{params or ''}"
        hash_key = hashlib.md5(cache_key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.json"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Verifica si el cache es válido según configuración"""
        if not cache_path.exists():
            return False
        
        cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        max_age = timedelta(hours=settings.CACHE_DURATION_HOURS)
        return cache_age < max_age
    
    async def _fetch_with_cache(self, url: str, params: Dict = None) -> Dict[str, Any]:
        """Obtiene datos con sistema de cache inteligente"""
        cache_path = self._get_cache_path(url, params)
        
        # Verificar cache válido
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    cached_data = json.load(f)
                    logger.info(f"Using cached data for {url}")
                    return cached_data
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
        
        # Fetch fresh data
        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                
                content_type = response.headers.get('content-type', '')
                
                if 'json' in content_type:
                    data = await response.json()
                elif 'csv' in content_type or url.endswith('.csv'):
                    text_data = await response.text()
                    data = {"csv_content": text_data, "format": "csv"}
                else:
                    text_data = await response.text()
                    data = {"text_content": text_data, "format": "text"}
                
                # Cache the data
                try:
                    with open(cache_path, 'w') as f:
                        json.dump(data, f, indent=2, default=str)
                except Exception as e:
                    logger.warning(f"Cache write error: {e}")
                
                logger.info(f"Fetched fresh data from {url}")
                return data
                
        except Exception as e:
            logger.error(f"Error fetching data from {url}: {e}")
            raise DataFetcherError(f"Failed to fetch data from {url}: {e}")

    async def fetch_silso_sunspot_data(self, years_back: int = 15) -> List[SolarActivity]:
        """
        Obtiene datos históricos de manchas solares del SILSO (Royal Observatory Belgium)
        Formato: Year Month SSN StdDev Observations Flag
        """
        try:
            data = await self._fetch_with_cache(settings.SILSO_SUNSPOT_URL)
            csv_content = data.get("csv_content", "")
            
            if not csv_content:
                raise DataFetcherError("No CSV content received from SILSO")
            
            # Procesar datos CSV del SILSO
            lines = csv_content.strip().split('\n')
            solar_activities = []
            cutoff_year = datetime.now().year - years_back
            
            for line in lines:
                if line.startswith('#') or not line.strip():
                    continue
                
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        year = int(parts[0])
                        month = int(parts[1])
                        ssn = float(parts[2])
                        std_dev = float(parts[3]) if parts[3] != '-1' else None
                        
                        # Filtrar por años recientes
                        if year < cutoff_year:
                            continue
                        
                        # Crear fecha del primer día del mes
                        date = datetime(year, month, 1)
                        
                        # Determinar fase del ciclo solar
                        cycle_phase = self._determine_solar_cycle_phase(date, ssn)
                        
                        activity = SolarActivity(
                            date=date,
                            sunspot_number=ssn,
                            cycle_phase=cycle_phase,
                            data_source="SILSO",
                            created_at=datetime.now()
                        )
                        
                        solar_activities.append(activity)
                        
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Error parsing SILSO line '{line}': {e}")
                        continue
            
            logger.info(f"Fetched {len(solar_activities)} SILSO records")
            return solar_activities
            
        except Exception as e:
            logger.error(f"Error fetching SILSO data: {e}")
            raise DataFetcherError(f"SILSO data fetch failed: {e}")

    async def fetch_noaa_solar_indices(self) -> List[SolarActivity]:
        """
        Obtiene índices solares actualizados del NOAA
        """
        try:
            data = await self._fetch_with_cache(settings.NOAA_SOLAR_URL)
            
            if not isinstance(data, list):
                raise DataFetcherError("Unexpected NOAA solar data format")
            
            solar_activities = []
            
            for record in data[-100:]:  # Últimos 100 registros
                try:
                    time_tag = record.get('time_tag')
                    ssn = record.get('ssn')
                    f107 = record.get('f10.7')
                    
                    if not all([time_tag, ssn is not None]):
                        continue
                    
                    date = datetime.fromisoformat(time_tag.replace('Z', '+00:00'))
                    cycle_phase = self._determine_solar_cycle_phase(date, float(ssn))
                    
                    activity = SolarActivity(
                        date=date,
                        sunspot_number=float(ssn),
                        solar_flux_10_7=float(f107) if f107 else None,
                        cycle_phase=cycle_phase,
                        data_source="NOAA_SWPC",
                        created_at=datetime.now()
                    )
                    
                    solar_activities.append(activity)
                    
                except (KeyError, ValueError, TypeError) as e:
                    logger.warning(f"Error parsing NOAA record: {e}")
                    continue
            
            logger.info(f"Fetched {len(solar_activities)} NOAA solar records")
            return solar_activities
            
        except Exception as e:
            logger.error(f"Error fetching NOAA solar data: {e}")
            raise DataFetcherError(f"NOAA solar data fetch failed: {e}")

    async def fetch_geomagnetic_data(self) -> List[Dict[str, Any]]:
        """
        Obtiene datos geomagnéticos actuales del NOAA
        """
        try:
            data = await self._fetch_with_cache(settings.NOAA_GEOMAG_URL)
            
            if not isinstance(data, list):
                raise DataFetcherError("Unexpected geomagnetic data format")
            
            geomag_data = []
            
            for record in data[-50:]:  # Últimos 50 registros
                try:
                    time_tag = record.get('time_tag')
                    kp = record.get('kp')
                    ap = record.get('estimated_ap')
                    
                    if not all([time_tag, kp is not None]):
                        continue
                    
                    date = datetime.fromisoformat(time_tag.replace('Z', '+00:00'))
                    
                    geomag_record = {
                        'date': date,
                        'kp_index': float(kp),
                        'ap_index': float(ap) if ap else None,
                        'data_source': 'NOAA_GEOMAG'
                    }
                    
                    geomag_data.append(geomag_record)
                    
                except (KeyError, ValueError, TypeError) as e:
                    logger.warning(f"Error parsing geomagnetic record: {e}")
                    continue
            
            logger.info(f"Fetched {len(geomag_data)} geomagnetic records")
            return geomag_data
            
        except Exception as e:
            logger.error(f"Error fetching geomagnetic data: {e}")
            raise DataFetcherError(f"Geomagnetic data fetch failed: {e}")

    async def fetch_space_weather_summary(self) -> Dict[str, Any]:
        """
        Obtiene resumen actual del clima espacial
        """
        try:
            data = await self._fetch_with_cache(settings.NOAA_SPACE_WEATHER_URL)
            
            # Procesar resumen de clima espacial
            summary = {
                'timestamp': datetime.now().isoformat(),
                'solar_activity_level': 'unknown',
                'geomagnetic_activity_level': 'unknown',
                'solar_wind_speed': None,
                'current_conditions': {},
                'data_source': 'NOAA_SWPC_SUMMARY'
            }
            
            # Extraer información relevante del resumen
            if isinstance(data, dict):
                summary.update(data)
            elif isinstance(data, list) and data:
                summary.update(data[0])
            
            logger.info("Fetched space weather summary")
            return summary
            
        except Exception as e:
            logger.error(f"Error fetching space weather summary: {e}")
            raise DataFetcherError(f"Space weather summary fetch failed: {e}")

    def _determine_solar_cycle_phase(self, date: datetime, ssn: float) -> SolarCyclePhase:
        """
        Determina la fase del ciclo solar basado en fecha y número de manchas solares
        Algoritmo simplificado basado en datos históricos
        """
        # Ciclos solares conocidos y sus fechas aproximadas de mínimo
        solar_cycle_minima = {
            23: datetime(1996, 5, 1),   # Ciclo 23 mínimo
            24: datetime(2008, 12, 1),  # Ciclo 24 mínimo  
            25: datetime(2019, 12, 1)   # Ciclo 25 mínimo
        }
        
        # Determinar ciclo actual
        current_cycle = 25  # Asumimos ciclo 25 para fechas recientes
        if date < datetime(2008, 12, 1):
            current_cycle = 23
        elif date < datetime(2019, 12, 1):
            current_cycle = 24
        
        if current_cycle in solar_cycle_minima:
            cycle_start = solar_cycle_minima[current_cycle]
            cycle_progress = (date - cycle_start).days / (11.2 * 365.25)
            
            # Determinar fase basado en progreso del ciclo y SSN
            if ssn < 20:
                if cycle_progress < 0.2 or cycle_progress > 0.8:
                    return SolarCyclePhase.MINIMUM
                else:
                    return SolarCyclePhase.DECLINING
            elif ssn < 50:
                if cycle_progress < 0.4:
                    return SolarCyclePhase.ASCENDING
                else:
                    return SolarCyclePhase.DECLINING
            elif ssn < 100:
                if 0.3 < cycle_progress < 0.7:
                    return SolarCyclePhase.MAXIMUM
                elif cycle_progress <= 0.3:
                    return SolarCyclePhase.ASCENDING
                else:
                    return SolarCyclePhase.DECLINING
            else:  # SSN >= 100
                return SolarCyclePhase.MAXIMUM
        
        return SolarCyclePhase.UNKNOWN

    async def fetch_comprehensive_solar_data(self, years_back: int = 5) -> Dict[str, Any]:
        """
        Obtiene datos solares completos de todas las fuentes
        """
        try:
            # Ejecutar todas las consultas en paralelo
            tasks = [
                self.fetch_silso_sunspot_data(years_back),
                self.fetch_noaa_solar_indices(),
                self.fetch_geomagnetic_data(),
                self.fetch_space_weather_summary()
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Procesar resultados
            comprehensive_data = {
                'silso_data': results[0] if not isinstance(results[0], Exception) else [],
                'noaa_solar': results[1] if not isinstance(results[1], Exception) else [],
                'geomagnetic': results[2] if not isinstance(results[2], Exception) else [],
                'space_weather': results[3] if not isinstance(results[3], Exception) else {},
                'fetch_timestamp': datetime.now().isoformat(),
                'errors': []
            }
            
            # Registrar errores
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    source_names = ['SILSO', 'NOAA_Solar', 'Geomagnetic', 'SpaceWeather']
                    error_info = f"{source_names[i]}: {str(result)}"
                    comprehensive_data['errors'].append(error_info)
                    logger.error(f"Error in {source_names[i]}: {result}")
            
            return comprehensive_data
            
        except Exception as e:
            logger.error(f"Error in comprehensive data fetch: {e}")
            raise DataFetcherError(f"Comprehensive data fetch failed: {e}")

# Funciones de utilidad para procesamiento de datos
def merge_solar_datasets(silso_data: List[SolarActivity], 
                        noaa_data: List[SolarActivity]) -> List[SolarActivity]:
    """
    Combina y deduplicita datos de diferentes fuentes
    Prioriza NOAA para datos recientes y SILSO para históricos
    """
    merged = {}
    
    # Agregar datos SILSO (base histórica)
    for activity in silso_data:
        key = activity.date.strftime('%Y-%m')
        merged[key] = activity
    
    # Sobrescribir con datos NOAA más recientes (últimos 2 años)
    cutoff_date = datetime.now() - timedelta(days=730)
    for activity in noaa_data:
        if activity.date >= cutoff_date:
            key = activity.date.strftime('%Y-%m')
            # Combinar información cuando sea posible
            if key in merged:
                existing = merged[key]
                # Mantener datos SILSO como base, añadir datos NOAA
                activity.sunspot_number = existing.sunspot_number
                if not activity.cycle_phase or activity.cycle_phase == SolarCyclePhase.UNKNOWN:
                    activity.cycle_phase = existing.cycle_phase
            merged[key] = activity
    
    # Convertir a lista ordenada
    sorted_activities = sorted(merged.values(), key=lambda x: x.date)
    return sorted_activities

def calculate_solar_statistics(activities: List[SolarActivity]) -> Dict[str, Any]:
    """
    Calcula estadísticas básicas de los datos solares
    """
    if not activities:
        return {"error": "No data available"}
    
    ssn_values = [a.sunspot_number for a in activities if a.sunspot_number is not None]
    
    if not ssn_values:
        return {"error": "No valid sunspot number data"}
    
    return {
        "total_records": len(activities),
        "valid_ssn_records": len(ssn_values),
        "date_range": {
            "start": min(a.date for a in activities).isoformat(),
            "end": max(a.date for a in activities).isoformat()
        },
        "ssn_statistics": {
            "mean": np.mean(ssn_values),
            "median": np.median(ssn_values),
            "std": np.std(ssn_values),
            "min": min(ssn_values),
            "max": max(ssn_values),
            "current": ssn_values[-1] if ssn_values else None
        },
        "cycle_phase_distribution": {
            phase.value: sum(1 for a in activities if a.cycle_phase == phase)
            for phase in SolarCyclePhase
        },
        "activity_level_distribution": {
            level.value: sum(1 for a in activities if a.activity_level == level)
            for level in SolarActivityLevel
        }
    }
