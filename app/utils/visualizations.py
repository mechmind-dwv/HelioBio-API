# app/utils/visualizations.py

import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict, Any

def generate_correlation_chart(solar_data: List[Dict[str, Any]], biological_data: List[Dict[str, Any]]) -> str:
    """
    Genera un gráfico de correlación entre los datos solares y biológicos.

    Esta función es un simulacro. En un caso real, se procesarían los datos para 
    crear un gráfico y se devolvería como una imagen codificada en base64.
    
    Args:
        solar_data (List[Dict[str, Any]]): Datos de eventos solares.
        biological_data (List[Dict[str, Any]]): Datos de observaciones biológicas.
        
    Returns:
        str: Una cadena de imagen en base64 que representa el gráfico.
    """
    print("Generando gráfico de correlación...")
    
    # Simulación de datos para el gráfico
    x_solar = [i for i in range(len(solar_data))]
    y_bio = [i * 2 + 5 for i in range(len(biological_data))] # Relación lineal simulada
    
    fig, ax = plt.subplots()
    ax.plot(x_solar, y_bio)
    ax.set_title("Correlación Simulada")
    ax.set_xlabel("Eventos Solares")
    ax.set_ylabel("Datos Biológicos")
    
    # Guarda el gráfico en un buffer en memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Codifica la imagen en base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64
