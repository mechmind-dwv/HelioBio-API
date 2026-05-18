#!/usr/bin/env python3
from app.websocket_handler import stream_solar_data, manager
from app.sentiment_analyzer import get_public_sentiment, analyze_sentiment
from app.auth import USERS_DB
from app.auth import create_access_token, verify_password, get_current_user, require_admin
from app.deep_learning import deep_solar_prediction
from app.graphql_api import graphql_app
from app.who_data import get_who_pandemics, get_who_health_indicators
from app.cdc_data import get_cdc_influenza, get_cdc_outbreaks, get_cdc_seasonal_patterns
from app.webhooks import register_webhook, list_webhooks, delete_webhook, trigger_webhooks
from app.email_notifier import send_alert_notification
from app.report_generator import generate_solar_report, generate_correlation_report
from fastapi.responses import Response
from app.solar_fetcher import fetch_real_silso_data
from app.space_weather import fetch_real_space_weather
from app.solar_cycles import get_solar_cycles_data
"""
HelioBio-API - Sistema avanzado de análisis heliobiológico
Basado en los estudios de Alexander Leonidovich Chizhevsky (1897-1964)
"""
import warnings
warnings.filterwarnings("ignore")

import base64
import sqlite3
from datetime import datetime, timedelta
from io import BytesIO
from typing import Any, Dict, List, Optional

import aiohttp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fastapi import FastAPI, Depends, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from scipy import signal, stats
from scipy.signal import find_peaks

from app.solar_fetcher import fetch_real_silso_data
from app.space_weather import fetch_real_space_weather
from app.solar_cycles import get_solar_cycles_data
from app.dashboard import router as dashboard_router

app = FastAPI(
    title="HelioBio-API",
    description="Sistema avanzado de análisis heliobiológico basado en los estudios de Alexander Chizhevsky",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(dashboard_router)
app.include_router(graphql_app, prefix="/graphql")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================== MODELOS DE DATOS ==================

class SolarActivity(BaseModel):
    """Modelo para datos de actividad solar"""
    date: datetime
    sunspot_number: float
    flare_activity: float = 0.0
    geomagnetic_storm: float = 0.0
    classification: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "date": "2024-03-15T00:00:00",
                    "sunspot_number": 125.3,
                    "flare_activity": 12.5,
                    "geomagnetic_storm": 45.2,
                    "classification": "high",
                },
                {
                    "date": "2020-06-01T00:00:00",
                    "sunspot_number": 8.7,
                    "flare_activity": 0.3,
                    "geomagnetic_storm": 5.1,
                    "classification": "low",
                },
            ]
        }
    }


class PandemicData(BaseModel):
    """Modelo para eventos epidemiológicos"""
    name: str
    start_year: int
    end_year: int
    death_count: Optional[int] = None
    affected_regions: List[str] = []
    notes: str
    solar_correlation: Optional[float] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "COVID-19",
                    "start_year": 2019,
                    "end_year": 2023,
                    "death_count": 7000000,
                    "affected_regions": ["Global"],
                    "notes": "Inicio en fase mínima del Ciclo Solar 24",
                    "solar_correlation": 0.68,
                },
                {
                    "name": "Gripe Española",
                    "start_year": 1918,
                    "end_year": 1920,
                    "death_count": 50000000,
                    "affected_regions": ["Global"],
                    "notes": "Máximo solar del Ciclo 15",
                    "solar_correlation": 0.94,
                },
            ]
        }
    }


class CorrelationResult(BaseModel):
    """Modelo para resultados de análisis de correlación"""
    solar_activity_period: str
    event_type: str
    event_name: str
    correlation_score: float
    confidence_interval: List[float]
    p_value: float
    phase_analysis: Dict[str, Any]
    prediction: Dict[str, Any]
    graph_image_base64: Optional[str] = None
    recommendations: List[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "solar_activity_period": "2000-01 a 2024-12",
                    "event_type": "pandemics",
                    "event_name": "COVID-19 + Gripe Española",
                    "correlation_score": 0.72,
                    "confidence_interval": [0.55, 0.85],
                    "p_value": 0.003,
                    "phase_analysis": {
                        "phase_difference": 0.23,
                        "solar_dominant_frequency": 0.089,
                        "seasonal_strength": 0.67,
                    },
                    "prediction": {
                        "next_predicted_maximum": "2025-07",
                        "current_risk_level": "Moderado",
                        "estimated_risk_period": "2025-2026",
                    },
                    "graph_image_base64": "iVBORw0KGgo...",
                    "recommendations": [
                        "Fuerte correlación detectada",
                        "Implementar sistema de alerta temprana",
                    ],
                }
            ]
        }
    }


class HealthAlert(BaseModel):
    """Modelo para alertas de salud"""
    level: str
    message: str
    expected_impact: str
    timeframe: str
    protective_measures: List[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "level": "Moderado",
                    "message": "Actividad solar moderada. Vigilar indicadores de salud.",
                    "expected_impact": "Posible aumento en condiciones cardiovasculares",
                    "timeframe": "Próximas 2-4 semanas",
                    "protective_measures": [
                        "Monitorear pacientes cardiovasculares",
                        "Mantener sistemas de vigilancia activos",
                    ],
                },
                {
                    "level": "Alto",
                    "message": "Alta actividad solar con tendencia creciente.",
                    "expected_impact": "Mayor riesgo de eventos de salud pública",
                    "timeframe": "Próximas 4-8 semanas",
                    "protective_measures": [
                        "Alertar sistemas de salud",
                        "Preparar recursos médicos adicionales",
                    ],
                },
            ]
        }
    }


# ================== BASE DE CONOCIMIENTO ==================

CHIZHEVSKY_KNOWLEDGE_BASE = {
    "solar_cycles": {
        "duration": 11.2,
        "phases": {
            "minimum": {"duration": 3, "characteristics": ["pasividad", "gobierno autocrático"]},
            "organizing": {"duration": 2, "characteristics": ["organización bajo nuevos líderes"]},
            "maximum": {"duration": 3, "characteristics": ["máxima excitabilidad", "revoluciones", "guerras"]},
            "declining": {"duration": 3, "characteristics": ["disminución de excitabilidad", "apatía"]},
        },
    },
    "historical_correlations": {
        "1917": {"solar_activity": "high", "events": ["Revolución Rusa"]},
        "1918": {"solar_activity": "very_high", "events": ["Gripe Española"]},
        "1939": {"solar_activity": "high", "events": ["Inicio Segunda Guerra Mundial"]},
        "1957": {"solar_activity": "high", "events": ["Gripe Asiática"]},
        "1968": {"solar_activity": "medium", "events": ["Revoluciones culturales", "Gripe de Hong Kong"]},
        "1989": {"solar_activity": "high", "events": ["Caída del Muro de Berlín"]},
        "2003": {"solar_activity": "medium", "events": ["SARS"]},
        "2009": {"solar_activity": "low", "events": ["Gripe A(H1N1)"]},
        "2019": {"solar_activity": "low", "events": ["COVID-19"]},
        "2020": {"solar_activity": "rising", "events": ["Pandemia COVID-19 global"]},
    },
    "biological_effects": {
        "cardiovascular": ["arritmias", "hipertensión", "infartos"],
        "neurological": ["migrañas", "epilepsia", "alteraciones del sueño"],
        "immunological": ["supresión inmune", "mayor susceptibilidad a infecciones"],
        "psychological": ["ansiedad", "depresión", "agitación social"],
    },
}

DB_PATH = "heliobio_data.db"


def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS solar_activity (
        date TEXT PRIMARY KEY, sunspot_number REAL, flare_index REAL,
        geomagnetic_ap REAL, solar_wind_speed REAL, cosmic_ray_intensity REAL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS epidemiological_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, start_date TEXT, end_date TEXT,
        death_count INTEGER, affected_regions TEXT, solar_correlation REAL, notes TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS correlations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, event_type TEXT, solar_parameter TEXT,
        correlation_score REAL, p_value REAL, timeframe TEXT, analysis_date TEXT)""")
    conn.commit()
    conn.close()


# ================== OBTENCIÓN DE DATOS ==================

async def fetch_solar_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Obtiene datos SOLARES REALES del SILSO (Royal Observatory Belgium)"""
    from app.solar_fetcher import fetch_real_silso_data
    return await fetch_real_silso_data(start_date, end_date)

def get_epidemiological_data() -> pd.DataFrame:
    pandemics = [
        {"name": "Influenza Rusa", "start_year": 1889, "end_year": 1890,
         "death_count": 1000000, "affected_regions": ["Global"],
         "solar_correlation": 0.87, "notes": "Asociada con máximo solar. Ciclo solar 13."},
        {"name": "Gripe Española", "start_year": 1918, "end_year": 1920,
         "death_count": 50000000, "affected_regions": ["Global"],
         "solar_correlation": 0.92, "notes": "Inicio durante máximo solar. Ciclo solar 15."},
        {"name": "Gripe Asiática", "start_year": 1957, "end_year": 1958,
         "death_count": 2000000, "affected_regions": ["Global"],
         "solar_correlation": 0.78, "notes": "Inicio durante máximo solar. Ciclo solar 19."},
        {"name": "COVID-19", "start_year": 2019, "end_year": 2023,
         "death_count": 7000000, "affected_regions": ["Global"],
         "solar_correlation": 0.65, "notes": "Inicio en fase mínima del Ciclo Solar 24."},
    ]
    return pd.DataFrame(pandemics)


# ================== ANÁLISIS ==================

def advanced_correlation_analysis(solar_df: pd.DataFrame, event_dates: List[datetime]) -> Dict[str, Any]:
    solar_values = solar_df["sunspot_number"].values
    event_density = np.zeros(len(solar_df))
    for ev in event_dates:
        diffs = np.abs((solar_df["date"] - ev).dt.days)
        idx = diffs.idxmin()
        if idx < len(event_density):
            event_density[idx] += 1
    smoothed = np.convolve(event_density, np.ones(12) / 12, mode="same")
    try:
        corr, pval = stats.pearsonr(solar_values, smoothed)
        if np.isnan(corr):
            corr, pval = 0.0, 1.0
    except:
        corr, pval = 0.0, 1.0

    f_s, Pxx_s = signal.periodogram(solar_values, fs=1)
    f_e, Pxx_e = signal.periodogram(smoothed, fs=1)

    phase_s = np.angle(signal.hilbert(solar_values - np.mean(solar_values)))
    phase_e = np.angle(signal.hilbert(smoothed - np.mean(smoothed)))
    phase_diff = np.mean(np.abs(phase_s - phase_e))

    return {
        "pearson_correlation": corr,
        "p_value": pval,
        "solar_dominant_frequency": f_s[np.argmax(Pxx_s)],
        "events_dominant_frequency": f_e[np.argmax(Pxx_e)],
        "phase_difference": phase_diff,
        "seasonal_strength": 0,
        "confidence_interval": [
            corr - 1.96 * np.sqrt((1 - corr**2) / (len(solar_values) - 2)),
            corr + 1.96 * np.sqrt((1 - corr**2) / (len(solar_values) - 2)),
        ],
    }


def predict_next_events(solar_df: pd.DataFrame, analysis: Dict) -> Dict[str, Any]:
    solar_series = pd.Series(solar_df["sunspot_number"].values, index=solar_df["date"])
    peaks, _ = find_peaks(solar_series, height=50, distance=100)
    next_maxima = []
    if len(peaks) > 2:
        peak_dates = solar_series.index[peaks]
        intervals = np.diff(peak_dates).astype("timedelta64[M]").astype(int)
        avg_interval = np.mean(intervals)
        next_peak = peak_dates[-1] + pd.DateOffset(months=avg_interval)
        next_maxima.append(next_peak)

    current = solar_series.iloc[-1]
    max_s = solar_series.max()
    min_s = solar_series.min()
    phase = (current - min_s) / (max_s - min_s) if max_s > min_s else 0.5
    risk = "Alto" if phase > 0.7 else "Bajo" if phase < 0.3 else "Moderado"

    return {
        "next_predicted_maximum": next_maxima[0].strftime("%Y-%m") if next_maxima else "Desconocido",
        "current_risk_level": risk,
        "estimated_risk_period": f"{next_maxima[0].strftime('%Y-%m') if next_maxima else '2024-2025'}",
        "recommended_actions": [
            "Monitorear indicadores de salud pública",
            "Fortalecer sistemas de vigilancia epidemiológica",
            "Preparar recursos médicos para posibles aumentos de demanda",
        ],
    }


# ================== ENDPOINTS ==================

@app.get("/")
async def root():
    return {"message": "HelioBio-API - Sistema de análisis heliobiológico basado en los estudios de Alexander Chizhevsky"}


@app.get("/solar/activity", response_model=List[SolarActivity])
async def get_solar_activity(start_date: str = "2000-01-01", end_date: str = "2023-12-31"):
    df = await fetch_solar_data(start_date, end_date)
    return df.to_dict("records")


@app.get("/health/events", response_model=List[PandemicData])
async def get_health_events():
    return get_epidemiological_data().to_dict("records")


@app.get("/analysis/correlate", response_model=CorrelationResult)
async def correlate_events(
    event_type: str = "pandemics",
    parameter: str = "sunspots",
    years_before: int = 10,
    years_after: int = 5,
):
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365 * (years_before + years_after))).strftime("%Y-%m-%d")
    solar_df = await fetch_solar_data(start_date, end_date)

    if event_type == "pandemics":
        events_df = get_epidemiological_data()
        event_dates = [datetime(year, 6, 15) for year in events_df["start_year"]]
    else:
        event_dates = [datetime(y, 6, 15) for y in [1917, 1939, 1968, 1989, 2001]]

    analysis = advanced_correlation_analysis(solar_df, event_dates)
    prediction = predict_next_events(solar_df, analysis)

    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(solar_df["date"], solar_df["sunspot_number"], "b-", label="Manchas Solares")
    plt.ylabel("Manchas Solares")
    plt.title("Actividad Solar y Eventos Históricos")
    plt.grid(True)
    plt.legend()
    for i, ev in enumerate(event_dates):
        plt.axvline(x=ev, color="r", linestyle="--", alpha=0.7)
        plt.text(ev, plt.ylim()[1] * 0.9, f"Evento {i+1}", rotation=90, va="top")

    plt.subplot(2, 1, 2)
    event_density = np.zeros(len(solar_df))
    for ev in event_dates:
        diffs = np.abs((solar_df["date"] - ev).dt.days)
        idx = diffs.idxmin()
        if idx < len(event_density):
            event_density[idx] += 1
    smoothed = np.convolve(event_density, np.ones(12) / 12, mode="same")
    plt.plot(solar_df["date"], solar_df["sunspot_number"] / max(solar_df["sunspot_number"]), "b-", label="Solar (norm)")
    plt.plot(solar_df["date"], smoothed / max(smoothed), "r-", label="Eventos (norm)")
    plt.xlabel("Año")
    plt.ylabel("Normalizado")
    plt.legend()
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    recs = []
    if analysis["pearson_correlation"] > 0.6:
        recs.append("Fuerte correlación detectada. Considerar sistema de alerta temprana.")
    if analysis["phase_difference"] < 0.5:
        recs.append("Los eventos tienden a ocurrir en fases solares específicas.")

    return CorrelationResult(
        solar_activity_period=f"{solar_df['date'].min().strftime('%Y-%m')} a {solar_df['date'].max().strftime('%Y-%m')}",
        event_type=event_type,
        event_name="Eventos históricos múltiples",
        correlation_score=analysis["pearson_correlation"],
        confidence_interval=analysis["confidence_interval"],
        p_value=analysis["p_value"],
        phase_analysis={
            "phase_difference": analysis["phase_difference"],
            "solar_dominant_frequency": analysis["solar_dominant_frequency"],
            "seasonal_strength": analysis["seasonal_strength"],
        },
        prediction=prediction,
        graph_image_base64=img_str,
        recommendations=recs,
    )


@app.get("/alerts/current", response_model=List[HealthAlert])
async def get_current_alerts():
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    df = await fetch_solar_data(start_date, end_date)

    recent = df["sunspot_number"].tail(30).mean()
    last_n = min(30, len(df))
    trend = np.polyfit(range(last_n), df["sunspot_number"].tail(last_n).values, 1)[0] if last_n >= 2 else 0

    if recent > 100 and trend > 0:
        level, msg = "Alto", "Alta actividad solar con tendencia creciente."
        measures = ["Monitorear pacientes cardiovasculares", "Alertar sistemas de salud", "Precaución al aire libre"]
    elif recent > 50:
        level, msg = "Moderado", "Actividad solar moderada."
        measures = ["Observar tendencias de salud", "Mantener monitoreo activo"]
    else:
        level, msg = "Bajo", "Actividad solar baja. Riesgo mínimo."
        measures = ["Continuar monitoreo rutinario"]

    return [HealthAlert(
        level=level, message=msg,
        expected_impact="Posible aumento en condiciones cardiovasculares y neurológicas",
        timeframe="Próximas 2-4 semanas",
        protective_measures=measures,
    )]


@app.get("/chizhevsky/knowledge")
async def get_chizhevsky_knowledge():
    return CHIZHEVSKY_KNOWLEDGE_BASE


@app.on_event("startup")
async def startup():
    init_database()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

@app.get("/space-weather")
async def get_space_weather():
    """Datos de clima espacial en tiempo real de NOAA"""
    return await fetch_real_space_weather()

@app.get("/solar-cycles")
async def get_solar_cycles():
    """Historial completo de ciclos solares (1755-presente)"""
    return get_solar_cycles_data().to_dict("records")

@app.get("/report/solar")
async def get_solar_report(start_date: str = "2024-01-01", end_date: str = "2024-12-31"):
    """Genera y descarga un informe PDF de actividad solar"""
    df = await fetch_solar_data(start_date, end_date)
    solar_data = df.to_dict("records")
    pdf_bytes = generate_solar_report(solar_data)
    return Response(content=pdf_bytes, media_type="application/pdf",
                   headers={"Content-Disposition": f"attachment; filename=informe_solar_{start_date}_{end_date}.pdf"})

@app.get("/report/correlation")
async def get_correlation_report(years_before: int = 10, years_after: int = 5):
    """Genera y descarga un informe PDF de análisis de correlación"""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365*(years_before + years_after))).strftime("%Y-%m-%d")
    solar_df = await fetch_solar_data(start_date, end_date)
    events_df = get_epidemiological_data()
    event_dates = [datetime(year, 6, 15) for year in events_df["start_year"]]
    analysis = advanced_correlation_analysis(solar_df, event_dates)
    prediction = predict_next_events(solar_df, analysis)
    
    correlation_data = {
        "correlation_score": analysis["pearson_correlation"],
        "p_value": analysis["p_value"],
        "prediction": prediction,
        "recommendations": [
            "Fuerte correlación detectada. Considerar sistema de alerta temprana." if analysis["pearson_correlation"] > 0.6 else "Correlación moderada.",
            "Los eventos tienden a ocurrir en fases solares específicas." if analysis["phase_difference"] < 0.5 else ""
        ]
    }
    pdf_bytes = generate_correlation_report(correlation_data)
    return Response(content=pdf_bytes, media_type="application/pdf",
                   headers={"Content-Disposition": "attachment; filename=informe_correlacion.pdf"})

@app.post("/notify/subscribe")
async def subscribe_notifications(email: str):
    """Suscribe un email para recibir notificaciones de alertas"""
    return {"status": "subscribed", "email": email, "message": "Recibirás alertas de HelioBio-API"}

@app.post("/notify/test")
async def test_notification(email: str = "ia.mechmind@gmail.com"):
    """Envía una notificación de prueba"""
    test_alert = {
        "level": "Moderado",
        "message": "Prueba del sistema de notificaciones HelioBio-API",
        "expected_impact": "Ninguno - solo prueba",
        "timeframe": "Inmediato",
        "protective_measures": ["Esto es una prueba del sistema"]
    }
    success = await send_alert_notification(test_alert, [email])
    return {"status": "sent" if success else "failed", "email": email}

@app.post("/webhooks/register")
async def webhook_register(url: str, events: str = "alert,solar_update"):
    """Registra un nuevo webhook para recibir notificaciones"""
    event_list = [e.strip() for e in events.split(",")]
    return await register_webhook(url, event_list)

@app.get("/webhooks")
async def webhook_list():
    """Lista todos los webhooks registrados"""
    return await list_webhooks()

@app.delete("/webhooks/{webhook_id}")
async def webhook_delete(webhook_id: int):
    """Elimina un webhook"""
    success = await delete_webhook(webhook_id)
    return {"status": "deleted" if success else "not found"}

@app.post("/webhooks/test")
async def webhook_test(event: str = "alert"):
    """Prueba el sistema de webhooks"""
    test_payload = {"message": "Prueba de webhook HelioBio-API", "source": "test"}
    count = await trigger_webhooks(event, test_payload)
    return {"event": event, "webhooks_triggered": count}

@app.get("/who/pandemics")
async def who_pandemics():
    """Pandemias verificadas por la OMS con correlación solar"""
    return get_who_pandemics()

@app.get("/who/health-indicators")
async def who_indicators():
    """Indicadores globales de salud de la OMS"""
    return get_who_health_indicators()

@app.get("/cdc/influenza")
async def cdc_influenza():
    """Vigilancia de influenza del CDC"""
    return get_cdc_influenza()

@app.get("/cdc/outbreaks")
async def cdc_outbreaks():
    """Brotes documentados por el CDC"""
    return get_cdc_outbreaks()

@app.get("/cdc/seasonal-patterns")
async def cdc_patterns():
    """Patrones estacionales según CDC"""
    return get_cdc_seasonal_patterns()

@app.post("/auth/login")
async def login(username: str, password: str):
    """Inicia sesión y obtiene token JWT"""
    if username in USERS_DB and verify_password(password, USERS_DB[username]["hashed_password"]):
        token = create_access_token({"sub": username, "role": USERS_DB[username]["role"]})
        return {"access_token": token, "token_type": "bearer", "role": USERS_DB[username]["role"]}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

@app.get("/auth/me")
async def me(user: dict = Depends(get_current_user)):
    """Información del usuario autenticado"""
    return user

@app.get("/admin/stats")
async def admin_stats(user: dict = Depends(require_admin)):
    """Estadísticas solo para administradores"""
    return {"message": "Panel de administración", "user": user, "endpoints": 24, "tests": 27}

@app.get("/predict/deep-learning")
async def deep_prediction(months_ahead: int = 12):
    """Predicción solar con Deep Learning (LSTM)"""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365*15)).strftime("%Y-%m-%d")
    solar_df = await fetch_solar_data(start_date, end_date)
    solar_data = solar_df.to_dict('records')
    return await deep_solar_prediction(solar_data, months_ahead)

@app.websocket("/ws/solar-stream")
async def websocket_solar(websocket: WebSocket):
    """Streaming de actividad solar en tiempo real vía WebSocket"""
    await stream_solar_data(websocket)

@app.get("/sentiment/public")
async def public_sentiment():
    """Análisis de sentimiento público sobre eventos heliobiológicos"""
    return await get_public_sentiment()

@app.get("/sentiment/analyze")
async def analyze_custom_text(text: str):
    """Analiza el sentimiento de un texto personalizado"""
    result = await analyze_sentiment([text])
    return result
