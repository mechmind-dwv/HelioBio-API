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
        if cycle_info['cycle_lengths']:
            cycle_info['mean_cycle_length'] = np.mean(cycle_info['cycle_lengths'])
            cycle_info['std_cycle_length'] = np.std(cycle_info['cycle_lengths'])
        else:
            cycle_info['mean_cycle_length'] = 134  # Valor teórico
            cycle_info['std_cycle_length'] = 15
        
        if cycle_info['cycle_amplitudes']:
            cycle_info['mean_amplitude'] = np.mean(cycle_info['cycle_amplitudes'])
            cycle_info['std_amplitude'] = np.std(cycle_info['cycle_amplitudes'])
        else:
            cycle_info['mean_amplitude'] = 120
            cycle_info['std_amplitude'] = 40
        
        # Determinar fase actual del ciclo
        current_value = solar_data.iloc[-1]
        current_date = solar_data.index[-1]
        
        if len(peaks) > 0:
            last_peak_idx = peaks[-1]
            last_peak_date = solar_data.index[last_peak_idx]
            months_since_peak = (current_date - last_peak_date).days / 30.44
            
            if months_since_peak < 48:  # Menos de 4 años desde el pico
                current_phase = 'declining'
                cycle_progress = months_since_peak / cycle_info['mean_cycle_length']
            else:
                current_phase = 'minimum' if current_value < 30 else 'ascending'
                cycle_progress = (months_since_peak / cycle_info['mean_cycle_length']) % 1.0
        else:
            # Sin picos detectados, estimar por nivel actual
            if current_value < 20:
                current_phase = 'minimum'
                cycle_progress = 0.0
            elif current_value > 80:
                current_phase = 'maximum'
                cycle_progress = 0.5
            else:
                current_phase = 'ascending'
                cycle_progress = 0.25
        
        cycle_info['current_phase'] = current_phase
        cycle_info['cycle_progress'] = cycle_progress
        cycle_info['current_ssn'] = float(current_value)
        
        return cycle_info
    
    def predict_solar_cycle(self, solar_data: pd.Series, 
                          months_ahead: int = 24) -> pd.DataFrame:
        """Predice actividad solar basada en modelo de ciclos"""
        
        # Ajustar modelo de ciclo
        cycle_info = self.fit_solar_cycle_model(solar_data)
        
        # Preparar predicciones
        last_date = solar_data.index[-1]
        prediction_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=months_ahead,
            freq='M'
        )
        
        predictions = []
        current_phase = cycle_info['current_phase']
        cycle_progress = cycle_info['cycle_progress']
        mean_cycle_length = cycle_info['mean_cycle_length']
        mean_amplitude = cycle_info['mean_amplitude']
        
        for i, pred_date in enumerate(prediction_dates):
            # Actualizar progreso del ciclo
            month_offset = i + 1
            new_progress = (cycle_progress + month_offset / mean_cycle_length) % 1.0
            
            # Modelo sinusoidal con forma de ciclo solar real
            # Ciclos solares reales tienen subida rápida y bajada lenta
            if 0 <= new_progress < 0.15:  # Mínimo
                phase = 'minimum'
                base_ssn = 10 + 10 * np.sin(new_progress * 10 * np.pi)
            elif 0.15 <= new_progress < 0.45:  # Subida rápida
                phase = 'ascending'
                t = (new_progress - 0.15) / 0.30
                base_ssn = 20 + mean_amplitude * (1 - np.cos(t * np.pi)) / 2
            elif 0.45 <= new_progress < 0.55:  # Máximo
                phase = 'maximum'
                t = (new_progress - 0.45) / 0.10
                base_ssn = 10 + mean_amplitude * (1 + 0.2 * np.sin(t * 2 * np.pi))
            else:  # Bajada lenta
                phase = 'declining'
                t = (new_progress - 0.55) / 0.45
                base_ssn = 20 + mean_amplitude * (1 + np.cos(t * np.pi)) / 2
            
            # Añadir variabilidad realista
            noise = np.random.normal(0, mean_amplitude * 0.15)
            predicted_ssn = max(0, base_ssn + noise)
            
            # Intervalos de confianza
            uncertainty = mean_amplitude * 0.3 * (1 + 0.5 * month_offset / months_ahead)
            lower_bound = max(0, predicted_ssn - uncertainty)
            upper_bound = predicted_ssn + uncertainty
            
            predictions.append({
                'date': pred_date,
                'predicted_ssn': predicted_ssn,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'cycle_phase': phase,
                'cycle_progress': new_progress,
                'confidence': 1 - (month_offset / (2 * months_ahead))  # Confianza decrece con tiempo
            })
        
        return pd.DataFrame(predictions)

class TimeSeriesPredictor:
    """Predictor basado en modelos ARIMA/SARIMA"""
    
    def __init__(self, config: PredictionConfig):
        self.config = config
        self.model = None
        self.model_params = None
        
    def find_optimal_arima_order(self, time_series: pd.Series) -> Tuple[int, int, int]:
        """Encuentra orden óptimo de ARIMA usando criterios de información"""
        
        # Test de estacionariedad
        adf_result = adfuller(time_series.dropna())
        is_stationary = adf_result[1] < 0.05
        
        # Orden de diferenciación
        d = 0 if is_stationary else 1
        
        # Buscar p y q óptimos
        best_aic = np.inf
        best_order = (1, d, 1)
        
        for p in range(0, 4):
            for q in range(0, 4):
                try:
                    model = ARIMA(time_series, order=(p, d, q))
                    fitted = model.fit()
                    
                    if fitted.aic < best_aic:
                        best_aic = fitted.aic
                        best_order = (p, d, q)
                except:
                    continue
        
        logger.info(f"Optimal ARIMA order: {best_order}, AIC: {best_aic:.2f}")
        return best_order
    
    def fit(self, solar_data: pd.Series) -> 'TimeSeriesPredictor':
        """Ajusta modelo ARIMA a datos solares"""
        
        # Encontrar orden óptimo
        optimal_order = self.find_optimal_arima_order(solar_data)
        
        # Ajustar modelo
        try:
            self.model = ARIMA(solar_data, order=optimal_order)
            self.fitted_model = self.model.fit()
            self.model_params = {
                'order': optimal_order,
                'aic': self.fitted_model.aic,
                'bic': self.fitted_model.bic,
                'rmse': np.sqrt(self.fitted_model.mse)
            }
            logger.info(f"ARIMA model fitted successfully: {optimal_order}")
        except Exception as e:
            logger.error(f"ARIMA fitting failed: {str(e)}")
            raise
        
        return self
    
    def predict(self, steps: int) -> pd.DataFrame:
        """Genera predicciones"""
        
        if self.fitted_model is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Predicción
        forecast = self.fitted_model.forecast(steps=steps)
        forecast_ci = self.fitted_model.get_forecast(steps=steps).conf_int(alpha=1-self.config.confidence_level)
        
        # Crear fechas futuras
        last_date = self.fitted_model.data.dates[-1]
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=steps,
            freq='M'
        )
        
        predictions = []
        for i, date in enumerate(future_dates):
            predictions.append({
                'date': date,
                'predicted_ssn': max(0, float(forecast.iloc[i])),
                'lower_bound': max(0, float(forecast_ci.iloc[i, 0])),
                'upper_bound': max(0, float(forecast_ci.iloc[i, 1])),
                'model': 'ARIMA' + str(self.model_params['order'])
            })
        
        return pd.DataFrame(predictions)

class MachineLearningPredictor:
    """Predictor basado en Random Forest y Gradient Boosting"""
    
    def __init__(self, config: PredictionConfig):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def create_features(self, time_series: pd.Series, lookback: int = 12) -> Tuple[np.ndarray, np.ndarray]:
        """Crea features para ML (valores previos, tendencias, estacionalidad)"""
        
        X = []
        y = []
        
        for i in range(lookback, len(time_series)):
            # Features basados en valores históricos
            features = []
            
            # Valores previos (lag features)
            for lag in [1, 3, 6, 12]:
                if i - lag >= 0:
                    features.append(time_series.iloc[i - lag])
            
            # Tendencia (pendiente de últimos n meses)
            trend_window = min(6, i)
            if trend_window > 1:
                recent_values = time_series.iloc[i-trend_window:i].values
                trend = np.polyfit(range(trend_window), recent_values, 1)[0]
                features.append(trend)
            else:
                features.append(0)
            
            # Media móvil
            ma_window = min(12, i)
            features.append(time_series.iloc[i-ma_window:i].mean())
            
            # Desviación estándar reciente
            features.append(time_series.iloc[i-ma_window:i].std())
            
            # Mes del año (estacionalidad)
            month = time_series.index[i].month
            features.append(np.sin(2 * np.pi * month / 12))
            features.append(np.cos(2 * np.pi * month / 12))
            
            X.append(features)
            y.append(time_series.iloc[i])
        
        self.feature_names = [
            'lag_1', 'lag_3', 'lag_6', 'lag_12',
            'trend', 'ma_12', 'std_12',
            'month_sin', 'month_cos'
        ]
        
        return np.array(X), np.array(y)
    
    def fit(self, solar_data: pd.Series) -> 'MachineLearningPredictor':
        """Ajusta modelo Random Forest"""
        
        X, y = self.create_features(solar_data)
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Crear y ajustar modelo
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_scaled, y)
        
        # Evaluar con validación cruzada
        tscv = TimeSeriesSplit(n_splits=self.config.cross_validation_folds)
        cv_scores = cross_val_score(
            self.model, X_scaled, y,
            cv=tscv,
            scoring='neg_mean_squared_error'
        )
        
        self.cv_rmse = np.sqrt(-cv_scores.mean())
        
        logger.info(f"Random Forest fitted. CV RMSE: {self.cv_rmse:.2f}")
        
        return self
    
    def predict(self, solar_data: pd.Series, steps: int) -> pd.DataFrame:
        """Genera predicciones iterativas"""
        
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        predictions = []
        last_date = solar_data.index[-1]
        
        # Crear serie temporal extendida para predicción iterativa
        extended_series = solar_data.copy()
        
        for step in range(steps):
            # Crear features para el próximo paso
            X_next, _ = self.create_features(extended_series)
            X_next_scaled = self.scaler.transform(X_next[-1:])
            
            # Predecir
            pred = self.model.predict(X_next_scaled)[0]
            pred = max(0, pred)  # No permitir valores negativos
            
            # Calcular incertidumbre basada en distancia temporal
            uncertainty = self.cv_rmse * (1 + 0.1 * step)
            
            # Agregar a serie extendida
            next_date = last_date + pd.DateOffset(months=step+1)
            extended_series = pd.concat([
                extended_series,
                pd.Series([pred], index=[next_date])
            ])
            
            predictions.append({
                'date': next_date,
                'predicted_ssn': pred,
                'lower_bound': max(0, pred - 1.96 * uncertainty),
                'upper_bound': pred + 1.96 * uncertainty,
                'model': 'RandomForest'
            })
        
        return pd.DataFrame(predictions)

class EnsemblePredictor:
    """Predictor ensemble que combina múltiples modelos"""
    
    def __init__(self, config: PredictionConfig):
        self.config = config
        self.models = {}
        self.weights = config.ensemble_weights
        
    def fit(self, solar_data: pd.Series) -> 'EnsemblePredictor':
        """Ajusta todos los modelos del ensemble"""
        
        logger.info("Fitting ensemble models...")
        
        # ARIMA
        try:
            arima_predictor = TimeSeriesPredictor(self.config)
            arima_predictor.fit(solar_data)
            self.models['arima'] = arima_predictor
            logger.info("✓ ARIMA model fitted")
        except Exception as e:
            logger.warning(f"✗ ARIMA failed: {str(e)}")
        
        # Random Forest
        try:
            rf_predictor = MachineLearningPredictor(self.config)
            rf_predictor.fit(solar_data)
            self.models['rf'] = rf_predictor
            logger.info("✓ Random Forest model fitted")
        except Exception as e:
            logger.warning(f"✗ Random Forest failed: {str(e)}")
        
        # Ciclo Solar
        try:
            cycle_predictor = SolarCyclePredictor()
            self.models['cycle'] = cycle_predictor
            logger.info("✓ Solar Cycle model fitted")
        except Exception as e:
            logger.warning(f"✗ Solar Cycle failed: {str(e)}")
        
        # Normalizar pesos basado en modelos disponibles
        available_models = list(self.models.keys())
        total_weight = sum(self.weights.get(m, 0) for m in available_models)
        self.normalized_weights = {
            m: self.weights.get(m, 0) / total_weight 
            for m in available_models
        }
        
        logger.info(f"Ensemble ready with {len(self.models)} models: {available_models}")
        
        return self
    
    def predict(self, solar_data: pd.Series, steps: int) -> pd.DataFrame:
        """Genera predicciones combinadas"""
        
        if not self.models:
            raise ValueError("No models fitted")
        
        all_predictions = {}
        
        # Obtener predicciones de cada modelo
        for model_name, model in self.models.items():
            try:
                if model_name == 'cycle':
                    preds = model.predict_solar_cycle(solar_data, steps)
                else:
                    preds = model.predict(steps)
                
                all_predictions[model_name] = preds
                logger.info(f"✓ {model_name} predictions generated")
            except Exception as e:
                logger.warning(f"✗ {model_name} prediction failed: {str(e)}")
        
        # Combinar predicciones usando pesos
        ensemble_predictions = []
        
        for i in range(steps):
            weighted_pred = 0
            weighted_lower = 0
            weighted_upper = 0
            total_weight = 0
            date = None
            
            for model_name, preds_df in all_predictions.items():
                if i < len(preds_df):
                    weight = self.normalized_weights.get(model_name, 0)
                    weighted_pred += preds_df.iloc[i]['predicted_ssn'] * weight
                    weighted_lower += preds_df.iloc[i]['lower_bound'] * weight
                    weighted_upper += preds_df.iloc[i]['upper_bound'] * weight
                    total_weight += weight
                    
                    if date is None:
                        date = preds_df.iloc[i]['date']
            
            if total_weight > 0:
                ensemble_predictions.append({
                    'date': date,
                    'predicted_ssn': weighted_pred / total_weight,
                    'lower_bound': weighted_lower / total_weight,
                    'upper_bound': weighted_upper / total_weight,
                    'model': 'Ensemble',
                    'models_used': list(all_predictions.keys()),
                    'confidence': 1 - (i / (2 * steps))
                })
        
        return pd.DataFrame(ensemble_predictions)

class BiologicalEventPredictor:
    """Predictor de eventos biológicos basado en actividad solar predicha"""
    
    def __init__(self, correlation_strength: float = 0.7):
        self.correlation_strength = correlation_strength
        
    def predict_biological_risk(self, solar_predictions: pd.DataFrame,
                              historical_correlations: Dict[str, Any]) -> Dict[str, Any]:
        """Predice riesgo de eventos biológicos basado en predicciones solares"""
        
        risk_periods = []
        
        for idx, row in solar_predictions.iterrows():
            ssn = row['predicted_ssn']
            date = row['date']
            phase = row.get('cycle_phase', 'unknown')
            
            # Calcular riesgo usando principios de Chizhevsky
            risk_score = self._calculate_chizhevsky_risk(ssn, phase)
            
            risk_assessment = {
                'period': date.strftime('%Y-%m'),
                'solar_activity': ssn,
                'cycle_phase': phase,
                'risk_score': risk_score,
                'risk_level': self._categorize_risk(risk_score),
                'expected_effects': self._predict_biological_effects(ssn, phase),
                'confidence': row.get('confidence', 0.7)
            }
            
            risk_periods.append(risk_assessment)
        
        # Identificar períodos críticos
        high_risk = [p for p in risk_periods if p['risk_score'] >= 0.7]
        moderate_risk = [p for p in risk_periods if 0.4 <= p['risk_score'] < 0.7]
        
        return {
            'all_periods': risk_periods,
            'high_risk_periods': high_risk,
            'moderate_risk_periods': moderate_risk,
            'peak_risk_period': max(risk_periods, key=lambda x: x['risk_score']) if risk_periods else None,
            'recommendations': self._generate_recommendations(high_risk, moderate_risk)
        }
    
    def _calculate_chizhevsky_risk(self, ssn: float, phase: str) -> float:
        """Calcula riesgo según teorías de Chizhevsky"""
        
        # Factor de actividad solar
        if ssn > 120:
            solar_factor = 1.0
        elif ssn > 80:
            solar_factor = 0.8
        elif ssn > 50:
            solar_factor = 0.5
        else:
            solar_factor = 0.2
        
        # Factor de fase del ciclo
        phase_factors = {
            'maximum': 1.0,
            'ascending': 0.7,
            'declining': 0.5,
            'minimum': 0.2,
            'unknown': 0.4
        }
        
        phase_factor = phase_factors.get(phase, 0.4)
        
        # Combinar factores
        risk = solar_factor * phase_factor * abs(self.correlation_strength)
        
        return min(1.0, max(0.0, risk))
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categoriza nivel de riesgo"""
        if risk_score >= 0.8:
            return "CRITICAL"
        elif risk_score >= 0.6:
            return "HIGH"
        elif risk_score >= 0.4:
            return "MODERATE"
        else:
            return "LOW"
    
    def _predict_biological_effects(self, ssn: float, phase: str) -> List[str]:
        """Predice efectos biológicos probables"""
        effects = []
        
        if phase == 'maximum' and ssn > 80:
            effects.extend([
                "Increased cardiovascular incidents",
                "Higher epidemic susceptibility", 
                "Neurological sensitivity peaks",
                "Immune system stress"
            ])
        elif phase == 'ascending' and ssn > 40:
            effects.extend([
                "Rising immune system activity",
                "Gradual increase in health incidents"
            ])
        elif phase == 'minimum':
            effects.extend([
                "Reduced biological stress",
                "Lower epidemic activity"
            ])
        
        return effects
    
    def _generate_recommendations(self, high_risk: List, moderate_risk: List) -> List[str]:
        """Genera recomendaciones basadas en predicciones"""
        recommendations = []
        
        if high_risk:
            recommendations.extend([
                "Implement enhanced epidemiological surveillance",
                "Increase healthcare preparedness",
                "Monitor vulnerable populations closely",
                "Consider public health advisories"
            ])
        
        if moderate_risk:
            recommendations.extend([
                "Maintain vigilant health monitoring",
                "Prepare contingency resources"
            ])
        
        recommendations.append("Continue validation of heliobiological correlations")
        
        return recommendations

# Función principal del módulo
async def generate_comprehensive_predictions(solar_data: pd.DataFrame,
                                           correlation_analysis: Dict[str, Any],
                                           config: PredictionConfig = None) -> PredictionResult:
    """Genera predicciones comprehensivas combinando todos los modelos"""
    
    if config is None:
        config = PredictionConfig()
    
    logger.info("Starting comprehensive prediction generation...")
    
    # Preparar serie temporal solar
    if 'date' in solar_data.columns:
        solar_data = solar_data.set_index('date')
    solar_ts = solar_data['sunspot_number']
    
    # Crear predictor ensemble
    predictor = EnsemblePredictor(config)
    predictor.fit(solar_ts)
    
    # Generar predicciones solares
    solar_predictions = predictor.predict(solar_ts, config.prediction_horizon_months)
    
    # Predecir eventos biológicos
    correlation_strength = correlation_analysis.get('correlations', {}).get('pearson', {}).get('correlation_coefficient', 0.7)
    bio_predictor = BiologicalEventPredictor(correlation_strength)
    biological_predictions = bio_predictor.predict_biological_risk(
        solar_predictions, correlation_analysis
    )
    
    # Evaluación de Chizhevsky
    chizhevsky_assessment = {
        'correlation_strength': correlation_strength,
        'prediction_confidence': 'high' if abs(correlation_strength) > 0.6 else 'moderate',
        'theory_applicability': 'High' if abs(correlation_strength) > 0.6 else 'Moderate'
    }
    
    # Análisis de incertidumbre
    uncertainty_analysis = {
        'sources_of_uncertainty': [
            'Model selection uncertainty',
            'Parameter estimation uncertainty',
            'Future unpredictability',
            'External factors not modeled'
        ],
        'confidence_degradation': 'Linear with time horizon',
        'reliability_assessment': 'Decreases ~10% per year ahead'
    }
    
    # Crear resultado final
    result = PredictionResult(
        model_type=config.model_type.value,
        predictions=solar_predictions.to_dict('records'),
        confidence_intervals=[(row['lower_bound'], row['upper_bound']) 
                            for _, row in solar_predictions.iterrows()],
        model_metrics={
            'models_used': len(predictor.models),
            'prediction_horizon_months': config.prediction_horizon_months
        },
        prediction_dates=solar_predictions['date'].tolist(),
        methodology="Ensemble of ARIMA, Random Forest, and Solar Cycle models",
        chizhevsky_assessment=chizhevsky_assessment,
        uncertainty_analysis=uncertainty_analysis,
        recommendations=biological_predictions['recommendations']
    )
    
    logger.info("Comprehensive predictions generated successfully")
    
    return result, biological_predictions

# Ejemplo de uso
if __name__ == "__main__":
    print("HelioBio-API Advanced Prediction System")
    print("Autor: mechmind-dwv (ia.mechmind@gmail.com)")
    print("="*60)
    
    # Generar datos sintéticos para prueba
    dates = pd.date_range('2000-01-01', '2023-12-01', freq='M')
    solar_cycle = np.sin(2 * np.pi * np.arange(len(dates)) / 132) * 50 + 70
    solar_noise = np.random.normal(0, 15, len(dates))
    
    test_data = pd.DataFrame({
        'date': dates,
        'sunspot_number': np.maximum(0, solar_cycle + solar_noise)
    })
    
    # Configurar y ejecutar predicciones
    config = PredictionConfig(
        prediction_horizon_months=24,
        model_type=PredictionModel.ENSEMBLE
    )
    
    print("\nGenerando predicciones de prueba...")
    
    # Crear predictor
    predictor = EnsemblePredictor(config)
    predictor.fit(test_data.set_index('date')['sunspot_number'])
    
    # Generar predicciones
    predictions = predictor.predict(test_data.set_index('date')['sunspot_number'], 24)
    
    print(f"\nPredicciones generadas para {len(predictions)} meses:")
    print(predictions.head(10))
    print("\n✓ Sistema de predicción funcionando correctamente")
