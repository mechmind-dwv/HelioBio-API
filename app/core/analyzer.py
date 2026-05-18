#!/usr/bin/env python3
"""
Motor de análisis estadístico avanzado para correlaciones heliobiológicas
Implementa métodos estadísticos robustos y algoritmos de machine learning
"""
import logging
import warnings
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from scipy import stats
from scipy.signal import find_peaks, periodogram
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

from app.core.chizhevsky_kb import get_chizhevsky_knowledge_base
from app.models.biological import BiologicalEvent
from app.models.solar import SolarActivity

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
