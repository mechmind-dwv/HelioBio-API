import numpy as np
from typing import Dict
from datetime import datetime

class MultiParamPredictor:
    def __init__(self):
        self.weights = {"ssn": 0.5, "solar_flux": 0.3, "geomagnetic": 0.2}
    
    def predict_health_risk(self, ssn: float, solar_flux: float, geomagnetic_ap: float) -> Dict:
        ssn_norm = min(ssn / 200, 1.0)
        flux_norm = min(solar_flux / 300, 1.0)
        geo_norm = min(geomagnetic_ap / 100, 1.0)
        risk_score = ssn_norm * self.weights["ssn"] + flux_norm * self.weights["solar_flux"] + geo_norm * self.weights["geomagnetic"]
        
        if risk_score > 0.7: risk_level = "CRÍTICO"
        elif risk_score > 0.4: risk_level = "ALTO"
        elif risk_score > 0.2: risk_level = "MODERADO"
        else: risk_level = "BAJO"
        
        return {"risk_score": round(risk_score,3), "risk_level": risk_level, "timestamp": datetime.now().isoformat()}

class IoTSimulator:
    @staticmethod
    def generate_health_metrics() -> Dict:
        return {"heart_rate_variability": round(np.random.normal(65,15),1), "sleep_quality": round(np.random.uniform(0.4,0.9),2)}
    
    @staticmethod
    def generate_environmental_metrics() -> Dict:
        return {"temperature": round(np.random.normal(22,5),1), "uv_index": round(np.random.uniform(0,11),1)}
