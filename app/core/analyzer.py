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
                'geomagnetic_ap': 'mean'
            })
            
            # Agregar eventos biológicos si están disponibles
            if biological_events:
                bio_records = []
                for event in biological_events:
                    start_date = event.start_date
                    end_date = event.end_date or event.start_date
                    
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
                    
                    df_bio_resampled = df_bio.resample(resample_frequency).agg({
                        'event_active': 'max',
                        'event_severity': 'max',
                        'death_count': 'sum',
                        'case_count': 'sum'
                    }).fillna(0)
                    
                    df_resampled = df_resampled.join(df_bio_resampled, how='outer')
            
            df_resampled = df_resampled.fillna(method='ffill').fillna(method='bfill')
            
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
            valid_mask = ~(pd.isna(x) | pd.isna(y))
            x_clean = x[valid_mask]
            y_clean = y[valid_mask]
            
            if len(x_clean) < 10:
                raise ValueError("Insufficient data points for correlation analysis")
            
            lag_days = 0
            
            if method == CorrelationMethod.PEARSON:
                corr_coef, p_value = stats.pearsonr(x_clean, y_clean)
                
            elif method == CorrelationMethod.SPEARMAN:
                corr_coef, p_value = stats.spearmanr(x_clean, y_clean)
                
            elif method == CorrelationMethod.KENDALL:
                corr_coef, p_value = stats.kendalltau(x_clean, y_clean)
                
            elif method == CorrelationMethod.CROSS_CORRELATION:
                max_lag = min(max_lag_days, len(x_clean) // 4)
                correlations = []
                
                for lag in range(-max_lag, max_lag + 1):
                    if lag == 0:
                        corr, p_val = stats.pearsonr(x_clean, y_clean)
                        correlations.append((lag, abs(corr)))
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
                
                if correlations:
                    best_lag, best_corr = max(correlations, key=lambda x: x[1])
                    
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
            
            n = len(x_clean)
            if method in [CorrelationMethod.PEARSON, CorrelationMethod.CROSS_CORRELATION]:
                if abs(corr_coef) == 1.0: # Evitar singularidad en la z-transformación
                    ci_lower, ci_upper = corr_coef, corr_coef
                else:
                    z_r = 0.5 * np.log((1 + corr_coef) / (1 - corr_coef))
                    se = 1 / np.sqrt(n - 3)
                    z_critical = stats.norm.ppf(1 - significance_level/2)
                    z_lower = z_r - z_critical * se
                    z_upper = z_r + z_critical * se
                    
                    ci_lower = (np.exp(2 * z_lower) - 1) / (np.exp(2 * z_lower) + 1)
                    ci_upper = (np.exp(2 * z_upper) - 1) / (np.exp(2 * z_upper) + 1)
            else:
                ci_lower, ci_upper = self._bootstrap_correlation_ci(
                    x_clean, y_clean, method, significance_level
                )
            
            strength = self._interpret_correlation_strength(abs(corr_coef))
            
            return CorrelationResult(
                method=method,
                correlation_coefficient=corr_coef,
                p_value=p_value,
                confidence_interval=(ci_lower, ci_upper),
                significance_level=significance_level,
                sample_size=n,
                lag_days=lag_days,
                strength_interpretation=strength,
                statistical_significance=p_value < significance_level
            )
            
        except Exception as e:
            logger.error(f"Correlation analysis failed: {e}")
            raise

    def _interpret_correlation_strength(self, r: float) -> str:
        """Interpreta la fuerza de la correlación de acuerdo a la magnitud de r."""
        if r >= 0.9: return "muy fuerte"
        if r >= 0.7: return "fuerte"
        if r >= 0.5: return "moderada"
        if r >= 0.3: return "débil"
        return "muy débil o nula"

    def _bootstrap_correlation_ci(self, x, y, method, significance_level, n_bootstrap=1000):
        """Calcula el intervalo de confianza con bootstrap para métodos no paramétricos."""
        correlations = []
        n = len(x)
        for _ in range(n_bootstrap):
            indices = np.random.choice(n, n, replace=True)
            x_sample = x.iloc[indices]
            y_sample = y.iloc[indices]
            if method == CorrelationMethod.SPEARMAN:
                corr, _ = stats.spearmanr(x_sample, y_sample)
            elif method == CorrelationMethod.KENDALL:
                corr, _ = stats.kendalltau(x_sample, y_sample)
            correlations.append(corr)
        
        correlations.sort()
        alpha = significance_level / 2
        lower_bound = correlations[int(n_bootstrap * alpha)]
        upper_bound = correlations[int(n_bootstrap * (1 - alpha))]
        return lower_bound, upper_bound

    def analyze_cycle_periodicity(self, data: pd.Series, method: CyclePeriodMethod = CyclePeriodMethod.FOURIER) -> CycleAnalysisResult:
        """Analiza la periodicidad dominante en una serie temporal."""
        try:
            if method == CyclePeriodMethod.FOURIER:
                f, Pxx = periodogram(data.dropna(), fs=1.0)
                peaks, _ = find_peaks(Pxx)
                
                if not peaks.any():
                    return CycleAnalysisResult(dominant_period_years=0, confidence_level=0, secondary_periods=[], cycle_strength=0, method_used=method)

                dominant_peak_idx = peaks[np.argmax(Pxx[peaks])]
                dominant_frequency = f[dominant_peak_idx]
                dominant_period = 1.0 / dominant_frequency if dominant_frequency > 0 else 0
                
                # Convertir período a años (si los datos son mensuales)
                dominant_period_years = dominant_period / 12.0
                
                secondary_periods = []
                sorted_peaks = peaks[np.argsort(Pxx[peaks])][::-1]
                for peak_idx in sorted_peaks[1:4]: # Top 3 secondary peaks
                    freq = f[peak_idx]
                    if freq > 0:
                        secondary_periods.append(1.0 / freq / 12.0)

                # Fuerza del ciclo (ratio del pico dominante sobre el total)
                cycle_strength = Pxx[dominant_peak_idx] / np.sum(Pxx) if np.sum(Pxx) > 0 else 0

                spectral_data = {
                    'frequencies': f.tolist(),
                    'power_spectrum': Pxx.tolist()
                }

                return CycleAnalysisResult(
                    dominant_period_years=dominant_period_years,
                    confidence_level=0.95,
                    secondary_periods=[round(p, 2) for p in secondary_periods],
                    cycle_strength=cycle_strength,
                    method_used=method,
                    spectral_data=spectral_data
                )

            else:
                raise ValueError(f"Unsupported cycle period method: {method}")

        except Exception as e:
            logger.error(f"Cycle periodicity analysis failed: {e}")
            raise
