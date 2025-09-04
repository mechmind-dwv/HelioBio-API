# app/models/alerts.py

from pydantic import BaseModel, Field
from datetime import datetime

class AlertEvent(BaseModel):
    """
    Modelo de datos para un evento de alerta.
    """
    alert_id: str = Field(..., description="Identificador único para el evento de alerta.")
    alert_type: str = Field(..., description="El tipo de alerta (e.g., 'HIGH_SOLAR_ACTIVITY', 'BIOLOGICAL_PEAK_PREDICTION').")
    timestamp: datetime = Field(..., description="Marca de tiempo de la generación de la alerta.")
    message: str = Field(..., description="Un mensaje descriptivo sobre la alerta.")
    source_data: dict = Field(..., description="Datos de origen que dispararon la alerta.")
    severity: str = Field(..., description="Severidad de la alerta (e.g., 'CRITICAL', 'WARNING', 'INFO').")
    triggered_by: str = Field(..., description="El parámetro o evento que activó la alerta.")
