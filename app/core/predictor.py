#!/usr/bin/env python3
"""
Sistema de predicción heliobiológica basado en machine learning
Implementa múltiples modelos predictivos para actividad solar y eventos biológicos
"""
import logging
import pickle
import warnings
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from scipy import signal
from scipy.optimize import curve_fit
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVR

from app.core.chizhevsky_kb import ChizhevskySolarCycles
from app.models.biological import BiologicalEvent
from app.models.solar import (SolarActivity, SolarActivityLevel,
                              SolarCyclePhase, SolarForecast)

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
    feature_importance: Optional[Dict[str, float]]
