"""Modelo Transformer para predicción solar avanzada"""
import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta

class MultiParamPredictor:
    """Predictor multiparamétrico: SSN + Flujo Solar + Geomagnetismo"""
    
    def __init__(self):
        self.weights = {
            "ssn": 0.5,
            "solar_flux": 0.3,
            "geomagnetic": 0.2
        }
    
    def predict_health_risk(self, ssn: float, solar_flux: float, geomagnetic_ap: float) -> Dict:
        """Predice riesgo de salud basado en múltiples parámetros"""
        # Normalizar cada parámetro (0-1)
        ssn_norm = min(ssn / 200, 1.0)
        flux_norm = min(solar_flux / 300, 1.0)
        geo_norm = min(geomagnetic_ap / 100, 1.0)
        
        # Ponderación
        risk_score = (
            ssn_norm * self.weights["ssn"] +
            flux_norm * self.weights["solar_flux"] +
            geo_norm * self.weights["geomagnetic"]
        )
        
        # Determinar nivel de riesgo
        if risk_score > 0.7:
            risk_level = "CRÍTICO"
            color = "#d73a4a"
        elif risk_score > 0.4:
            risk_level = "ALTO"
            color = "#ff6600"
        elif risk_score > 0.2:
            risk_level = "MODERADO"
            color = "#ffd700"
        else:
            risk_level = "BAJO"
            color = "#2d7d46"
        
        # Sistemas afectados según Chizhevsky
        affected_systems = []
        if ssn_norm > 0.6:
            affected_systems.append("Cardiovascular (arritmias, hipertensión)")
        if geo_norm > 0.5:
            affected_systems.append("Neurológico (migrañas, alteraciones del sueño)")
        if flux_norm > 0.6:
            affected_systems.append("Inmunológico (mayor susceptibilidad a infecciones)")
        if risk_score > 0.5:
            affected_systems.append("Psicológico (ansiedad, agitación social)")
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "color": color,
            "parameters": {
                "ssn": ssn,
                "solar_flux": solar_flux,
                "geomagnetic_ap": geomagnetic_ap
            },
            "affected_systems": affected_systems,
            "recommendations": [
                "Monitorear pacientes cardiovasculares" if ssn_norm > 0.6 else "",
                "Reforzar sistemas de vigilancia epidemiológica" if flux_norm > 0.6 else "",
                "Preparar recursos médicos adicionales" if risk_score > 0.5 else "",
            ],
            "chizhevsky_correlation": "Alta" if risk_score > 0.5 else "Moderada" if risk_score > 0.2 else "Baja",
            "timestamp": datetime.now().isoformat()
        }

# Simulador de datos IoT (wearables, sensores ambientales)
class IoTSimulator:
    """Simulador de datos de dispositivos IoT"""
    
    @staticmethod
    def generate_health_metrics() -> Dict:
        """Genera métricas de salud simuladas de wearables"""
        return {
            "heart_rate_variability": round(np.random.normal(65, 15), 1),
            "blood_pressure_systolic": round(np.random.normal(120, 10), 1),
            "sleep_quality": round(np.random.uniform(0.4, 0.9), 2),
            "stress_index": round(np.random.uniform(0.1, 0.7), 2),
            "circadian_rhythm_score": round(np.random.uniform(0.5, 1.0), 2),
            "correlation_with_ssn": round(np.random.uniform(0.3, 0.8), 2)
        }
    
    @staticmethod
    def generate_environmental_metrics() -> Dict:
        """Genera métricas ambientales simuladas"""
        return {
            "temperature": round(np.random.normal(22, 5), 1),
            "humidity": round(np.random.uniform(30, 80), 1),
            "air_pressure": round(np.random.normal(1013, 10), 1),
            "uv_index": round(np.random.uniform(0, 11), 1),
            "emf_level": round(np.random.uniform(0.1, 3.0), 2),
            "cosmic_ray_flux": round(np.random.uniform(0.01, 0.5), 3)
        }
