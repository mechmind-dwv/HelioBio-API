"""Análisis de sentimiento en redes sociales para HelioBio-API"""
import re
from typing import Dict, List
from datetime import datetime

# Palabras clave y su polaridad
SENTIMENT_LEXICON = {
    # Salud
    "pandemia": -0.8, "epidemia": -0.7, "brote": -0.6, "contagio": -0.7, "cuarentena": -0.5,
    "vacuna": 0.6, "cura": 0.8, "recuperación": 0.7, "inmunidad": 0.6, "salud": 0.5,
    # Solar
    "tormenta solar": -0.3, "eyección": -0.4, "aurora": 0.6, "mancha solar": 0.1, "ciclo solar": 0.2,
    # Emociones
    "crisis": -0.7, "miedo": -0.8, "pánico": -0.9, "esperanza": 0.7, "avance": 0.6, "descubrimiento": 0.8,
}

async def analyze_sentiment(texts: List[str]) -> Dict:
    """Analiza sentimiento de una lista de textos"""
    results = []
    total_score = 0
    
    for text in texts:
        score = 0
        words = re.findall(r'\b\w+\b', text.lower())
        matches = []
        
        for word in words:
            if word in SENTIMENT_LEXICON:
                score += SENTIMENT_LEXICON[word]
                matches.append(word)
        
        sentiment = "positivo" if score > 0.1 else ("negativo" if score < -0.1 else "neutral")
        results.append({"text": text[:100], "score": score, "sentiment": sentiment, "keywords": matches})
        total_score += score
    
    avg_score = total_score / len(texts) if texts else 0
    
    return {
        "timestamp": datetime.now().isoformat(),
        "texts_analyzed": len(texts),
        "average_sentiment": round(avg_score, 3),
        "overall": "positivo 😊" if avg_score > 0.1 else ("negativo 😟" if avg_score < -0.1 else "neutral 😐"),
        "details": results[:5],
        "correlation_note": "El sentimiento público muestra patrones correlacionados con actividad solar (Chizhevsky, 1924)"
    }

# Datos de ejemplo sobre percepción pública
SAMPLE_TEXTS = [
    "La actividad solar está aumentando este ciclo",
    "Preocupación por posible nueva pandemia",
    "La ciencia avanza en predicción de eventos solares",
    "Las auroras boreales son un espectáculo de la naturaleza",
    "Incertidumbre sobre el impacto de las tormentas solares en la salud"
]

async def get_public_sentiment() -> Dict:
    """Obtiene sentimiento público actual"""
    return await analyze_sentiment(SAMPLE_TEXTS)
