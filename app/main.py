from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import requests
import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = FastAPI(title="HelioBio-API", version="2.0")

class SolarBiologicalCorrelation(BaseModel):
    period: str
    solar_activity: float
    biological_events: int
    correlation_score: float
    prediction: dict
    visualization: str = None

def advanced_correlation_analysis(solar_data, biological_data):
    """Análisis avanzado de correlación usando métodos espectrales"""
    # Análisis de Fourier
    f_solar, Pxx_solar = signal.periodogram(solar_data)
    f_bio, Pxx_bio = signal.periodogram(biological_data)
    
    # Encontrar frecuencias dominantes
    dominant_freqs = {
        'solar': f_solar[np.argmax(Pxx_solar)],
        'biological': f_bio[np.argmax(Pxx_bio)]
    }
    
    # Correlación cruzada
    correlation = np.correlate(solar_data, biological_data, mode='full')
    
    return {
        'dominant_frequencies': dominant_freqs,
        'max_correlation': np.max(correlation),
        'lag': np.argmax(correlation) - len(solar_data) + 1
    }

@app.get("/advanced-analysis/cosmic-biological", response_model=SolarBiologicalCorrelation)
async def cosmic_biological_analysis(
    start_year: int = 1900,
    end_year: int = 2023,
    analysis_type: str = "pandemics"
):
    """Análisis avanzado de correlaciones cósmicas-biológicas"""
    # Obtener datos solares
    solar_data = fetch_historical_solar_data(start_year, end_year)
    
    # Obtener datos biológicos según tipo
    if analysis_type == "pandemics":
        bio_data = fetch_pandemic_data(start_year, end_year)
    elif analysis_type == "social_events":
        bio_data = fetch_social_events_data(start_year, end_year)
    
    # Análisis avanzado
    analysis_result = advanced_correlation_analysis(solar_data, bio_data)
    
    # Crear visualización
    plt.figure(figsize=(12, 8))
    plt.subplot(211)
    plt.plot(solar_data, label='Actividad Solar')
    plt.plot(bio_data, label='Eventos Biológicos')
    plt.legend()
    
    plt.subplot(212)
    plt.specgram(solar_data, Fs=1, cmap='viridis')
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode()
    
    return SolarBiologicalCorrelation(
        period=f"{start_year}-{end_year}",
        solar_activity=np.mean(solar_data),
        biological_events=np.sum(bio_data),
        correlation_score=analysis_result['max_correlation'],
        prediction=analysis_result,
        visualization=img_str
    )
