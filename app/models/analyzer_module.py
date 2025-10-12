#!/usr/bin/env python3
"""
Módulo 4: Motor de Análisis Estadístico Avanzado - HelioBio-API
Implementa análisis matemáticos sofisticados para validar teorías heliobiológicas
de Alexander Chizhevsky usando métodos estadísticos modernos.

Análisis incluidos:
- Correlaciones temporales avanzadas
- Análisis espectral y wavelets
- Detección de regímenes y cambios estructurales
- Causalidad de Granger multivariada
- Bootstrap y validación cruzada
- Análisis de coherencia y sincronización

Autor: mechmind-dwv
Email: ia.mechmind@gmail.com
GitHub: https://github.com/mechmind-dwv/HelioBio-API
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.signal as signal
from scipy.fft import fft, fftfreq
from scipy.interpolate import interp1d
from scipy.optimize import minimize
import statsmodels.api as sm
from statsmodels.tsa.stattools import grangercausalitytests, adfuller, coint
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.regression.rolling import RollingOLS
from statsmodels.stats.diagnostic import acorr_ljungbox

from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LassoCV, RidgeCV

import pywt  # PyWavelets for wavelet analysis
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import seaborn as sns

from typing import Dict, List, Tuple, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import warnings
import logging

# Configurar warnings y logging
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
plt.switch_backend('Agg')  # Backend sin GUI

logger = logging.getLogger(__name__)

class AnalysisMethod(Enum):
    """Métodos de análisis disponibles"""
    PEARSON = "pearson"
    SPEARMAN = "spearman"
    KENDALL = "kendall"
    PARTIAL_CORRELATION = "partial"
    GRANGER_CAUSALITY = "granger"
    CROSS_CORRELATION = "cross_correlation"
    SPECTRAL_COHERENCE = "spectral_coherence"
    WAVELET_COHERENCE = "wavelet_coherence"
    MUTUAL_INFORMATION = "mutual_information"

class TimeScale(Enum):
    """Escalas temporales para análisis"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    CYCLE = "solar_cycle"

@dataclass
class AnalysisConfig:
    """Configuración para análisis estadísticos"""
    significance_level: float = 0.05
    bootstrap_iterations: int = 1000
    max_lag_months: int = 24
    min_overlap_points: int = 50
    window_size_months: int = 60
    wavelet_name: str = 'morlet'
    spectral_method: str = 'welch'
    detrend_method: str = 'linear'

@dataclass
class CorrelationResult:
    """Resultado de análisis de correlación"""
    method: AnalysisMethod
    correlation_coefficient: float
    p_value: float
    confidence_interval: Tuple[float, float]
    sample_size: int
    degrees_of_freedom: int
    effect_size: str
    statistical_significance: bool
    bootstrap_ci: Optional[Tuple[float, float]] = None
    interpretation: str = ""

@dataclass
class SpectralAnalysisResult:
    """Resultado de análisis espectral"""
    dominant_frequencies: List[Tuple[float, float]]  # (frequency, power)
    coherence_spectrum: Optional[Dict[str, np.ndarray]] = None
    phase_spectrum: Optional[Dict[str, np.ndarray]] = None
    cross_spectrum: Optional[Dict[str, np.ndarray]] = None
    wavelet_coherence: Optional[Dict[str, Any]] = None
    solar_cycle_harmonics: List[float] = None

class ChizhevskAnalyzer:
    """Analizador avanzado para correlaciones heliobiológicas"""
    
    def __init__(self, config: AnalysisConfig = None):
        self.config = config or AnalysisConfig()
        self.scaler = RobustScaler()  # Robusto a outliers
        
    def comprehensive_correlation_analysis(self, 
                                         solar_data: pd.DataFrame,
                                         biological_data: pd.DataFrame,
                                         biological_events: List[Dict]) -> Dict[str, Any]:
        """
        Análisis exhaustivo de correlaciones entre actividad solar y eventos biológicos
        """
        logger.info("Starting comprehensive correlation analysis")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'analysis_config': self.config.__dict__,
            'data_summary': {},
            'correlations': {},
            'spectral_analysis': {},
            'temporal_analysis': {},
            'causality_analysis': {},
            'validation_results': {},
            'chizhevsky_assessment': {}
        }
        
        # 1. Preparar y validar datos
        solar_ts, bio_ts, events_ts = self._prepare_time_series(
            solar_data, biological_data, biological_events
        )
        
        results['data_summary'] = {
            'solar_points': len(solar_ts),
            'biological_points': len(bio_ts),
            'events_count': len(biological_events),
            'overlap_period': f"{solar_ts.index[0]} to {solar_ts.index[-1]}",
            'temporal_resolution': self._detect_temporal_resolution(solar_ts)
        }
        
        # 2. Análisis de correlaciones múltiples
        results['correlations'] = self._multiple_correlation_analysis(solar_ts, bio_ts)
        
        # 3. Análisis espectral avanzado
        results['spectral_analysis'] = self._advanced_spectral_analysis(solar_ts, bio_ts)
        
        # 4. Análisis temporal y de desfase
        results['temporal_analysis'] = self._temporal_lag_analysis(solar_ts, bio_ts)
        
        # 5. Análisis de causalidad
        results['causality_analysis'] = self._causality_analysis(solar_ts, bio_ts)
        
        # 6. Validación estadística
        results['validation_results'] = self._statistical_validation(
            solar_ts, bio_ts, results['correlations']
        )
        
        # 7. Evaluación específica de teorías de Chizhevsky
        results['chizhevsky_assessment'] = self._assess_chizhevsky_theories(
            solar_ts, bio_ts, events_ts, results
        )
        
        return results
    
    def _prepare_time_series(self, solar_data: pd.DataFrame, 
                           biological_data: pd.DataFrame,
                           biological_events: List[Dict]) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Prepara y alinea series temporales para análisis"""
        
        # Procesar datos solares
        if 'date' in solar_data.columns:
            solar_data = solar_data.set_index('date')
        
        if 'sunspot_number' in solar_data.columns:
            solar_ts = solar_data['sunspot_number'].copy()
        else:
            raise ValueError("Solar data must contain 'sunspot_number' column")
        
        # Procesar datos biológicos (si están disponibles)
        if not biological_data.empty:
            if 'date' in biological_data.columns:
                biological_data = biological_data.set_index('date')
            bio_ts = biological_data.iloc[:, 0]  # Primera columna numérica
        else:
            # Crear serie de eventos biológicos
            bio_ts = self._create_biological_event_series(biological_events, solar_ts.index)
        
        # Crear serie temporal de eventos
        events_ts = self._create_biological_event_series(biological_events, solar_ts.index)
        
        # Alinear series temporales
        common_index = solar_ts.index.intersection(bio_ts.index)
        if len(common_index) < self.config.min_overlap_points:
            raise ValueError(f"Insufficient overlap: {len(common_index)} points")
        
        solar_ts = solar_ts.reindex(common_index)
        bio_ts = bio_ts.reindex(common_index)
        events_ts = events_ts.reindex(common_index)
        
        # Interpolar valores faltantes
        solar_ts = solar_ts.interpolate(method='linear')
        bio_ts = bio_ts.interpolate(method='linear')
        
        # Remover outliers extremos (> 3 desviaciones estándar)
        solar_ts = self._remove_extreme_outliers(solar_ts)
        bio_ts = self._remove_extreme_outliers(bio_ts)
        
        return solar_ts, bio_ts, events_ts
    
    def _create_biological_event_series(self, events: List[Dict], 
                                      date_index: pd.DatetimeIndex) -> pd.Series:
        """Crea serie temporal de densidad de eventos biológicos"""
        
        event_series = pd.Series(0.0, index=date_index)
        
        for event in events:
            try:
                start_date = pd.Timestamp(event.get('start_date') or event.get('start_year', 2000))
                end_date = pd.Timestamp(event.get('end_date') or event.get('end_year', start_date.year + 1))
                
                # Calcular peso del evento basado en severidad
                weight = 1.0
                if 'death_count' in event and event['death_count']:
                    # Normalizar logarítmicamente
                    weight = np.log10(max(event['death_count'], 1)) / 8  # Escala 0-1
                elif 'case_count' in event and event['case_count']:
                    weight = np.log10(max(event['case_count'], 1)) / 10
                
                # Distribución temporal del evento
                event_mask = (date_index >= start_date) & (date_index <= end_date)
                if event_mask.sum() > 0:
                    # Distribución beta para simular curva epidemiológica
                    duration_months = event_mask.sum()
                    if duration_months > 1:
                        beta_curve = stats.beta.pdf(
                            np.linspace(0, 1, duration_months), 2, 5
                        )
                        beta_curve = beta_curve / beta_curve.sum() * weight
                        event_series.loc[event_mask] += beta_curve
                    else:
                        event_series.loc[event_mask] += weight
                        
            except Exception as e:
                logger.warning(f"Error processing event: {str(e)}")
        
        return event_series
    
    def _remove_extreme_outliers(self, series: pd.Series, z_threshold: float = 3.5) -> pd.Series:
        """Remueve outliers extremos usando modified z-score"""
        median = series.median()
        mad = np.median(np.abs(series - median))
        modified_z_scores = 0.6745 * (series - median) / mad
        
        outlier_mask = np.abs(modified_z_scores) > z_threshold
        if outlier_mask.sum() > 0:
            logger.info(f"Removing {outlier_mask.sum()} extreme outliers")
            series = series.copy()
            series[outlier_mask] = np.nan
            series = series.interpolate()
        
        return series
    
    def _detect_temporal_resolution(self, time_series: pd.Series) -> str:
        """Detecta la resolución temporal de la serie"""
        time_diffs = np.diff(time_series.index)
        median_diff = np.median(time_diffs)
        
        if median_diff <= pd.Timedelta(days=2):
            return "daily"
        elif median_diff <= pd.Timedelta(days=8):
            return "weekly"
        elif median_diff <= pd.Timedelta(days=35):
            return "monthly"
        else:
            return "yearly"
    
    def _multiple_correlation_analysis(self, solar_ts: pd.Series, 
                                     bio_ts: pd.Series) -> Dict[str, CorrelationResult]:
        """Múltiples análisis de correlación"""
        
        correlations = {}
        
        # Correlación de Pearson
        pearson_r, pearson_p = stats.pearsonr(solar_ts, bio_ts)
        correlations['pearson'] = CorrelationResult(
            method=AnalysisMethod.PEARSON,
            correlation_coefficient=pearson_r,
            p_value=pearson_p,
            confidence_interval=self._correlation_confidence_interval(
                pearson_r, len(solar_ts)
            ),
            sample_size=len(solar_ts),
            degrees_of_freedom=len(solar_ts) - 2,
            effect_size=self._interpret_effect_size(pearson_r),
            statistical_significance=pearson_p < self.config.significance_level
        )
        
        # Correlación de Spearman (no paramétrica)
        spearman_r, spearman_p = stats.spearmanr(solar_ts, bio_ts)
        correlations['spearman'] = CorrelationResult(
            method=AnalysisMethod.SPEARMAN,
            correlation_coefficient=spearman_r,
            p_value=spearman_p,
            confidence_interval=self._correlation_confidence_interval(
                spearman_r, len(solar_ts)
            ),
            sample_size=len(solar_ts),
            degrees_of_freedom=len(solar_ts) - 2,
            effect_size=self._interpret_effect_size(spearman_r),
            statistical_significance=spearman_p < self.config.significance_level
        )
        
        # Correlación de Kendall
        kendall_r, kendall_p = stats.kendalltau(solar_ts, bio_ts)
        correlations['kendall'] = CorrelationResult(
            method=AnalysisMethod.KENDALL,
            correlation_coefficient=kendall_r,
            p_value=kendall_p,
            confidence_interval=self._correlation_confidence_interval(
                kendall_r, len(solar_ts)
            ),
            sample_size=len(solar_ts),
            degrees_of_freedom=len(solar_ts) - 2,
            effect_size=self._interpret_effect_size(kendall_r),
            statistical_significance=kendall_p < self.config.significance_level
        )
        
        # Bootstrap confidence intervals
        for method in ['pearson', 'spearman', 'kendall']:
            bootstrap_ci = self._bootstrap_correlation_ci(
                solar_ts.values, bio_ts.values, method
            )
            correlations[method].bootstrap_ci = bootstrap_ci
        
        return correlations
    
    def _correlation_confidence_interval(self, r: float, n: int, 
                                       confidence: float = 0.95) -> Tuple[float, float]:
        """Calcula intervalo de confianza para correlación usando transformación Fisher"""
        z_r = np.arctanh(r)
        se = 1 / np.sqrt(n - 3)
        z_alpha = stats.norm.ppf((1 + confidence) / 2)
        
        z_lower = z_r - z_alpha * se
        z_upper = z_r + z_alpha * se
        
        r_lower = np.tanh(z_lower)
        r_upper = np.tanh(z_upper)
        
        return (r_lower, r_upper)
    
    def _bootstrap_correlation_ci(self, x: np.ndarray, y: np.ndarray, 
                                method: str) -> Tuple[float, float]:
        """Bootstrap confidence interval para correlaciones"""
        
        bootstrap_correlations = []
        n = len(x)
        
        for _ in range(self.config.bootstrap_iterations):
            # Muestreo con reemplazo
            indices = np.random.choice(n, n, replace=True)
            x_boot = x[indices]
            y_boot = y[indices]
            
            # Calcular correlación
            try:
                if method == 'pearson':
                    r, _ = stats.pearsonr(x_boot, y_boot)
                elif method == 'spearman':
                    r, _ = stats.spearmanr(x_boot, y_boot)
                elif method == 'kendall':
                    r, _ = stats.kendalltau(x_boot, y_boot)
                else:
                    r = 0
                
                bootstrap_correlations.append(r)
            except:
                continue
        
        bootstrap_correlations = np.array(bootstrap_correlations)
        lower = np.percentile(bootstrap_correlations, 2.5)
        upper = np.percentile(bootstrap_correlations, 97.5)
        
        return (lower, upper)
    
    def _interpret_effect_size(self, correlation: float) -> str:
        """Interpreta el tamaño del efecto según Cohen"""
        abs_r = abs(correlation)
        
        if abs_r < 0.1:
            return "negligible"
        elif abs_r < 0.3:
            return "small"
        elif abs_r < 0.5:
            return "medium"
        else:
            return "large"
    
    def _advanced_spectral_analysis(self, solar_ts: pd.Series, 
                                  bio_ts: pd.Series) -> Dict[str, Any]:
        """Análisis espectral avanzado incluyendo coherencia y wavelets"""
        
        results = {}
        
        # Preparar datos (interpolación y detrending)
        solar_interp, bio_interp = self._prepare_for_spectral_analysis(solar_ts, bio_ts)
        
        # 1. Análisis de densidad espectral de potencia
        results['power_spectral_density'] = self._power_spectral_analysis(
            solar_interp, bio_interp
        )
        
        # 2. Análisis de coherencia espectral
        results['spectral_coherence'] = self._spectral_coherence_analysis(
            solar_interp, bio_interp
        )
        
        # 3. Análisis de wavelets
        try:
            results['wavelet_analysis'] = self._wavelet_analysis(solar_interp, bio_interp)
        except Exception as e:
            logger.warning(f"Wavelet analysis failed: {str(e)}")
            results['wavelet_analysis'] = {'error': str(e)}
        
        # 4. Detección de armónicos del ciclo solar
        results['solar_harmonics'] = self._detect_solar_harmonics(solar_interp)
        
        return results
    
    def _prepare_for_spectral_analysis(self, solar_ts: pd.Series, 
                                     bio_ts: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        """Prepara datos para análisis espectral"""
        
        # Asegurar muestreo regular
        common_index = solar_ts.index.intersection(bio_ts.index)
        solar_regular = solar_ts.reindex(common_index).interpolate()
        bio_regular = bio_ts.reindex(common_index).interpolate()
        
        # Detrending
        if self.config.detrend_method == 'linear':
            solar_detrend = signal.detrend(solar_regular.values, type='linear')
            bio_detrend = signal.detrend(bio_regular.values, type='linear')
        else:
            solar_detrend = solar_regular.values - solar_regular.rolling(
                window=min(len(solar_regular)//4, 120)
            ).mean().fillna(method='bfill')
            bio_detrend = bio_regular.values - bio_regular.rolling(
                window=min(len(bio_regular)//4, 120)
            ).mean().fillna(method='bfill')
        
        # Windowing para reducir spectral leakage
        window = signal.windows.hann(len(solar_detrend))
        solar_windowed = solar_detrend * window
        bio_windowed = bio_detrend * window
        
        return solar_windowed, bio_windowed
    
    def _power_spectral_analysis(self, solar_data: np.ndarray, 
                               bio_data: np.ndarray) -> Dict[str, Any]:
        """Análisis de densidad espectral de potencia"""
        
        # Calcular PSD usando método de Welch
        if self.config.spectral_method == 'welch':
            f_solar, psd_solar = signal.welch(
                solar_data, nperseg=min(len(solar_data)//4, 256)
            )
            f_bio, psd_bio = signal.welch(
                bio_data, nperseg=min(len(bio_data)//4, 256)
            )
        else:
            f_solar, psd_solar = signal.periodogram(solar_data)
            f_bio, psd_bio = signal.periodogram(bio_data)
        
        # Encontrar frecuencias dominantes
        solar_peaks, _ = signal.find_peaks(psd_solar, height=np.max(psd_solar)*0.1)
        bio_peaks, _ = signal.find_peaks(psd_bio, height=np.max(psd_bio)*0.1)
        
        # Convertir frecuencias a períodos en años (asumiendo datos mensuales)
        def freq_to_period_years(freq):
            if freq > 0:
                return 12 / freq / 12  # meses a años
            return np.inf
        
        solar_dominant_periods = [freq_to_period_years(f_solar[peak]) for peak in solar_peaks[:5]]
        bio_dominant_periods = [freq_to_period_years(f_bio[peak]) for peak in bio_peaks[:5]]
        
        return {
            'solar_frequencies': f_solar.tolist(),
            'solar_psd': psd_solar.tolist(),
            'bio_frequencies': f_bio.tolist(),
            'bio_psd': psd_bio.tolist(),
            'solar_dominant_periods_years': solar_dominant_periods,
            'bio_dominant_periods_years': bio_dominant_periods,
            'solar_peak_frequency': f_solar[np.argmax(psd_solar)],
            'bio_peak_frequency': f_bio[np.argmax(psd_bio)]
        }
    
    def _spectral_coherence_analysis(self, solar_data: np.ndarray, 
                                   bio_data: np.ndarray) -> Dict[str, Any]:
        """Análisis de coherencia espectral entre series"""
        
        try:
            # Calcular coherencia
            f, coherence = signal.coherence(
                solar_data, bio_data, 
                nperseg=min(len(solar_data)//4, 256)
            )
            
            # Calcular espectro cruzado para análisis de fase
            f_cross, cross_spectrum = signal.csd(
                solar_data, bio_data,
                nperseg=min(len(solar_data)//4, 256)
            )
            
            # Calcular fase
            phase = np.angle(cross_spectrum)
            
            # Encontrar frecuencias con alta coherencia
            high_coherence_indices = coherence > 0.5
            significant_frequencies = f[high_coherence_indices]
            significant_coherences = coherence[high_coherence_indices]
            
            return {
                'frequencies': f.tolist(),
                'coherence': coherence.tolist(),
                'phase': phase.tolist(),
                'mean_coherence': float(np.mean(coherence)),
                'max_coherence': float(np.max(coherence)),
                'max_coherence_frequency': float(f[np.argmax(coherence)]),
                'significant_frequencies': significant_frequencies.tolist(),
                'significant_coherences': significant_coherences.tolist(),
                'high_coherence_count': int(np.sum(high_coherence_indices))
            }
        
        except Exception as e:
            logger.error(f"Coherence analysis failed: {str(e)}")
            return {'error': str(e)}
    
    def _wavelet_analysis(self, solar_data: np.ndarray, bio_data: np.ndarray) -> Dict[str, Any]:
        """Análisis de coherencia wavelet"""
        
        # Transformada wavelet continua
        scales = np.arange(1, 128)
        
        # CWT para datos solares
        solar_cwt, freqs_solar = pywt.cwt(solar_data, scales, self.config.wavelet_name)
        bio_cwt, freqs_bio = pywt.cwt(bio_data, scales, self.config.wavelet_name)
        
        # Coherencia wavelet (simplificada)
        cross_wavelet = solar_cwt * np.conj(bio_cwt)
        coherence_magnitude = np.abs(cross_wavelet)
        
        # Promedios por escala
        mean_coherence_by_scale = np.mean(coherence_magnitude, axis=1)
        
        return {
            'scales': scales.tolist(),
            'mean_coherence_by_scale': mean_coherence_by_scale.tolist(),
            'max_coherence_scale': int(scales[np.argmax(mean_coherence_by_scale)]),
            'wavelet_type': self.config.wavelet_name
        }
    
    def _detect_solar_harmonics(self, solar_data: np.ndarray) -> Dict[str, Any]:
        """Detecta armónicos del ciclo solar de 11 años"""
        
        # FFT para detectar periodicidades
        fft_result = np.abs(fft(solar_data))
        freqs = fftfreq(len(solar_data))
        
        # Convertir a períodos en años (asumiendo datos mensuales)
        periods = []
        amplitudes = []
        
        for i, freq in enumerate(freqs[:len(freqs)//2]):
            if freq > 0:
                period_months = 1 / freq
                period_years = period_months / 12
                
                # Buscar armónicos del ciclo de 11 años
                if 5 < period_years < 25:  # Rango de interés
                    periods.append(period_years)
                    amplitudes.append(fft_result[i])
        
        # Ordenar por amplitud
        if periods:
            sorted_indices = np.argsort(amplitudes)[::-1]
            top_periods = [periods[i] for i in sorted_indices[:5]]
            top_amplitudes = [amplitudes[i] for i in sorted_indices[:5]]
        else:
            top_periods = []
            top_amplitudes = []
        
        return {
            'detected_periods_years': top_periods,
            'period_amplitudes': top_amplitudes,
            'closest_to_11_year': min(top_periods, key=lambda x: abs(x - 11)) if top_periods else None
        }
    
    def _temporal_lag_analysis(self, solar_ts: pd.Series, bio_ts: pd.Series) -> Dict[str, Any]:
        """Análisis de desfases temporales usando correlación cruzada"""
        
        # Correlación cruzada con diferentes lags
        max_lag = min(self.config.max_lag_months, len(solar_ts) // 4)
        lags = range(-max_lag, max_lag + 1)
        cross_correlations = []
        
        for lag in lags:
            if lag == 0:
                corr, _ = stats.pearsonr(solar_ts, bio_ts)
            elif lag > 0:
                # Bio retrasa a solar
                if len(solar_ts) > lag and len(bio_ts) > lag:
                    corr, _ = stats.pearsonr(solar_ts[:-lag], bio_ts[lag:])
                else:
                    corr = 0
            else:
                # Solar retrasa a bio
                lag_abs = abs(lag)
                if len(solar_ts) > lag_abs and len(bio_ts) > lag_abs:
                    corr, _ = stats.pearsonr(solar_ts[lag_abs:], bio_ts[:-lag_abs])
                else:
                    corr = 0
            
            cross_correlations.append(corr)
        
        # Encontrar lag óptimo
        max_corr_idx = np.argmax(np.abs(cross_correlations))
        optimal_lag = lags[max_corr_idx]
        max_correlation = cross_correlations[max_corr_idx]
        
        return {
            'lags': list(lags),
            'cross_correlations': cross_correlations,
            'optimal_lag_months': optimal_lag,
            'max_cross_correlation': max_correlation,
            'lag_interpretation': self._interpret_lag(optimal_lag),
            'significant_lags': [
                {'lag': lag, 'correlation': corr} 
                for lag, corr in zip(lags, cross_correlations) 
                if abs(corr) > 0.3
            ]
        }
    
    def _interpret_lag(self, lag_months: int) -> str:
        """Interpreta el significado del desfase temporal"""
        if lag_months == 0:
            return "Eventos biológicos son simultáneos con actividad solar"
        elif lag_months > 0:
            return f"Eventos biológicos tienden a seguir actividad solar por {lag_months} meses"
        else:
            return f"Eventos biológicos tienden a preceder actividad solar por {abs(lag_months)} meses"
    
    def _causality_analysis(self, solar_ts: pd.Series, bio_ts: pd.Series) -> Dict[str, Any]:
        """Análisis de causalidad de Granger y tests relacionados"""
        
        results = {}
        
        # Preparar datos para análisis de causalidad
        try:
            data_df = pd.DataFrame({
                'solar': solar_ts,
                'biological': bio_ts
            }).dropna()
            
            if len(data_df) < 20:
                return {'error': 'Insufficient data for causality analysis'}
            
            # Test de causalidad de Granger
            max_lag = min(12, len(data_df) // 10)
            
            try:
                # Solar -> Biological
                granger_solar_to_bio = grangercausalitytests(
                    data_df[['biological', 'solar']], 
                    maxlag=max_lag, 
                    verbose=False
                )
                
                # Biological -> Solar  
                granger_bio_to_solar = grangercausalitytests(
                    data_df[['solar', 'biological']], 
                    maxlag=max_lag, 
                    verbose=False
                )
                
                # Extraer mejores resultados
                best_lag_s2b = min(granger_solar_to_bio.keys())
                best_lag_b2s = min(granger_bio_to_solar.keys())
                
                results['granger_causality'] = {
                    'solar_to_biological': {
                        'best_lag': best_lag_s2b,
                        'f_statistic': granger_solar_to_bio[best_lag_s2b][0]['ssr_ftest'][0],
                        'p_value': granger_solar_to_bio[best_lag_s2b][0]['ssr_ftest'][1],
                        'significant': granger_solar_to_bio[best_lag_s2b][0]['ssr_ftest'][1] < 0.05
                    },
                    'biological_to_solar': {
                        'best_lag': best_lag_b2s,
                        'f_statistic': granger_bio_to_solar[best_lag_b2s][0]['ssr_ftest'][0],
                        'p_value': granger_bio_to_solar[best_lag_b2s][0]['ssr_ftest'][1],
                        'significant': granger_bio_to_solar[best_lag_b2s][0]['ssr_ftest'][1] < 0.05
                    }
                }
                
            except Exception as e:
                results['granger_causality'] = {'error': f'Granger test failed: {str(e)}'}
            
            # Test de cointegración
            try:
                coint_result = coint(data_df['solar'], data_df['biological'])
                results['cointegration'] = {
                    't_statistic': coint_result[0],
                    'p_value': coint_result[1],
                    'critical_values': dict(zip(['1%', '5%', '10%'], coint_result[2])),
                    'cointegrated': coint_result[1] < 0.05
                }
            except Exception as e:
                results['cointegration'] = {'error': f'Cointegration test failed: {str(e)}'}
                
        except Exception as e:
            results['error'] = f'Causality analysis failed: {str(e)}'
        
        return results
    
    def _statistical_validation(self, solar_ts: pd.Series, bio_ts: pd.Series, 
                              correlations: Dict[str, CorrelationResult]) -> Dict[str, Any]:
        """Validación estadística rigurosa de resultados"""
        
        validation_results = {}
        
        # 1. Test de normalidad
        solar_shapiro = stats.shapiro(solar_ts.values)
        bio_shapiro = stats.shapiro(bio_ts.values)
        
        validation_results['normality_tests'] = {
            'solar_shapiro_statistic': solar_shapiro[0],
            'solar_shapiro_p_value': solar_shapiro[1],
            'solar_normal': solar_shapiro[1] > 0.05,
            'bio_shapiro_statistic': bio_shapiro[0],
            'bio_shapiro_p_value': bio_shapiro[1],
            'bio_normal': bio_shapiro[1] > 0.05
        }
        
        # 2. Test de estacionariedad
        try:
            solar_adf = adfuller(solar_ts.dropna())
            bio_adf = adfuller(bio_ts.dropna())
            
            validation_results['stationarity_tests'] = {
                'solar_adf_statistic': solar_adf[0],
                'solar_adf_p_value': solar_adf[1],
                'solar_stationary': solar_adf[1] < 0.05,
                'bio_adf_statistic': bio_adf[0],
                'bio_adf_p_value': bio_adf[1],
                'bio_stationary': bio_adf[1] < 0.05
            }
        except Exception as e:
            validation_results['stationarity_tests'] = {'error': str(e)}
        
        # 3. Análisis de residuos para correlación principal
        if 'pearson' in correlations:
            try:
                # Regresión lineal simple
                X = sm.add_constant(solar_ts.values)
                model = sm.OLS(bio_ts.values, X).fit()
                residuals = model.resid
                
                # Test de autocorrelación en residuos
                lb_test = acorr_ljungbox(residuals, lags=10, return_df=True)
                
                validation_results['residual_analysis'] = {
                    'ljung_box_statistic': lb_test['lb_stat'].iloc[-1],
                    'ljung_box_p_value': lb_test['lb_pvalue'].iloc[-1],
                    'residuals_independent': lb_test['lb_pvalue'].iloc[-1] > 0.05,
                    'r_squared': model.rsquared,
                    'adjusted_r_squared': model.rsquared_adj
                }
            except Exception as e:
                validation_results['residual_analysis'] = {'error': str(e)}
        
        # 4. Validación cruzada temporal
        validation_results['temporal_validation'] = self._temporal_cross_validation(
            solar_ts, bio_ts
        )
        
        return validation_results
    
    def _temporal_cross_validation(self, solar_ts: pd.Series, 
                                 bio_ts: pd.Series) -> Dict[str, Any]:
        """Validación cruzada temporal para estabilidad de correlaciones"""
        
        tscv = TimeSeriesSplit(n_splits=5)
        correlations_cv = []
        
        for train_idx, test_idx in tscv.split(solar_ts):
            train_solar = solar_ts.iloc[train_idx]
            train_bio = bio_ts.iloc[train_idx]
            
            try:
                corr, _ = stats.pearsonr(train_solar, train_bio)
                correlations_cv.append(corr)
            except:
                continue
        
        if correlations_cv:
            return {
                'cv_correlations': correlations_cv,
                'mean_cv_correlation': np.mean(correlations_cv),
                'std_cv_correlation': np.std(correlations_cv),
                'cv_stability': 'stable' if np.std(correlations_cv) < 0.1 else 'unstable'
            }
        else:
            return {'error': 'Cross-validation failed'}
    
    def _assess_chizhevsky_theories(self, solar_ts: pd.Series, bio_ts: pd.Series,
                                  events_ts: pd.Series, 
                                  analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluación específica de las teorías de Chizhevsky"""
        
        assessment = {
            'overall_assessment': '',
            'theory_validations': {},
            'contradictions': [],
            'modern_refinements': []
        }
        
        # 1. Evaluación de correlación solar-biológica fundamental
        main_correlation = analysis_results['correlations'].get('pearson', None)
        if main_correlation:
            if main_correlation.statistical_significance and abs(main_correlation.correlation_coefficient) > 0.3:
                assessment['theory_validations']['fundamental_correlation'] = {
                    'supported': True,
                    'strength': main_correlation.effect_size,
                    'evidence': f"Correlación significativa r={main_correlation.correlation_coefficient:.3f}, p={main_correlation.p_value:.4f}"
                }
            else:
                assessment['theory_validations']['fundamental_correlation'] = {
                    'supported': False,
                    'evidence': "Correlación no significativa o muy débil"
                }
        
        # 2. Evaluación del ciclo de 11 años
        spectral_results = analysis_results.get('spectral_analysis', {})
        harmonics = spectral_results.get('solar_harmonics', {})
        
        if harmonics and harmonics.get('closest_to_11_year'):
            closest_period = harmonics['closest_to_11_year']
            if 9 < closest_period < 13:
                assessment['theory_validations']['11_year_cycle'] = {
                    'supported': True,
                    'detected_period': closest_period,
                    'evidence': f"Período dominante detectado: {closest_period:.1f} años"
                }
            else:
                assessment['contradictions'].append(
                    f"Período dominante ({closest_period:.1f} años) difiere significativamente de 11 años"
                )
        
        # 3. Evaluación de causalidad solar -> biológica
        causality = analysis_results.get('causality_analysis', {})
        granger = causality.get('granger_causality', {})
        
        if granger and 'solar_to_biological' in granger:
            s2b = granger['solar_to_biological']
            if s2b.get('significant', False):
                assessment['theory_validations']['solar_causality'] = {
                    'supported': True,
                    'lag_months': s2b.get('best_lag', 0),
                    'evidence': f"Causalidad Granger significativa (p={s2b.get('p_value', 1):.4f})"
                }
            else:
                assessment['contradictions'].append("No se detectó causalidad solar -> biológica")
        
        # 4. Análisis de desfases temporales (teoría de Chizhevsky sugiere efectos inmediatos a corto plazo)
        temporal = analysis_results.get('temporal_analysis', {})
        optimal_lag = temporal.get('optimal_lag_months', 0)
        
        if abs(optimal_lag) <= 3:
            assessment['theory_validations']['temporal_proximity'] = {
                'supported': True,
                'optimal_lag': optimal_lag,
                'evidence': "Efectos biológicos ocurren cerca de actividad solar"
            }
        else:
            assessment['modern_refinements'].append(
                f"Desfase óptimo de {optimal_lag} meses sugiere mecanismos más complejos"
            )
        
        # 5. Evaluación de la fuerza de correlación en diferentes fases del ciclo solar
        cycle_phase_analysis = self._analyze_by_solar_cycle_phase(solar_ts, bio_ts)
        assessment['cycle_phase_analysis'] = cycle_phase_analysis
        
        # Resumen general
        supported_theories = len([v for v in assessment['theory_validations'].values() if v.get('supported')])
        total_theories = len(assessment['theory_validations'])
        
        if supported_theories == 0:
            assessment['overall_assessment'] = "Las teorías de Chizhevsky no reciben apoyo estadístico significativo en estos datos"
        elif supported_theories == total_theories:
            assessment['overall_assessment'] = "Las teorías fundamentales de Chizhevsky reciben fuerte apoyo estadístico"
        else:
            assessment['overall_assessment'] = f"Apoyo parcial a las teorías de Chizhevsky ({supported_theories}/{total_theories} validaciones)"
        
        return assessment
    
    def _analyze_by_solar_cycle_phase(self, solar_ts: pd.Series, 
                                    bio_ts: pd.Series) -> Dict[str, Any]:
        """Analiza correlaciones por fase del ciclo solar"""
        
        # Determinar fases basadas en nivel de actividad solar
        solar_values = solar_ts.values
        
        # Definir umbrales para fases
        low_threshold = np.percentile(solar_values, 25)
        high_threshold = np.percentile(solar_values, 75)
        
        minimum_mask = solar_values <= low_threshold
        maximum_mask = solar_values >= high_threshold
        intermediate_mask = (solar_values > low_threshold) & (solar_values < high_threshold)
        
        phase_correlations = {}
        
        for phase_name, mask in [('minimum', minimum_mask), 
                               ('maximum', maximum_mask),
                               ('intermediate', intermediate_mask)]:
            if np.sum(mask) > 10:  # Suficientes puntos
                try:
                    phase_solar = solar_ts.values[mask]
                    phase_bio = bio_ts.values[mask]
                    corr, p_val = stats.pearsonr(phase_solar, phase_bio)
                    
                    phase_correlations[phase_name] = {
                        'correlation': corr,
                        'p_value': p_val,
                        'sample_size': int(np.sum(mask)),
                        'significant': p_val < 0.05
                    }
                except:
                    phase_correlations[phase_name] = {'error': 'Calculation failed'}
        
        return phase_correlations

# Funciones de utilidad

def create_correlation_report(analysis_results: Dict[str, Any]) -> str:
    """Genera reporte textual de análisis de correlación"""
    
    report = []
    report.append("REPORTE DE ANÁLISIS HELIOBIOLÓGICO")
    report.append("="*50)
    report.append(f"Fecha de análisis: {analysis_results.get('timestamp', 'N/A')}")
    report.append("")
    
    # Resumen de datos
    data_summary = analysis_results.get('data_summary', {})
    report.append("RESUMEN DE DATOS:")
    report.append(f"- Puntos solares: {data_summary.get('solar_points', 'N/A')}")
    report.append(f"- Puntos biológicos: {data_summary.get('biological_points', 'N/A')}")
    report.append(f"- Período: {data_summary.get('overlap_period', 'N/A')}")
    report.append(f"- Resolución: {data_summary.get('temporal_resolution', 'N/A')}")
    report.append("")
    
    # Correlaciones principales
    correlations = analysis_results.get('correlations', {})
    report.append("CORRELACIONES PRINCIPALES:")
    for method, result in correlations.items():
        if isinstance(result, dict) and 'correlation_coefficient' in result:
            report.append(f"- {method.capitalize()}: r={result['correlation_coefficient']:.3f}, "
                        f"p={result['p_value']:.4f}, "
                        f"efecto={result.get('effect_size', 'N/A')}")
    report.append("")
    
    # Evaluación de Chizhevsky
    chizhevsky = analysis_results.get('chizhevsky_assessment', {})
    report.append("EVALUACIÓN DE TEORÍAS DE CHIZHEVSKY:")
    report.append(f"- Evaluación general: {chizhevsky.get('overall_assessment', 'N/A')}")
    
    validations = chizhevsky.get('theory_validations', {})
    for theory, validation in validations.items():
        status = "✓" if validation.get('supported') else "✗"
        report.append(f"- {theory}: {status} {validation.get('evidence', '')}")
    report.append("")
    
    return "\n".join(report)

# Ejemplo de uso para testing
async def test_analyzer():
    """Función de prueba para el analizador"""
    
    # Generar datos sintéticos para prueba
    dates = pd.date_range('2000-01-01', '2023-12-01', freq='M')
    
    # Datos solares sintéticos con ciclo de ~11 años
    solar_cycle = np.sin(2 * np.pi * np.arange(len(dates)) / 132) * 50 + 70  # 132 meses ≈ 11 años
    solar_noise = np.random.normal(0, 20, len(dates))
    solar_data = pd.DataFrame({
        'date': dates,
        'sunspot_number': np.maximum(0, solar_cycle + solar_noise)
    })
    
    # Datos biológicos sintéticos correlacionados
    bio_base = solar_cycle * 0.3 + np.random.normal(0, 10, len(dates))
    bio_data = pd.DataFrame({
        'date': dates,
        'biological_index': bio_base
    })
    
    # Eventos sintéticos
    events = [
        {'start_date': '2003-01-01', 'end_date': '2004-01-01', 'death_count': 1000},
        {'start_date': '2009-01-01', 'end_date': '2010-01-01', 'death_count': 5000},
        {'start_date': '2020-01-01', 'end_date': '2022-01-01', 'death_count': 10000}
    ]
    
    # Crear analizador y ejecutar análisis
    analyzer = ChizhevskAnalyzer()
    
    print("Ejecutando análisis heliobiológico de prueba...")
    results = analyzer.comprehensive_correlation_analysis(
        solar_data, bio_data, events
    )
    
    # Generar reporte
    report = create_correlation_report(results)
    print("\n" + report)
    
    return results

if __name__ == "__main__":
    import asyncio
    
    print("HelioBio-API Advanced Statistical Analyzer")
    print("Autor: mechmind-dwv (ia.mechmind@gmail.com)")
    print("GitHub: https://github.com/mechmind-dwv/HelioBio-API")
    print("="*60)
    
    # Ejecutar test
    asyncio.run(test_analyzer())
