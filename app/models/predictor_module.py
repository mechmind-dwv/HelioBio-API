#!/usr/bin/env python3
"""
Módulo 5: Sistema de Predicción Avanzado - HelioBio-API
Motor de predicción que combina modelos estadísticos, machine learning y
teorías de Chizhevsky para predecir eventos heliobiológicos futuros.

Modelos implementados:
- ARIMA/SARIMA para series temporales
- Redes Neuronales LSTM para patrones complejos  
- Random Forest para relaciones no lineales
- Ensemble methods para robustez
- Modelos de ciclos solares específicos
- Predicción de eventos epidemiológicos

Autor: mechmind-dwv
Email: ia.mechmind@gmail.com
GitHub: https://github.com/mechmind-dwv/HelioBio-API
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import warnings
import logging
import pickle
from pathlib import Path

# Análisis estadístico y series temporales
import scipy.stats as stats
from scipy.optimize import minimize, differential_evolution
from scipy.signal import find_peaks, savgol_filter
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Machine Learning
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline

# Deep Learning (si está disponible TensorFlow/Keras)
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.info("TensorFlow no disponible - modelos LSTM deshabilitados")

warnings.filterwarnings('ignore', category=FutureWarning)
logger = logging.getLogger(__name__)

class PredictionModel(Enum):
    """Tipos de modelos de predicción disponibles"""
    ARIMA = "arima"
    SARIMA = "sarima"
    LSTM = "lstm"
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    ENSEMBLE = "ensemble"
    CHIZHEVSKY_CYCLE = "chizhevsky_cycle"
    HYBRID = "hybrid"

class PredictionHorizon(Enum):
    """Horizontes temporales de predicción"""
    SHORT_TERM = "short_term"      # 1-6 meses
    MEDIUM_TERM = "medium_term"    # 6-24 meses  
    LONG_TERM = "long_term"        # 2-11 años (ciclo solar completo)

@dataclass
class PredictionConfig:
    """Configuración del sistema de predicción"""
    model_type: PredictionModel = PredictionModel.ENSEMBLE
    prediction_horizon_months: int = 24
    confidence_level: float = 0.95
    cross_validation_folds: int = 5
    max_features_rf: int = 10
    lstm_lookback_months: int = 60
    lstm_epochs: int = 100
    lstm_batch_size: int = 32
    ensemble_weights: Dict[str, float] = field(default_factory=lambda: {
        'arima': 0.3,
        'rf': 0.3, 
        'lstm': 0.2,
        'cycle': 0.2
    })
    auto_model_selection: bool = True
    save_models: bool = True
    model_cache_dir: str = "./data/models"

@dataclass 
class PredictionResult:
    """Resultado de predicción"""
    model_type: str
    predictions: List[Dict[str, Any]]
    confidence_intervals: List[Tuple[float, float]]
    model_metrics: Dict[str, float]
    prediction_dates: List[datetime]
    methodology: str
    chizhevsky_assessment: Dict[str, Any]
    uncertainty_analysis: Dict[str, Any]
    recommendations: List[str]
    created_at: datetime = field(default_factory=datetime.now)

class SolarCyclePredictor:
    """Predictor especializado en ciclos solares usando teorías de Chizhevsky"""
    
    def __init__(self):
        self.cycle_length_months = 134  # ~11.2 años
        self.cycle_amplitude_range = (50, 200)  # Rango típico de SSN máximo
        
    def fit_solar_cycle_model(self, solar_data: pd.Series) -> Dict[str, Any]:
        """Ajusta modelo de ciclo solar a datos históricos"""
        
        # Detectar picos y valles para identificar ciclos
        smoothed_data = solar_data.rolling(window=13, center=True).mean()
        peaks, peak_props = find_peaks(smoothed_data.values, height=30, distance=80)
        valleys, valley_props = find_peaks(-smoothed_data.values, height=-30, distance=80)
        
        # Analizar características de ciclos históricos
        cycle_info = {
            'detected_peaks': len(peaks),
            'detected_valleys': len(valleys),
            'peak_dates': [solar_data.index[i].strftime('%Y-%m') for i in peaks],
            'peak_values': [smoothed_data.iloc[i] for i in peaks],
            'cycle_lengths': [],
            'cycle_amplitudes': []
        }
        
        # Calcular longitudes de ciclo
        if len(peaks) > 1:
            for i in range(1, len(peaks)):
                cycle_length = (solar_data.index[peaks[i]] - solar_data.index[peaks[i-1]]).days / 30.44
                cycle_info['cycle_lengths'].append(cycle_length)
        
        # Calcular amplitudes de ciclo (pico - valle previo)
        for peak_idx in peaks:
            previous_valleys = valleys[valleys < peak_idx]
            if len(previous_valleys) > 0:
                valley_idx = previous_valleys[-1]
                amplitude = smoothed_data.iloc[peak_idx] - smoothed_data.iloc[valley_idx]
                cycle_info['cycle_amplitudes'].append(amplitude)
        
        # Estadísticas de ciclos
        if cycle_info['cycle_lengths
