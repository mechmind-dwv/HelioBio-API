Como un arquitecto de software y seguidor de la visión de Chizhevsky, entiendo que la ciencia es inútil si no es accesible. Una documentación clara es nuestro puente hacia la comunidad, permitiendo que otros investigadores, desarrolladores y curiosos puedan usar y construir sobre nuestra API. Aquí está la documentación técnica para **HelioBio-API**, diseñada para ser clara, completa y fácil de navegar.

-----

### **HelioBio-API: Documentación de la API**

#### **Introducción**

La HelioBio-API es una interfaz RESTful que proporciona acceso a datos solares, información sobre eventos biológicos, y resultados de análisis heliobiológicos. Permite a los usuarios consultar datos históricos, obtener información en tiempo real y realizar análisis avanzados de correlación entre la actividad solar y fenómenos biológicos.

La API sigue los principios de la arquitectura REST. Todos los *endpoints* devuelven respuestas en formato **JSON**.

-----

### **Endpoints**

#### **1. Endpoints de Datos Solares**

##### `GET /solar/data/`

Este *endpoint* recupera datos históricos y recientes de la actividad solar, combinando información de SILSO y NOAA.

  * **Descripción:** Obtiene un conjunto de datos completos de actividad solar, incluyendo el número de manchas solares (SSN), el flujo solar (F10.7) y la fase del ciclo solar.
  * **Parámetros de Consulta:**
      * `years_back` (opcional, entero): El número de años de datos históricos a recuperar. Por defecto es 5.
  * **Ejemplo de Respuesta (JSON):**
    ```json
    [
      {
        "date": "2024-01-01T00:00:00",
        "sunspot_number": 120.5,
        "solar_flux_10_7": 150.2,
        "cycle_phase": "MAXIMUM",
        "data_source": "NOAA_SWPC"
      },
      {
        "date": "2024-02-01T00:00:00",
        "sunspot_number": 135.1,
        "solar_flux_10_7": 160.8,
        "cycle_phase": "MAXIMUM",
        "data_source": "SILSO"
      }
    ]
    ```

-----

#### **2. Endpoints de Análisis**

##### `GET /analysis/correlation/`

Calcula la correlación entre una métrica solar y una métrica biológica.

  * **Descripción:** Realiza un análisis de correlación con un método estadístico especificado y devuelve el coeficiente de correlación, el p-valor y la significancia.
  * **Parámetros de Consulta:**
      * `solar_metric` (requerido, cadena): La métrica solar a analizar (`ssn`, `f10_7`).
      * `biological_metric` (requerido, cadena): La métrica biológica (`death_count`, `case_count`, `event_severity`).
      * `method` (opcional, cadena): El método de correlación a usar (`pearson`, `spearman`, `cross_correlation`). Por defecto es `cross_correlation`.
  * **Ejemplo de Respuesta (JSON):**
    ```json
    {
      "method": "cross_correlation",
      "correlation_coefficient": 0.65,
      "p_value": 0.001,
      "lag_days": 14,
      "strength_interpretation": "moderate positive correlation",
      "statistical_significance": true
    }
    ```

##### `GET /analysis/cycle/`

Identifica el ciclo dominante en una serie de datos solares o biológicos.

  * **Descripción:** Utiliza análisis de series de tiempo para encontrar periodos recurrentes en los datos.
  * **Parámetros de Consulta:**
      * `metric` (requerido, cadena): La métrica a analizar (`ssn`, `death_count`).
  * **Ejemplo de Respuesta (JSON):**
    ```json
    {
      "dominant_period_years": 11.2,
      "confidence_level": 0.95,
      "secondary_periods": [3.5, 27.0],
      "method_used": "fourier"
    }
    ```

-----

#### **3. Endpoints de Predicción**

##### `GET /predictions/solar/`

Proporciona una predicción a corto y medio plazo de la actividad solar.

  * **Descripción:** Utiliza un modelo de *machine learning* entrenado con datos históricos para predecir futuros valores de SSN.
  * **Parámetros de Consulta:**
      * `forecast_months` (opcional, entero): El número de meses a pronosticar. Por defecto es 24.
  * **Ejemplo de Respuesta (JSON):**
    ```json
    {
      "forecast_date": "2025-09-04T06:12:35",
      "predicted_ssn_values": [
        { "date": "2025-10-01", "ssn": 145.2 },
        { "date": "2025-11-01", "ssn": 148.1 }
      ],
      "model": "RandomForestRegressor"
    }
    ```

-----

### **Códigos de Estado HTTP**

  * `200 OK`: La solicitud fue exitosa.
  * `400 Bad Request`: Parámetros de consulta no válidos.
  * `404 Not Found`: El recurso solicitado no existe.
  * `500 Internal Server Error`: Un error en el servidor impidió completar la solicitud.

Esta documentación es un mapa para aquellos que deseen explorar el vasto y fascinante campo de la heliobiología. ¡Que la ciencia nos guíe\!
