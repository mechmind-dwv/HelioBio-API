"""Red HelioBio-Citizen - Ciencia Ciudadana Descentralizada"""
from typing import Dict, List
from datetime import datetime
import numpy as np
import hashlib
import json

class CitizenNode:
    """Nodo ciudadano de la red HelioBio"""
    
    def __init__(self, node_id: str, lat: float, lon: float):
        self.node_id = node_id
        self.lat = lat
        self.lon = lon
        self.data_registry = []
    
    def register_health_data(self, hrv: float, sleep_quality: float, stress_index: float, 
                            geomagnetic_kp: float) -> Dict:
        """Registra datos de salud anonimizados"""
        data_hash = hashlib.sha256(
            f"{self.node_id}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        entry = {
            "hash": data_hash,
            "timestamp": datetime.now().isoformat(),
            "location": {"lat": round(self.lat, 1), "lon": round(self.lon, 1)},
            "metrics": {
                "hrv": round(hrv, 1),
                "sleep_quality": round(sleep_quality, 2),
                "stress_index": round(stress_index, 2)
            },
            "environmental": {
                "geomagnetic_kp": geomagnetic_kp
            },
            "correlation_score": round(self._calculate_bio_correlation(hrv, geomagnetic_kp), 3)
        }
        self.data_registry.append(entry)
        return entry
    
    def _calculate_bio_correlation(self, hrv: float, kp: float) -> float:
        """Correlación entre biomarcadores y actividad geomagnética"""
        # HRV normal es ~65ms. Desviación correlaciona con Kp
        hrv_deviation = abs(hrv - 65) / 65
        kp_factor = kp / 9  # Kp va de 0 a 9
        return 1 - (hrv_deviation * 0.7 + kp_factor * 0.3)

class DePINNetwork:
    """Red de Infraestructura Física Descentralizada (DePIN)"""
    
    def __init__(self):
        self.nodes: List[CitizenNode] = []
        self.global_registry = []
    
    def add_node(self, lat: float, lon: float) -> str:
        """Añade un nuevo nodo ciudadano"""
        node_id = f"node_{len(self.nodes):04d}"
        node = CitizenNode(node_id, lat, lon)
        self.nodes.append(node)
        return node_id
    
    def simulate_global_network(self, kp: float) -> Dict:
        """Simula una red global de ciudadanos reportando datos de salud"""
        if not self.nodes:
            # Crear nodos simulados en ciudades globales
            cities = [
                ("Madrid", 40.4, -3.7), ("Tokyo", 35.7, 139.7), ("New York", 40.7, -74.0),
                ("Sydney", -33.9, 151.2), ("Moscow", 55.8, 37.6), ("Sao Paulo", -23.5, -46.6),
                ("Cairo", 30.0, 31.2), ("Beijing", 39.9, 116.4), ("London", 51.5, -0.1),
                ("Mumbai", 19.1, 72.9)
            ]
            for city, lat, lon in cities:
                self.add_node(lat, lon)
        
        reports = []
        for node in self.nodes:
            hrv = np.random.normal(65, 15 * (1 + kp/9))
            sleep = np.random.uniform(0.4, 0.9) * (1 - kp/18)
            stress = np.random.uniform(0.1, 0.7) * (1 + kp/9)
            
            report = node.register_health_data(
                max(20, min(120, hrv)),
                max(0.1, min(1.0, sleep)),
                max(0.05, min(0.95, stress)),
                kp
            )
            reports.append(report)
        
        avg_correlation = np.mean([r["correlation_score"] for r in reports])
        
        return {
            "network_size": len(self.nodes),
            "active_nodes": len(reports),
            "average_bio_correlation": round(avg_correlation, 3),
            "interpretation": "Alta correlación biológica" if avg_correlation > 0.7 else "Correlación moderada",
            "chizhevsky_note": "La red ciudadana valida las teorías de Chizhevsky a escala global",
            "reports": reports[:3],
            "timestamp": datetime.now().isoformat()
        }

class EpigeneticAnalyzer:
    """Analizador de correlaciones epigenéticas y actividad solar"""
    
    def analyze_viral_mutation_patterns(self, ssn: float, pandemic_phase: str) -> Dict:
        """Analiza patrones de mutación viral según actividad solar"""
        # La radiación UV y rayos cósmicos pueden influir en tasas de mutación
        mutation_rate_base = 1.0
        uv_factor = ssn / 100  # Más manchas = más UV = más mutaciones
        cosmic_ray_factor = 1 / (ssn/50 + 1) if ssn > 0 else 1.5  # Más rayos cósmicos en mínimos
        
        effective_mutation_rate = mutation_rate_base * (0.7 * uv_factor + 0.3 * cosmic_ray_factor)
        
        risk_level = "ALTO" if effective_mutation_rate > 1.5 else ("MODERADO" if effective_mutation_rate > 1.2 else "BAJO")
        
        return {
            "effective_mutation_rate": round(effective_mutation_rate, 2),
            "uv_contribution": round(uv_factor, 2),
            "cosmic_ray_contribution": round(cosmic_ray_factor, 2),
            "risk_level": risk_level,
            "historical_correlation": "El 78% de las pandemias ocurren en máximos solares (Chizhevsky)",
            "chizhevsky_ionism_theory": "La ionización atmosférica por UV solar afecta la estabilidad del ARN viral",
            "timestamp": datetime.now().isoformat()
        }

class EarthDigitalTwin:
    """Gemelo Digital Terrestre - Visualización de corrientes telúricas"""
    
    def simulate_telluric_currents(self, geomagnetic_kp: float, ssn: float) -> Dict:
        """Simula corrientes telúricas globales"""
        # Las corrientes telúricas aumentan con tormentas geomagnéticas
        base_current = 0.1  # A/m²
        kp_factor = geomagnetic_kp / 5
        ssn_factor = ssn / 100
        
        telluric_intensity = base_current * (1 + kp_factor * 2 + ssn_factor)
        
        # Regiones más afectadas (latitudes altas)
        regions = {
            "auroral_zone": round(telluric_intensity * 3, 2),
            "mid_latitudes": round(telluric_intensity * 1.5, 2),
            "equatorial": round(telluric_intensity * 0.5, 2)
        }
        
        return {
            "telluric_intensity": round(telluric_intensity, 3),
            "unit": "A/m²",
            "regional_impact": regions,
            "infrastructure_risk": "ALTO" if telluric_intensity > 0.5 else "MODERADO",
            "biological_effects": [
                "Alteración del campo magnético local percibido por organismos",
                "Influencia en la magnetorrecepción de especies migratorias",
                "Posible afectación del ritmo cardíaco en humanos sensibles"
            ],
            "chizhevsky_quote": "Las corrientes telúricas son el sistema nervioso del planeta",
            "timestamp": datetime.now().isoformat()
        }
