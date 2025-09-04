# app/models/analysis.py

from pydantic import BaseModel, Field, conlist, constr
from typing import Optional, List

class CorrelationResult(BaseModel):
    """
    Modelo de datos para los resultados de un análisis de correlación.
    """
    method: constr(min_length=1) = Field(..., description="El método de correlación utilizado (e.g., 'pearson', 'spearman', 'cross_correlation').")
    correlation_coefficient: float = Field(..., description="El coeficiente de correlación que mide la fuerza de la relación.")
    p_value: float = Field(..., description="El valor p para determinar la significancia estadística del resultado.")
    lag_days: Optional[int] = Field(None, description="El retraso de tiempo en días donde se encontró la correlación más fuerte.")
    strength_interpretation: str = Field(..., description="Una interpretación cualitativa de la fuerza de la correlación (e.g., 'fuerte', 'moderada', 'débil').")
    statistical_significance: bool = Field(..., description="Indica si el resultado es estadísticamente significativo.")

class CycleResult(BaseModel):
    """
    Modelo de datos para los resultados del análisis de ciclos.
    """
    dominant_period_years: float = Field(..., description="El periodo dominante del ciclo en años.")
    confidence_level: Optional[float] = Field(None, description="El nivel de confianza del resultado.")
    secondary_periods: conlist(float, min_length=0) = Field([], description="Otros periodos cíclicos detectados, en años.")
    method_used: str = Field(..., description="El método de análisis de ciclo utilizado (e.g., 'fourier', 'lomb-scargle').")

class PredictionResult(BaseModel):
    """
    Modelo de datos para el resultado de una predicción de series de tiempo.
    """
    forecast_date: str = Field(..., description="La fecha de la predicción.")
    predicted_ssn_values: List[dict] = Field(..., description="Lista de valores de manchas solares (SSN) predichos con sus fechas correspondientes.")
    model: str = Field(..., description="El tipo de modelo de machine learning utilizado para la predicción.")
