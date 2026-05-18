"""Módulo de Ionismo Digital - Resonancia Schumann + TEC"""
import numpy as np
from typing import Dict
from datetime import datetime

class IonosphereMonitor:
    """Monitor de ionosfera y resonancia Schumann"""
    
    # Frecuencias de Resonancia Schumann (Hz)
    SCHUMANN_FREQUENCIES = {
        "fundamental": 7.83,
        "harmonics": [14.3, 20.8, 27.3, 33.8]
    }
    
    def calculate_schumann_resonance(self, solar_wind_speed: float, geomagnetic_kp: float) -> Dict:
        """Calcula estado de resonancia Schumann basado en actividad solar"""
        # La resonancia Schumann varía con la actividad solar
        base_freq = self.SCHUMANN_FREQUENCIES["fundamental"]
        variation = (solar_wind_speed / 400 - 1) * 0.5 + (geomagnetic_kp / 5 - 1) * 0.3
        current_freq = base_freq * (1 + variation * 0.1)
        
        # Interpretación biológica según Chizhevsky
        if abs(current_freq - base_freq) < 0.1:
            bio_state = "Equilibrio - Ritmos circadianos óptimos"
        elif current_freq > base_freq:
            bio_state = "Excitación - Mayor actividad neural (posible insomnio/ansiedad)"
        else:
            bio_state = "Depresión - Reducción metabólica (posible fatiga/apatía)"
        
        return {
            "schumann_fundamental": round(current_freq, 2),
            "base_frequency": base_freq,
            "variation_percent": round(variation * 100, 1),
            "biological_state": bio_state,
            "ion_quality_index": round(100 - abs(variation) * 50, 1),
            "chizhevsky_ionism_note": "Los iones negativos atmosféricos, modulados por actividad solar, afectan la fisiología celular",
            "timestamp": datetime.now().isoformat()
        }
    
    def estimate_tec(self, ssn: float, solar_zenith: float = 45) -> Dict:
        """Estima Contenido Total de Electrones (TEC) ionosférico"""
        tec_base = 10  # TECU (unidades)
        tec = tec_base + ssn * 0.5 + solar_zenith * 0.1
        
        if tec > 50:
            impact = "ALTO - Posible interferencia en comunicaciones y GPS"
        elif tec > 30:
            impact = "MODERADO - Alteraciones en propagación de radio"
        else:
            impact = "BAJO - Condiciones normales"
        
        return {
            "tec_value": round(tec, 1),
            "unit": "TECU",
            "impact": impact,
            "biological_note": "El TEC elevado correlaciona con mayor incidencia de arritmias (Chizhevsky, 1930s)",
            "timestamp": datetime.now().isoformat()
        }

class BioResonancePredictor:
    """Predictor de efectos biológicos de la resonancia electromagnética"""
    
    def predict_health_effects(self, schumann_variation: float, tec: float) -> Dict:
        """Predice efectos en salud basados en parámetros ionosféricos"""
        effects = []
        risk_score = 0
        
        if schumann_variation > 0.2:
            effects.append("Alteraciones del sueño (ritmos circadianos)")
            risk_score += 0.3
        if schumann_variation < -0.15:
            effects.append("Fatiga crónica y reducción de melatonina")
            risk_score += 0.2
        if tec > 40:
            effects.append("Aumento de arritmias cardíacas")
            risk_score += 0.3
        if tec > 30 and schumann_variation > 0.1:
            effects.append("Mayor incidencia de migrañas")
            risk_score += 0.2
        
        risk_level = "ALTO" if risk_score > 0.6 else ("MODERADO" if risk_score > 0.3 else "BAJO")
        
        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "predicted_effects": effects,
            "chizhevsky_quote": "El campo magnético terrestre es el sistema nervioso del planeta",
            "timestamp": datetime.now().isoformat()
        }
