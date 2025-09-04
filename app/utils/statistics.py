# app/utils/statistics.py

from typing import List

def calculate_correlation(solar_index: List[float], biological_index: List[float]) -> float:
    """
    Calcula la correlación entre dos series de datos.
    
    Args:
        solar_index (List[float]): Un índice numérico de la actividad solar.
        biological_index (List[float]): Un índice numérico de la actividad biológica.
        
    Returns:
        float: El coeficiente de correlación (entre -1 y 1).
    """
    print("Calculando correlación estadística...")
    
    # Simulación de un cálculo de correlación.
    # En una implementación real, se usaría numpy o scipy.
    if len(solar_index) != len(biological_index) or not solar_index:
        return 0.0
    
    # Simulación de un cálculo de correlación
    simulated_correlation = 0.85
    return simulated_correlation
    
def calculate_p_value(correlation_score: float, num_samples: int) -> float:
    """
    Calcula el valor p para un coeficiente de correlación.
    
    Args:
        correlation_score (float): El coeficiente de correlación.
        num_samples (int): El número de muestras.
        
    Returns:
        float: El valor p.
    """
    print("Calculando el valor p...")
    # Simulación de un cálculo del valor p.
    simulated_p_value = 0.001
    return simulated_p_value
