# app/api/endpoints/predictions.py

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any
import datetime

# Define un enrutador para los endpoints de predicción.
router = APIRouter()

# Define un modelo de datos Pydantic para una predicción de evento solar.
class SolarEventPrediction(BaseModel):
    """
    Representa una predicción de un evento solar específico.
    """
    predicted_event: str = Field(..., description="Tipo de evento solar pronosticado.")
    probability: float = Field(..., ge=0.0, le=1.0, description="Probabilidad del evento (0.0 a 1.0).")
    prediction_time_utc: str = Field(..., description="Tiempo UTC de la predicción.")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Puntuación de confianza del modelo.")

# Define un modelo para la predicción del impacto biológico.
class BiologicalImpactPrediction(BaseModel):
    """
    Representa una predicción del impacto biológico de un evento solar.
    """
    solar_event_id: str
    predicted_symptoms: List[str]
    predicted_severity: int = Field(..., ge=1, le=10, description="Severidad pronosticada (1 a 10).")
    explanation: str

# ==================== ENDPOINTS DE PREDICCIÓN ====================

@router.get("/predictions/solar_event", response_model=SolarEventPrediction, summary="Predecir un evento solar futuro")
def predict_solar_event(
    date: str = Query(..., example="2025-09-07", description="Fecha para la que se desea la predicción (formato YYYY-MM-DD).")
) -> SolarEventPrediction:
    """
    Realiza una predicción simulada sobre la probabilidad de un evento solar importante
    (por ejemplo, una llamarada de clase X) para una fecha determinada.
    
    En una aplicación real, esta función usaría un modelo de machine learning
    entrenado con datos históricos para generar la predicción.
    """
    # Lógica de predicción simulada.
    # En la vida real, se procesarían los datos de entrada y se ejecutaría un modelo.
    try:
        # Convertir la fecha a un objeto datetime para la simulación
        prediction_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        
        # Simular una lógica de predicción. Por ejemplo, mayor probabilidad en días pares.
        is_high_risk = prediction_date.day % 2 == 0
        probability = 0.95 if is_high_risk else 0.25
        
        # Generar el resultado simulado
        predicted_event = "solar_flare_x_class" if is_high_risk else "minor_solar_flare"
        
        prediction = {
            "predicted_event": predicted_event,
            "probability": probability,
            "prediction_time_utc": datetime.datetime.utcnow().isoformat() + "Z",
            "confidence_score": 0.88 if is_high_risk else 0.75
        }
        return SolarEventPrediction(**prediction)
    except ValueError:
        return {"error": "Formato de fecha inválido. Use YYYY-MM-DD."}

@router.get("/predictions/biological_impact", response_model=BiologicalImpactPrediction, summary="Predecir el impacto biológico de un evento solar")
def predict_biological_impact(
    solar_event_id: str = Query(..., example="X1-20250907", description="ID del evento solar a analizar.")
) -> BiologicalImpactPrediction:
    """
    Realiza una predicción simulada sobre el posible impacto biológico
    de un evento solar.

    Esta función simula la fase final del análisis de la API, donde los
    datos solares se utilizan para prever efectos en la salud humana,
    tal como se exploró en la obra de Chizhevsky.
    """
    # Lógica de predicción simulada basada en el ID del evento.
    if "X1" in solar_event_id:
        return BiologicalImpactPrediction(
            solar_event_id=solar_event_id,
            predicted_symptoms=["dolores de cabeza", "fatiga", "trastornos del sueño"],
            predicted_severity=8,
            explanation="La predicción se basa en una alta correlación histórica entre eventos de clase X y una mayor incidencia de estos síntomas en la población."
        )
    elif "M" in solar_event_id:
        return BiologicalImpactPrediction(
            solar_event_id=solar_event_id,
            predicted_symptoms=["irritabilidad", "ansiedad"],
            predicted_severity=5,
            explanation="Se espera un impacto moderado en el estado de ánimo y la salud mental, alineado con las observaciones históricas."
        )
    else:
        return BiologicalImpactPrediction(
            solar_event_id=solar_event_id,
            predicted_symptoms=["ninguno"],
            predicted_severity=2,
            explanation="No se espera un impacto biológico significativo según los datos de la actividad solar."
        )
