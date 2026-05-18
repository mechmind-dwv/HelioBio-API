import numpy as np
from typing import Dict
from datetime import datetime

class IonosphereMonitor:
    SCHUMANN_FREQUENCIES = {"fundamental": 7.83, "harmonics": [14.3, 20.8, 27.3, 33.8]}
    
    def calculate_schumann_resonance(self, solar_wind_speed: float, geomagnetic_kp: float) -> Dict:
        base_freq = self.SCHUMANN_FREQUENCIES["fundamental"]
        variation = (solar_wind_speed / 400 - 1) * 0.5 + (geomagnetic_kp / 5 - 1) * 0.3
        current_freq = base_freq * (1 + variation * 0.1)
        if abs(current_freq - base_freq) < 0.1: bio_state = "Equilibrio - Ritmos circadianos óptimos"
        elif current_freq > base_freq: bio_state = "Excitación - Mayor actividad neural"
        else: bio_state = "Depresión - Reducción metabólica"
        return {"schumann_fundamental": round(current_freq,2), "base_frequency": base_freq, "variation_percent": round(variation*100,1), "biological_state": bio_state, "ion_quality_index": round(100-abs(variation)*50,1), "chizhevsky_note": "Los iones negativos modulados por actividad solar afectan la fisiología celular", "timestamp": datetime.now().isoformat()}
    
    def estimate_tec(self, ssn: float) -> Dict:
        tec = 10 + ssn * 0.5
        impact = "ALTO" if tec>50 else ("MODERADO" if tec>30 else "BAJO")
        return {"tec_value": round(tec,1), "unit": "TECU", "impact": impact, "timestamp": datetime.now().isoformat()}

class BioResonancePredictor:
    def predict_health_effects(self, schumann_variation: float, tec: float) -> Dict:
        effects = []
        risk_score = 0
        if schumann_variation > 0.2: effects.append("Alteraciones del sueño"); risk_score += 0.3
        if tec > 40: effects.append("Aumento de arritmias"); risk_score += 0.3
        if tec > 30 and schumann_variation > 0.1: effects.append("Migrañas"); risk_score += 0.2
        risk_level = "ALTO" if risk_score>0.6 else ("MODERADO" if risk_score>0.3 else "BAJO")
        return {"risk_score": round(risk_score,2), "risk_level": risk_level, "predicted_effects": effects, "chizhevsky_quote": "El campo magnético terrestre es el sistema nervioso del planeta", "timestamp": datetime.now().isoformat()}
