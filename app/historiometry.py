"""Módulo de Historiometría - Chizhevsky"""
from typing import Dict, List
from datetime import datetime
import numpy as np

# Base de datos historiométrica verificada
HISTORICAL_EVENTS = {
    "1789": {"event": "Revolución Francesa", "ssn_peak": 120.0, "solar_cycle": 5, "type": "revolución"},
    "1848": {"event": "Primavera de los Pueblos", "ssn_peak": 98.3, "solar_cycle": 9, "type": "revolución"},
    "1871": {"event": "Comuna de París", "ssn_peak": 140.3, "solar_cycle": 11, "type": "revolución"},
    "1905": {"event": "Revolución Rusa de 1905", "ssn_peak": 64.2, "solar_cycle": 14, "type": "revolución"},
    "1914": {"event": "Inicio Primera Guerra Mundial", "ssn_peak": 87.9, "solar_cycle": 15, "type": "guerra"},
    "1917": {"event": "Revolución Rusa", "ssn_peak": 105.4, "solar_cycle": 15, "type": "revolución"},
    "1918": {"event": "Gripe Española", "ssn_peak": 105.4, "solar_cycle": 15, "type": "pandemia"},
    "1929": {"event": "Crack de Wall Street", "ssn_peak": 78.1, "solar_cycle": 16, "type": "económico"},
    "1939": {"event": "Segunda Guerra Mundial", "ssn_peak": 119.2, "solar_cycle": 17, "type": "guerra"},
    "1945": {"event": "Bombas atómicas / Fin WWII", "ssn_peak": 151.8, "solar_cycle": 18, "type": "guerra"},
    "1957": {"event": "Gripe Asiática / Sputnik", "ssn_peak": 201.3, "solar_cycle": 19, "type": "pandemia"},
    "1968": {"event": "Revoluciones culturales / Mayo 68", "ssn_peak": 110.6, "solar_cycle": 20, "type": "revolución"},
    "1989": {"event": "Caída del Muro de Berlín", "ssn_peak": 158.5, "solar_cycle": 22, "type": "revolución"},
    "2001": {"event": "11-S / Atentados", "ssn_peak": 120.8, "solar_cycle": 23, "type": "conflicto"},
    "2008": {"event": "Crisis financiera global", "ssn_peak": 2.2, "solar_cycle": 24, "type": "económico"},
    "2020": {"event": "COVID-19 / Confinamiento global", "ssn_peak": 5.0, "solar_cycle": 24, "type": "pandemia"},
}

class SocialExcitabilityIndex:
    """Índice de Excitabilidad Social según Chizhevsky"""
    
    def calculate_sei(self, ssn: float, ssn_trend: str, sentiment_score: float = 0) -> Dict:
        """
        Calcula el Índice de Excitabilidad Social (SEI)
        Basado en la teoría de Chizhevsky: máxima excitabilidad en picos solares
        """
        # Normalizar SSN (0-1)
        ssn_norm = min(ssn / 200, 1.0)
        
        # Factor de tendencia
        trend_factor = 1.3 if ssn_trend == "ascending" else (1.0 if ssn_trend == "stable" else 0.7)
        
        # Factor de sentimiento social (de v4.0.0)
        sentiment_factor = 1 + sentiment_score * 0.5
        
        # SEI compuesto
        sei = ssn_norm * trend_factor * sentiment_factor * 100
        
        # Interpretación
        if sei > 70:
            interpretation = "Máxima excitabilidad - Período de revoluciones y guerras (Chizhevsky, 1924)"
        elif sei > 40:
            interpretation = "Excitabilidad moderada - Reorganización social y nuevos movimientos"
        elif sei > 20:
            interpretation = "Baja excitabilidad - Estabilidad y apatía social"
        else:
            interpretation = "Mínima excitabilidad - Consolidación de gobiernos autocráticos"
        
        return {
            "sei_index": round(sei, 1),
            "interpretation": interpretation,
            "components": {
                "ssn_normalized": round(ssn_norm, 2),
                "trend_factor": trend_factor,
                "sentiment_factor": round(sentiment_factor, 2)
            },
            "historical_parallel": self._find_historical_parallel(ssn),
            "chizhevsky_note": "Los máximos solares correlacionan con picos de excitabilidad colectiva",
            "timestamp": datetime.now().isoformat()
        }
    
    def _find_historical_parallel(self, ssn: float) -> str:
        """Encuentra el evento histórico más similar según SSN"""
        closest = None
        closest_diff = float('inf')
        for year, data in HISTORICAL_EVENTS.items():
            diff = abs(data["ssn_peak"] - ssn)
            if diff < closest_diff:
                closest_diff = diff
                closest = data
        
        if closest:
            return f"Similar a {closest['event']} ({closest['type']}) - SSN={closest['ssn_peak']}"
        return "Sin paralelo histórico cercano"

    def get_historical_correlations(self) -> List[Dict]:
        """Retorna la base de datos historiométrica completa"""
        return [
            {
                "year": year,
                "event": data["event"],
                "ssn_peak": data["ssn_peak"],
                "solar_cycle": data["solar_cycle"],
                "type": data["type"],
                "chizhevsky_validated": data["ssn_peak"] > 50  # Validado si SSN > 50
            }
            for year, data in HISTORICAL_EVENTS.items()
        ]

async def get_historiometric_analysis(ssn: float, sentiment: float = 0) -> Dict:
    """Análisis historiométrico completo"""
    sei_calc = SocialExcitabilityIndex()
    sei = sei_calc.calculate_sei(ssn, "ascending" if ssn > 80 else "stable", sentiment)
    correlations = sei_calc.get_historical_correlations()
    
    return {
        "sei_analysis": sei,
        "historical_events_count": len(correlations),
        "events_validated_by_chizhevsky": sum(1 for c in correlations if c["chizhevsky_validated"]),
        "events_by_type": {
            "revolución": sum(1 for c in correlations if c["type"] == "revolución"),
            "guerra": sum(1 for c in correlations if c["type"] == "guerra"),
            "pandemia": sum(1 for c in correlations if c["type"] == "pandemia"),
            "económico": sum(1 for c in correlations if c["type"] == "económico"),
        },
        "correlation_note": "Chizhevsky demostró que ~78% de los eventos históricos ocurren en máximos solares",
        "timestamp": datetime.now().isoformat()
    }
