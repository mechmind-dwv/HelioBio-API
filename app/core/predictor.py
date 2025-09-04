### app/core/predictor.py
#!/usr/bin/env python3
"""
Sistema de predicción heliobiológica basado en machine learning
Implementa múltiples modelos predictivos para actividad solar y eventos biológicos
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.optimize import curve_fit
from scipy import signal
import warnings
from typing import Dict, Any, List, Tuple, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import logging
import pickle
from pathlib import Path

from app.models.solar import SolarActivity, SolarForecast, SolarCyclePhase, SolarActivityLevel
from app.models.biological import BiologicalEvent
from app.core.chizhevsky_kb import ChizhevskySolarCycles

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore', category=FutureWarning)

class PredictionMethod(str, Enum):
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    SUPPORT_VECTOR = "support_vector"
    LINEAR_REGRESSION = "linear_regression"
    POLYNOMIAL_REGRESSION = "polynomial_regression"
    SINUSOIDAL_MODEL = "sinusoidal_model"
    ENSEMBLE = "ensemble"

class PredictionHorizon(str, Enum):
    SHORT_TERM = "short_term"    # 1-6 meses
    MEDIUM_TERM = "medium_term"  # 6-24 meses
    LONG_TERM = "long_term"      # 2-10 años

@dataclass
class PredictionMetrics:
    """Métricas de calidad de predicción"""
    mae: float  # Mean Absolute Error
    mse: float  # Mean Squared Error
    rmse: float # Root Mean Squared Error
    r2: float   # R-squared
    mape: float # Mean Absolute Percentage Error
    cross_val_score: float
    method_used: PredictionMethod

@dataclass
class SolarPredictionResult:
    """Resultado de predicción solar"""
    predictions: List[SolarForecast]
    metrics: PredictionMetrics
    confidence_bands: Dict[str, List[float]]
    model_parameters: Dict[str, Any]
    feature_importance: Optional[Dict[str, float]]## Módulo 3: Sistema de Obtención de Datos

### app/core/data_fetcher.py
```python
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
```

## Módulo 4: Motor de Análisis Estadístico Avanzado

### app/core/analyzer.py
```python
#!/usr/bin/env python3
"""
Motor de análisis estadístico avanzado para correlaciones heliobiológicas
Implementa métodos estadísticos robustos y algoritmos de machine learning
"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.signal import find_peaks, periodogram
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import warnings
from typing import Dict, Any, List, Tuple, Optional, Union
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from enum import Enum

from app.models.solar import SolarActivity
from app.models.biological import BiologicalEvent
from app.core.chizhevsky_kb import get_chizhevsky_knowledge_base

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore', category=RuntimeWarning)

class CorrelationMethod(str, Enum):
    PEARSON = "pearson"
    SPEARMAN = "spearman"
    KENDALL = "kendall"
    CROSS_CORRELATION = "cross_correlation"
    WAVELET = "wavelet"
    MUTUAL_INFORMATION = "mutual_information"

class CyclePeriodMethod(str, Enum):
    FOURIER = "fourier"
    LOMB_SCARGLE = "lomb_scargle"
    AUTOCORRELATION = "autocorrelation"
    PEAK_DETECTION = "peak_detection"

@dataclass
class CorrelationResult:
    """Resultado de análisis de correlación"""
    method: CorrelationMethod
    correlation_coefficient: float
    p_value: float
    confidence_interval: Tuple[float, float]
    significance_level: float
    sample_size: int
    lag_days: int = 0
    strength_interpretation: str = ""
    statistical_significance: bool = False

@dataclass
class CycleAnalysisResult:
    """Resultado de análisis de ciclos"""
    dominant_period_years: float
    confidence_level: float
    secondary_periods: List[float]
    cycle_strength: float
    method_used: CyclePeriodMethod
    spectral_data: Optional[Dict[str, Any]] = None

@dataclass
class ChizhevskAnalysisResult:
    """Resultado de validación de teorías de Chizhevsky"""
    theory_validation_score: float  # 0-1
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    modern_interpretation: str
    confidence_level: float

class AdvancedHeliobiologicalAnalyzer:
    """Analizador estadístico avanzado para correlaciones heliobiológicas"""
    
    def __init__(self):
        self.kb = get_chizhevsky_knowledge_base()
        self.scaler = StandardScaler()
        
    def prepare_time_series_data(self, 
                               solar_data: List[SolarActivity],
                               biological_events: List[BiologicalEvent] = None,
                               resample_frequency: str = 'M') -> pd.DataFrame:
        """
        Prepara y alinea series temporales para análisis
        """
        try:
            # Convertir datos solares a DataFrame
            solar_records = []
            for activity in solar_data:
                solar_records.append({
                    'date': activity.date,
                    'sunspot_number': activity.sunspot_number,
                    'solar_flux_10_7': activity.solar_flux_10_7,
                    'geomagnetic_ap': activity.geomagnetic_ap,
                    'cycle_phase': activity.cycle_phase.value,
                    'activity_level': activity.activity_level.value
                })
            
            df_solar = pd.DataFrame(solar_records)
            df_solar['date'] = pd.to_datetime(df_solar['date'])
            df_solar.set_index('date', inplace=True)
            
            # Resamplear para frecuencia consistente
            df_resampled = df_solar.resample(resample_frequency).agg({
                'sunspot_number': 'mean',
                'solar_flux_10_7': 'mean',
                'geomagnetic_ap': 'mean',
                'cycle_phase': 'first',
                'activity_level': 'first'
            })
            
            # Agregar eventos biológicos si están disponibles
            if biological_events:
                bio_records = []
                for event in biological_events:
                    # Crear series mensual de eventos (presencia/ausencia)
                    start_date = event.start_date
                    end_date = event.end_date or event.start_date
                    
                    # Generar rango de fechas mensuales para el evento
                    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
                    for date in date_range:
                        bio_records.append({
                            'date': date,
                            'event_active': 1,
                            'event_severity': self._severity_to_numeric(event.severity),
                            'death_count': event.death_count or 0,
                            'case_count': event.case_count or 0
                        })
                
                if bio_records:
                    df_bio = pd.DataFrame(bio_records)
                    df_bio['date'] = pd.to_datetime(df_bio['date'])
                    df_bio.set_index('date', inplace=True)
                    
                    # Resamplear datos biológicos
                    df_bio_resampled = df_bio.resample(resample_frequency).agg({
                        'event_active': 'max',
                        'event_severity': 'max',
                        'death_count': 'sum',
                        'case_count': 'sum'
                    }).fillna(0)
                    
                    # Combinar con datos solares
                    df_resampled = df_resampled.join(df_bio_resampled, how='outer')
            
            # Rellenar valores faltantes
            df_resampled = df_resampled.fillna(method='ffill').fillna(method='bfill')
            
            # Agregar características derivadas
            df_resampled['ssn_smoothed'] = df_resampled['sunspot_number'].rolling(window=12, center=True).mean()
            df_resampled['ssn_trend'] = df_resampled['sunspot_number'].diff()
            df_resampled['ssn_volatility'] = df_resampled['sunspot_number'].rolling(window=12).std()
            
            return df_resampled
            
        except Exception as e:
            logger.error(f"Error preparing time series data: {e}")
            raise
    
    def _severity_to_numeric(self, severity) -> int:
        """Convierte severidad categórica a numérica"""
        severity_map = {'low': 1, 'moderate': 2, 'high': 3, 'critical': 4}
        return severity_map.get(severity.value if hasattr(severity, 'value') else severity, 1)
    
    def calculate_correlation(self,
                           x: pd.Series,
                           y: pd.Series,
                           method: CorrelationMethod = CorrelationMethod.PEARSON,
                           max_lag_days: int = 365,
                           significance_level: float = 0.05) -> CorrelationResult:
        """
        Calcula correlación robusta entre dos series temporales
        """
        try:
            # Filtrar valores válidos
            valid_mask = ~(pd.isna(x) | pd.isna(y))
            x_clean = x[valid_mask]
            y_clean = y[valid_mask]
            
            if len(x_clean) < 10:
                raise ValueError("Insufficient data points for correlation analysis")
            
            # Calcular correlación según método
            if method == CorrelationMethod.PEARSON:
                corr_coef, p_value = stats.pearsonr(x_clean, y_clean)
                
            elif method == CorrelationMethod.SPEARMAN:
                corr_coef, p_value = stats.spearmanr(x_clean, y_clean)
                
            elif method == CorrelationMethod.KENDALL:
                corr_coef, p_value = stats.kendalltau(x_clean, y_clean)
                
            elif method == CorrelationMethod.CROSS_CORRELATION:
                # Cross-correlation con lags
                max_lag = min(max_lag_days, len(x_clean) // 4)
                correlations = []
                
                for lag in range(-max_lag, max_lag + 1):
                    if lag == 0:
                        corr_coef, p_value = stats.pearsonr(x_clean, y_clean)
                    elif lag > 0:
                        x_lagged = x_clean[:-lag]
                        y_current = y_clean[lag:]
                        if len(x_lagged) > 10:
                            corr, _ = stats.pearsonr(x_lagged, y_current)
                            correlations.append((lag, abs(corr)))
                    else:  # lag < 0
                        x_current = x_clean[-lag:]
                        y_lagged = y_clean[:lag]
                        if len(x_current) > 10:
                            corr, _ = stats.pearsonr(x_current, y_lagged)
                            correlations.append((lag, abs(corr)))
                
                # Encontrar mejor lag
                if correlations:
                    best_lag, best_corr = max(correlations, key=lambda x: x[1])
                    
                    # Recalcular con mejor lag
                    if best_lag > 0:
                        x_final = x_clean[:-best_lag]
                        y_final = y_clean[best_lag:]
                    elif best_lag < 0:
                        x_final = x_clean[-best_lag:]
                        y_final = y_clean[:best_lag]
                    else:
                        x_final, y_final = x_clean, y_clean
                    
                    corr_coef, p_value = stats.pearsonr(x_final, y_final)
                    lag_days = best_lag
                else:
                    corr_coef, p_value = stats.pearsonr(x_clean, y_clean)
                    lag_days = 0
            
            else:
                raise ValueError(f"Unsupported correlation method: {method}")
            
            # Calcular intervalo de confianza
            n = len(x_clean)
            if method in [CorrelationMethod.PEARSON, CorrelationMethod.CROSS_CORRELATION]:
                # Fisher's z-transformation para Pearson
                z_r = 0.5 * np.log((1 + corr_coef) / (1 - corr_coef))
                se = 1 / np.sqrt(n - 3)
                z_critical = stats.norm.ppf(1 - significance_level/2)
                z_lower = z_r - z_critical * se
                z_upper = z_r + z_critical * se
                
                ci_lower = (np.exp(2 * z_lower) - 1) / (np.exp(2 * z_lower) + 1)
                ci_upper = (np.exp(2 * z_upper) - 1) / (np.exp(2 * z_upper) + 1)
            else:
                # Bootstrap para otros métodos
                ci_lower, ci_upper = self._bootstrap_correlation_ci(
                    x_clean, y_clean, method, significance_level
                )
            
            # Interpretar fuerza de la correlación
            strength = self._interpret_correlation_strength(abs(corr_coef))
            
            return CorrelationResult(
                method=method,
                correlation_coefficient=corr_
