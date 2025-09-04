# app/api/endpoints/alerts.py

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import datetime

# Define un enrutador para los endpoints de alertas.
router = APIRouter()

# ==================== MODELOS DE DATOS ====================

# Modelo para un contacto de alerta.
class AlertContact(BaseModel):
    """
    Representa un contacto de notificación.
    """
    contact_id: str
    contact_type: str  # e.g., "email", "sms"
    value: str

# Modelo para una alerta generada.
class GeneratedAlert(BaseModel):
    """
    Representa una alerta generada por el sistema.
    """
    alert_id: str
    alert_level: str = Field(..., description="Nivel de la alerta (ej., 'baja', 'media', 'alta').")
    event_summary: str
    timestamp_utc: str
    recipients: List[str]  # IDs de los contactos que recibieron la alerta

# ==================== ENDPOINTS DE ALERTAS ====================

@router.post("/alerts/subscribe", summary="Suscribir un nuevo contacto para recibir alertas")
def subscribe_to_alerts(contact: AlertContact) -> Dict[str, str]:
    """
    Permite que un usuario se suscriba para recibir alertas.

    En una aplicación real, esta función validaría el contacto y lo guardaría
    en una base de datos para futuras notificaciones.
    """
    # Lógica simulada de suscripción.
    print(f"Nuevo contacto suscrito: ID {contact.contact_id}, Tipo: {contact.contact_type}, Valor: {contact.value}")
    return {"message": f"Suscripción de {contact.value} exitosa."}

@router.get("/alerts/latest", response_model=List[GeneratedAlert], summary="Obtener las últimas alertas generadas")
def get_latest_alerts() -> List[GeneratedAlert]:
    """
    Retorna una lista de las últimas alertas de eventos solares
    que han sido emitidas por el sistema.

    Esto permite a los usuarios o a los sistemas externos obtener
    un historial de las notificaciones más recientes.
    """
    # Datos simulados de alertas.
    # En la realidad, esta función consultaría el historial de la base de datos de alertas.
    now = datetime.datetime.utcnow().isoformat() + "Z"
    alerts_data = [
        {
            "alert_id": "alert-001",
            "alert_level": "baja",
            "event_summary": "Se ha detectado una llamarada de clase C menor. No se espera un impacto significativo.",
            "timestamp_utc": now,
            "recipients": ["contact-123", "contact-456"]
        },
        {
            "alert_id": "alert-002",
            "alert_level": "alta",
            "event_summary": "PRECAUCIÓN: Probabilidad alta de una llamarada de clase X en las próximas 12 horas. Posible interrupción de comunicaciones.",
            "timestamp_utc": now,
            "recipients": ["contact-123", "contact-789"]
        }
    ]
    return [GeneratedAlert(**data) for data in alerts_data]
