### app/models/biological.py
#!/usr/bin/env python3
"""
Modelos para eventos biológicos y epidemiológicos
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class PathogenType(str, Enum):
    VIRUS = "virus"
    BACTERIA = "bacteria"
    PARASITE = "parasite"
    FUNGUS = "fungus"
    PRION = "prion"
    UNKNOWN = "unknown"

class TransmissionMode(str, Enum):
    RESPIRATORY = "respiratory"
    CONTACT = "contact"
    VECTOR_BORNE = "vector_borne"
    FOODBORNE = "foodborne"
    WATERBORNE = "waterborne"
    SEXUAL = "sexual"
    BLOODBORNE = "bloodborne"
    UNKNOWN = "unknown"

class EventSeverity(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class BiologicalEvent(BaseModel):
    """Modelo para eventos biológicos/epidemiológicos"""
    id: Optional[int] = None
    name: str = Field(min_length=1, max_length=200)
    start_date: datetime
    end_date: Optional[datetime] = None
    peak_date: Optional[datetime] = None
    death_count: Optional[int] = Field(None, ge=0)
    case_count: Optional[int] = Field(None, ge=0)
    affected_regions: List[str] = []
    pathogen_type: PathogenType = PathogenType.UNKNOWN
    transmission_mode: TransmissionMode = TransmissionMode.UNKNOWN
    severity: EventSeverity = EventSeverity.MODERATE
    solar_correlation: Optional[float] = Field(None, ge=-1, le=1)
    solar_cycle_phase_at_start: Optional[str] = None
    notes: str = ""
    data_source: str = "manual"
    created_at: Optional[datetime] = None
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v
    
    @validator('peak_date')
    def validate_peak_date(cls, v, values):
        if v and 'start_date' in values:
            if v < values['start_date']:
                raise ValueError('Peak date must be after start date')
            if 'end_date' in values and values['end_date'] and v > values['end_date']:
                raise ValueError('Peak date must be before end date')
        return v

class BiologicalParameter(BaseModel):
    """Parámetros biológicos monitoreados"""
    parameter_name: str
    value: float
    unit: str
    measurement_date: datetime
    solar_dependence_coefficient: Optional[float] = Field(None, ge=-1, le=1)
    confidence_level: float = Field(ge=0, le=1)
    data_source: str
    
class HealthMetric(BaseModel):
    """Métricas de salud para correlación"""
    metric_type: str  # "cardiovascular", "neurological", "immune", etc.
    region: str
    date: datetime
    value: float
    population_base: Optional[int] = None
    standardized_rate: Optional[float] = None
    notes: str = ""
