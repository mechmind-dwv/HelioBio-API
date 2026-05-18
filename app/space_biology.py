import numpy as np
from typing import Dict
from datetime import datetime

class SpaceColonySimulator:
    MISSION_DATA = {
        "ISS": {"radiation_mSv_day": 0.5, "magnetic_shield": True},
        "Moon": {"radiation_mSv_day": 1.5, "magnetic_shield": False},
        "Mars": {"radiation_mSv_day": 1.8, "magnetic_shield": False},
        "Deep Space": {"radiation_mSv_day": 2.5, "magnetic_shield": False},
    }
    
    def calculate_radiation_exposure(self, destination: str, ssn: float, duration_days: int = 180) -> Dict:
        mission = self.MISSION_DATA.get(destination, self.MISSION_DATA["Deep Space"])
        helio = ssn / 150
        gcr = 1 + (1 - min(helio, 1)) * 0.8
        daily = mission["radiation_mSv_day"] * (0.3 if mission["magnetic_shield"] else 1.0) * gcr
        total = daily * duration_days
        risk = "CRÍTICO" if total>1000 else ("ALTO" if total>500 else ("MODERADO" if total>100 else "BAJO"))
        return {"destination":destination,"daily_mSv":round(daily,2),"total_mSv":round(total,1),"risk":risk,"heliosphere_protection":round(helio*100,1),"timestamp":datetime.now().isoformat()}
    
    def predict_crew_health(self, destination: str, crew_size: int = 6, ssn: float = 120) -> Dict:
        rad = self.calculate_radiation_exposure(destination, ssn)
        effects = []
        if rad["total_mSv"] > 100: effects.append("Riesgo de cataratas radio-inducidas")
        if rad["total_mSv"] > 200: effects.append("Aumento 3% riesgo cáncer (NASA)")
        if not self.MISSION_DATA[destination]["magnetic_shield"]: effects.append("Alteración circadiana por falta de campo magnético")
        alert = "CRÍTICO" if rad["total_mSv"]>500 else ("ALTO" if rad["total_mSv"]>200 else "MODERADO")
        return {"crew_size":crew_size,"destination":destination,"effects":effects,"bio_alert":alert,"countermeasures":["Blindaje con agua 10cm","Monitoreo biomarcadores"],"chizhevsky_note":"Sin campo magnético, la heliobiología es crucial","timestamp":datetime.now().isoformat()}

class GalacticCosmicRaySimulator:
    def simulate_gcr_flux(self, ssn: float, solar_wind_speed: float = 400) -> Dict:
        strength = ssn/100 + solar_wind_speed/400
        gcr = 4.0 / max(strength, 0.1)
        impact = "ALTO - Daño ADN" if gcr>8 else ("MODERADO" if gcr>5 else "BAJO")
        return {"gcr_flux":round(gcr,2),"heliosphere_strength":round(strength,2),"biological_impact":impact,"chizhevsky_note":"La heliosfera es nuestro escudo","timestamp":datetime.now().isoformat()}

class ExoplanetHabitability:
    def assess_habitability(self, star_type: str, orbital_distance_au: float, magnetic_field: bool = False, ssn_equivalent: float = 100) -> Dict:
        stars = {"G":1.0,"K":1.2,"M":0.4,"F":0.8}
        sf = stars.get(star_type,0.5)
        df = 1.0/orbital_distance_au if orbital_distance_au>0 else 0
        mf = 3.0 if magnetic_field else 0.3
        h = sf * df * mf * (ssn_equivalent/100)
        rating = "EXCELENTE" if h>2.0 else ("BUENO" if h>1.0 else ("MARGINAL" if h>0.5 else "INHÓSPITO"))
        return {"star_type":star_type,"habitability_index":round(h,2),"rating":rating,"magnetic_field":magnetic_field,"chizhevsky_principle":"Sin campo magnético no hay protección. La heliobiología es universal.","timestamp":datetime.now().isoformat()}
