# app/api/endpoints/solar.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

# Define un enrutador para los endpoints solares.
# Esto permite agrupar rutas relacionadas y organizarlas mejor en el código.
router = APIRouter()

# Define un modelo de datos Pydantic para la actividad solar actual.
# Pydantic nos ayuda a validar y documentar automáticamente los datos de la respuesta.
class SolarActivity(BaseModel):
    """
    Representa el estado actual de la actividad solar.
    """
    sunspot_number: int
    solar_flux: float
    flare_class: str
    last_updated: str

# Define un modelo de datos para los eventos de llamaradas solares históricos.
class SolarFlareEvent(BaseModel):
    """
    Representa un evento de llamarada solar individual.
    """
    date: str
    time: str
    flare_class: str
    region: str
    notes: str = None

# ==================== ENDPOINTS DE LA API SOLAR ====================

@router.get("/solar/current", response_model=SolarActivity, summary="Obtener la actividad solar actual")
def get_current_solar_activity() -> SolarActivity:
    """
    Retorna datos de actividad solar simulados.
    
    Esta función simula una respuesta de una fuente de datos en tiempo real,
    proporcionando información como el número de manchas solares y el flujo.
    """
    # Datos simulados para demostración. En una aplicación real,
    # esta información provendría de una base de datos o de una API externa.
    data = {
        "sunspot_number": 156,
        "solar_flux": 125.7,
        "flare_class": "C1.2",
        "last_updated": "2025-09-04T10:00:00Z"
    }
    return SolarActivity(**data)

@router.get("/solar/historical_flares", response_model=List[SolarFlareEvent], summary="Obtener un historial de llamaradas solares")
def get_historical_solar_flares() -> List[SolarFlareEvent]:
    """
    Retorna un conjunto de eventos de llamaradas solares históricos simulados.
    
    Esto es útil para el análisis y la visualización de datos históricos.
    """
    # Datos históricos simulados.
    historical_data = [
        {
            "date": "2025-08-30",
            "time": "14:15:00Z",
            "flare_class": "M5.6",
            "region": "3456",
            "notes": "Associated with a large coronal mass ejection (CME)."
        },
        {
            "date": "2025-08-28",
            "time": "08:30:00Z",
            "flare_class": "X1.1",
            "region": "3452",
            "notes": "Powerful flare that caused a radio blackout."
        },
        {
            "date": "2025-08-25",
            "time": "22:05:00Z",
            "flare_class": "C3.4",
            "region": "3449"
        }
    ]
    return [SolarFlareEvent(**d) for d in historical_data]
