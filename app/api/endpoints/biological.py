# app/api/endpoints/biological.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

# Define un enrutador para los endpoints biológicos.
router = APIRouter()

# Define un modelo de datos Pydantic para los efectos biológicos de un evento solar.
class BiologicalImpact(BaseModel):
    """
    Representa un impacto biológico documentado de la actividad solar.
    """
    event_type: str
    description: str
    symptoms: List[str]
    severity: int  # Escala de 1 a 10
    research_paper_id: str

# Define un modelo de datos para un informe de salud simulado.
class HealthReport(BaseModel):
    """
    Representa un informe de salud subido para el análisis de correlación.
    """
    report_id: str
    date: str
    patient_age: int
    symptom_list: List[str]
    diagnosis: str = None

# ==================== ENDPOINTS DE LA API BIOLÓGICA ====================

@router.get("/biological/impacts", response_model=List[BiologicalImpact], summary="Obtener los impactos biológicos de la actividad solar")
def get_known_biological_impacts() -> List[BiologicalImpact]:
    """
    Retorna una lista de impactos biológicos conocidos o documentados
    asociados con la actividad solar y cósmica.

    Esta función simula datos de estudios científicos para demostrar
    cómo la API podría correlacionar eventos solares con efectos biológicos
    observados, tal como lo propuso el científico Chizhevsky.
    """
    # Datos simulados que representan los hallazgos de investigación.
    impact_data = [
        {
            "event_type": "solar_flare_x_class",
            "description": "Correlación observada con alteraciones en el sistema nervioso central.",
            "symptoms": ["irritabilidad", "dolores de cabeza", "fatiga"],
            "severity": 7,
            "research_paper_id": "heli-bio-2023-01A"
        },
        {
            "event_type": "geomagnetic_storm",
            "description": "Impacto en los ritmos circadianos y la producción de melatonina.",
            "symptoms": ["trastornos del sueño", "ansiedad"],
            "severity": 5,
            "research_paper_id": "heli-bio-2023-02B"
        },
        {
            "event_type": "coronal_mass_ejection",
            "description": "Posible influencia en la presión arterial y la coagulación sanguínea.",
            "symptoms": ["mareos", "náuseas"],
            "severity": 6,
            "research_paper_id": "heli-bio-2023-03C"
        }
    ]
    return [BiologicalImpact(**data) for data in impact_data]

@router.post("/biological/submit_report", summary="Enviar un nuevo informe de salud")
def submit_health_report(report: HealthReport) -> Dict[str, str]:
    """
    Recibe un informe de salud y simula su procesamiento para el análisis de correlación.

    En una aplicación real, este endpoint guardaría el informe en una base de datos
    para su posterior análisis.
    """
    # Aquí iría la lógica para guardar el informe en la base de datos.
    # Por ahora, solo retornamos un mensaje de confirmación.
    print(f"Informe recibido: {report.report_id} del paciente de {report.patient_age} años.")
    return {"message": "Informe de salud recibido con éxito. ID: " + report.report_id}
