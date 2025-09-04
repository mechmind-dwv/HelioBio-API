### app/models/solar.py
#!/usr/bin/env python3
"""
Modelos de datos para actividad solar
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class SolarCyclePhase(str, Enum):
    MINIMUM = "minimum"
    ASCENDING = "ascending"
    MAXIMUM = "maximum"
    DECLINING = "declining"
    UNKNOWN = "unknown"

class SolarActivityLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"

class SolarActivity(BaseModel):
    """Modelo para datos de actividad solar"""
    id: Optional[int] = None
    date: datetime
    sunspot_number: float = Field(ge=0, description="Número de manchas solares")
    solar_flux_10_7: Optional[float] = Field(None, ge=0, description="Flujo solar a 10.7 cm")
    geomagnetic_ap: Optional[float] = Field(None, ge=0, description="Índice geomagnético Ap")
    solar_wind_speed: Optional[float] = Field(None, ge=0, description="Velocidad del viento solar (km/s)")
    cosmic_ray_intensity: Optional[float] = Field(None, description="Intensidad de rayos cósmicos")
    solar_cycle: Optional[int] = Field(None, ge=1, description="Número del ciclo solar")
    cycle_phase: SolarCyclePhase = SolarCyclePhase.UNKNOWN
    activity_level: SolarActivityLevel = SolarActivityLevel.LOW
    data_source: str = "unknown"
    created_at: Optional[datetime] = None
    
    @validator('sunspot_number')
    def validate_ssn(cls, v):
        if v < 0:
            raise ValueError('Sunspot number cannot be negative')
        return v
    
    @validator('activity_level', pre=True, always=True)
    def determine_activity_level(cls, v, values):
        if 'sunspot_number' in values:
            ssn = values['sunspot_number']
            if ssn < 10:
                return SolarActivityLevel.VERY_LOW
            elif ssn < 30:
                return SolarActivityLevel.LOW
            elif ssn < 70:
                return SolarActivityLevel.MODERATE
            elif ssn < 120:
                return SolarActivityLevel.HIGH
            elif ssn < 200:
                return SolarActivityLevel.VERY_HIGH
            else:
                return SolarActivityLevel.EXTREME
        return v

class SolarForecast(BaseModel):
    """Modelo para predicciones de actividad solar"""
    date: datetime
    predicted_ssn: float = Field(ge=0)
    lower_bound: float = Field(ge=0)
    upper_bound: float = Field(ge=0)
    confidence_level: float = Field(ge=0, le=1)
    cycle_phase: SolarCyclePhase
    forecast_method: str
    
    @validator('upper_bound')
    def validate_bounds(cls, v, values):
        if 'lower_bound' in values and v < values['lower_bound']:
            raise ValueError('Upper bound must be greater than lower bound')
        return v

class SolarCycleInfo(BaseModel):
    """Información del ciclo solar actual"""
    cycle_number: int = Field(ge=1)
    start_date: Optional[datetime] = None
    expected_maximum: Optional[datetime] = None
    current_phase: SolarCyclePhase
    cycle_progress: float = Field(ge=0, le=1, description="Progreso del ciclo (0-1)")
    cycle_strength: str = Field(description="weak, moderate, strong")
    estimated_duration_months: int = Field(ge=80, le=180)
