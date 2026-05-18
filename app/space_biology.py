"""Biología Espacial - Adaptación Heliobiológica a entornos extraterrestres"""
import numpy as np
from typing import Dict, List
from datetime import datetime

class SpaceColonySimulator:
    """Simulador de colonia espacial y exposición a radiación cósmica"""
    
    # Datos de referencia de misiones espaciales reales
    MISSION_DATA = {
        "ISS": {"altitude_km": 408, "radiation_mSv_day": 0.5, "magnetic_shield": True},
        "Moon": {"altitude_km": 384400, "radiation_mSv_day": 1.5, "magnetic_shield": False},
        "Mars": {"altitude_km": 225000000, "radiation_mSv_day": 1.8, "magnetic_shield": False},
        "Deep Space": {"altitude_km": float('inf'), "radiation_mSv_day": 2.5, "magnetic_shield": False},
    }
    
    def calculate_radiation_exposure(self, destination: str, ssn: float, duration_days: int = 180) -> Dict:
        """Calcula exposición a radiación en misiones espaciales"""
        mission = self.MISSION_DATA.get(destination, self.MISSION_DATA["Deep Space"])
        
        # La radiación aumenta en mínimos solares (menos protección de la heliosfera)
        heliosphere_protection = ssn / 150  # Normalizado
        base_radiation = mission["radiation_mSv_day"]
        
        # Sin campo magnético terrestre, la exposición es mayor
        magnetic_factor = 0.3 if mission["magnetic_shield"] else 1.0
        
        # Radiación cósmica galáctica (GCR) - mayor en mínimos solares
        gcr_factor = 1 + (1 - min(heliosphere_protection, 1)) * 0.8
        
        daily_dose = base_radiation * magnetic_factor * gcr_factor
        total_dose = daily_dose * duration_days
        
        # Evaluación de riesgo según NASA
        if total_dose > 1000:
            risk = "CRÍTICO - Supera límites de seguridad NASA (>1000 mSv)"
        elif total_dose > 500:
            risk = "ALTO - Requiere blindaje adicional"
        elif total_dose > 100:
            risk = "MODERADO - Monitoreo continuo requerido"
        else:
            risk = "BAJO - Dentro de límites seguros"
        
        return {
            "destination": destination,
            "mission_duration_days": duration_days,
            "daily_radiation_mSv": round(daily_dose, 2),
            "total_radiation_mSv": round(total_dose, 1),
            "risk_level": risk,
            "heliosphere_protection": round(heliosphere_protection * 100, 1),
            "solar_cycle_phase": "Máximo" if ssn > 100 else ("Moderado" if ssn > 50 else "Mínimo"),
            "recommendation": "Viajar durante máximo solar para mayor protección de la heliosfera" if ssn > 100 else "Precaución: mínimo solar, mayor exposición a GCR",
            "timestamp": datetime.now().isoformat()
        }
    
    def predict_crew_health(self, destination: str, crew_size: int = 6, ssn: float = 120) -> Dict:
        """Predice efectos en la salud de la tripulación"""
        radiation = self.calculate_radiation_exposure(destination, ssn)
        
        # Efectos biológicos documentados en astronautas
        effects = []
        if radiation["total_radiation_mSv"] > 100:
            effects.append("Riesgo elevado de cataratas radio-inducidas")
            effects.append("Posible daño al sistema nervioso central")
        if radiation["total_radiation_mSv"] > 200:
            effects.append("Aumento del 3% en riesgo de cáncer a largo plazo (NASA)") 
            effects.append("Degradación potencial del microbioma intestinal")
        if not self.MISSION_DATA[destination]["magnetic_shield"]:
            effects.append("Alteración del ritmo circadiano por ausencia de campo magnético")
            effects.append("Posible desorientación magneto-receptiva")
        
        # Sistema de alerta biológica
        bio_alert = "CRÍTICO" if radiation["total_radiation_mSv"] > 500 else ("ALTO" if radiation["total_radiation_mSv"] > 200 else "MODERADO")
        
        return {
            "crew_size": crew_size,
            "destination": destination,
            "predicted_effects": effects,
            "bio_alert_level": bio_alert,
            "chizhevsky_space_note": "Sin la protección del campo magnético terrestre, la heliobiología es crucial para la supervivencia",
            "countermeasures": [
                "Blindaje con agua o polietileno (10cm reducen 50% radiación)",
                "Fármacos radioprotectores (amifostina)",
                "Monitoreo continuo de biomarcadores de radiación",
                "Selección genética de astronautas con mayor resistencia a radiación"
            ],
            "timestamp": datetime.now().isoformat()
        }

class GalacticCosmicRaySimulator:
    """Simulador de Rayos Cósmicos Galácticos (GCR)"""
    
    def simulate_gcr_flux(self, ssn: float, solar_wind_speed: float = 400) -> Dict:
        """Simula el flujo de GCR según actividad solar"""
        # Los GCR aumentan en mínimos solares (la heliosfera se debilita)
        base_gcr = 4.0  # partículas/cm²/s
        heliosphere_strength = ssn / 100 + solar_wind_speed / 400
        gcr_flux = base_gcr / max(heliosphere_strength, 0.1)
        
        # Efectos biológicos
        if gcr_flux > 8:
            bio_impact = "ALTO - Daño significativo al ADN por ionización"
            shielding_needed = "20 cm de agua o 15 cm de polietileno"
        elif gcr_flux > 5:
            bio_impact = "MODERADO - Estrés oxidativo celular aumentado"
            shielding_needed = "10 cm de agua"
        else:
            bio_impact = "BAJO - Condiciones normales de radiación"
            shielding_needed = "Blindaje estándar suficiente"
        
        return {
            "gcr_flux_particles_cm2_s": round(gcr_flux, 2),
            "heliosphere_strength": round(heliosphere_strength, 2),
            "biological_impact": bio_impact,
            "recommended_shielding": shielding_needed,
            "ionization_potential": "ALTO - Riesgo de rotura de doble cadena de ADN" if gcr_flux > 6 else "MODERADO",
            "chizhevsky_cosmic_note": "La heliosfera es nuestro escudo. En el espacio profundo, estamos desnudos ante el cosmos",
            "timestamp": datetime.now().isoformat()
        }

class ExoplanetHabitability:
    """Evaluador de habitabilidad para exoplanetas"""
    
    def assess_habitability(self, star_type: str, orbital_distance_au: float, 
                           magnetic_field: bool = False, ssn_equivalent: float = 100) -> Dict:
        """Evalúa habitabilidad de exoplanetas basado en heliobiología"""
        
        # Factor estelar
        star_factors = {
            "G": 1.0,    # Como el Sol
            "K": 1.2,    # Más estable, mejor para la vida
            "M": 0.4,    # Enanas rojas: llamaradas frecuentes
            "F": 0.8,    # Más UV, vida más difícil
        }
        star_factor = star_factors.get(star_type, 0.5)
        
        # Factor de distancia orbital (zona habitable = 1.0)
        distance_factor = 1.0 / orbital_distance_au if orbital_distance_au > 0 else 0
        
        # Factor de campo magnético (esencial para la vida)
        magnetic_factor = 3.0 if magnetic_field else 0.3
        
        # Índice de habitabilidad heliobiológica
        habitability = star_factor * distance_factor * magnetic_factor * (ssn_equivalent / 100)
        
        if habitability > 2.0:
            rating = "EXCELENTE - Condiciones óptimas para vida compleja"
        elif habitability > 1.0:
            rating = "BUENO - Vida microbiana probable, vida compleja posible"
        elif habitability > 0.5:
            rating = "MARGINAL - Solo extremófilos sobrevivirían"
        else:
            rating = "INHÓSPITO - Condiciones incompatibles con la vida"
        
        return {
            "star_type": star_type,
            "orbital_distance_au": orbital_distance_au,
            "magnetic_field": magnetic_field,
            "habitability_index": round(habitability, 2),
            "rating": rating,
            "chizhevsky_principle": "Sin campo magnético, no hay protección contra la radiación estelar. La heliobiología es universal.",
            "potential_for_life": "ALTO" if habitability > 1.5 else ("MODERADO" if habitability > 0.8 else "BAJO"),
            "timestamp": datetime.now().isoformat()
        }
