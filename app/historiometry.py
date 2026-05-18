from typing import Dict, List
from datetime import datetime
import numpy as np

HISTORICAL_EVENTS = {
    "1789": {"event": "Revolución Francesa", "ssn_peak": 120.0, "type": "revolución"},
    "1917": {"event": "Revolución Rusa", "ssn_peak": 105.4, "type": "revolución"},
    "1918": {"event": "Gripe Española", "ssn_peak": 105.4, "type": "pandemia"},
    "1939": {"event": "Segunda Guerra Mundial", "ssn_peak": 119.2, "type": "guerra"},
    "1957": {"event": "Gripe Asiática", "ssn_peak": 201.3, "type": "pandemia"},
    "1989": {"event": "Caída del Muro de Berlín", "ssn_peak": 158.5, "type": "revolución"},
    "2008": {"event": "Crisis financiera global", "ssn_peak": 2.2, "type": "económico"},
    "2020": {"event": "COVID-19", "ssn_peak": 5.0, "type": "pandemia"},
}

class SocialExcitabilityIndex:
    def calculate_sei(self, ssn: float, ssn_trend: str = "stable", sentiment_score: float = 0) -> Dict:
        ssn_norm = min(ssn/200, 1.0)
        trend_factor = 1.3 if ssn_trend=="ascending" else (1.0 if ssn_trend=="stable" else 0.7)
        sentiment_factor = 1 + sentiment_score * 0.5
        sei = ssn_norm * trend_factor * sentiment_factor * 100
        if sei > 70: interpretation = "Máxima excitabilidad - Período de revoluciones (Chizhevsky, 1924)"
        elif sei > 40: interpretation = "Excitabilidad moderada - Reorganización social"
        elif sei > 20: interpretation = "Baja excitabilidad - Estabilidad"
        else: interpretation = "Mínima excitabilidad - Gobiernos autocráticos"
        return {"sei_index": round(sei,1), "interpretation": interpretation, "components": {"ssn_normalized": round(ssn_norm,2), "trend_factor": trend_factor}, "timestamp": datetime.now().isoformat()}
    
    def get_historical_correlations(self) -> List[Dict]:
        return [{"year": y, "event": d["event"], "ssn_peak": d["ssn_peak"], "type": d["type"], "chizhevsky_validated": d["ssn_peak"]>50} for y,d in HISTORICAL_EVENTS.items()]

async def get_historiometric_analysis(ssn: float) -> Dict:
    sei_calc = SocialExcitabilityIndex()
    sei = sei_calc.calculate_sei(ssn)
    correlations = sei_calc.get_historical_correlations()
    return {"sei_analysis": sei, "events_count": len(correlations), "validated_by_chizhevsky": sum(1 for c in correlations if c["chizhevsky_validated"]), "timestamp": datetime.now().isoformat()}
