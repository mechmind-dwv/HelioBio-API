## **HelioBio-API: Sistema Heliobiológico Avanzado** ⚛️

### Visión del Proyecto

HelioBio-API es un sistema modular y escalable diseñado para investigar, analizar y predecir la relación entre la **actividad solar** (manchas solares, viento solar, eventos geomagnéticos) y los **fenómenos biológicos** y epidemiológicos en la Tierra. Utilizando fuentes de datos oficiales y técnicas de análisis de datos de vanguardia, nuestro objetivo es:

1.  **Recopilar** de manera confiable datos heliofísicos y biológicos históricos y en tiempo real.
2.  **Analizar** la correlación y las periodicidades entre ambas series de tiempo, identificando posibles relaciones de causa y efecto.
3.  **Validar** las teorías de Chizhevsky con un enfoque moderno y riguroso.
4.  **Generar predicciones** y alertas tempranas para instituciones de salud y organismos de investigación.
5.  **Democratizar la ciencia** poniendo los datos y las herramientas de análisis a disposición de la comunidad global.

### Arquitectura del Sistema

El sistema se basa en una arquitectura de microservicios con un enfoque modular, lo que garantiza robustez, escalabilidad y facilidad de mantenimiento.

  * **Módulo 1: `app/config`** ⚙️

      * **Propósito:** Gestión centralizada de configuraciones y secretos.
      * **Tecnologías:** Pydantic para la validación de configuraciones.
      * **Componentes Clave:** `settings.py` (cargas desde `.env`) y `database.py`.

  * **Módulo 2: `app/models`** 🧠

      * **Propósito:** Define los modelos de datos para asegurar la integridad y la estructura de la información.
      * **Tecnologías:** Pydantic.
      * **Componentes Clave:** `solar.py` (modelos de actividad solar), `biological.py` (modelos de eventos biológicos) y `analysis.py` (modelos para resultados de análisis).

  * **Módulo 3: `app/core`** 🔬

      * **Propósito:** Contiene el corazón de la lógica de negocio y los algoritmos científicos.
      * **Tecnologías:** `aiohttp` (asincronía), Pandas, NumPy, Scipy, scikit-learn (análisis y machine learning).
      * **Componentes Clave:**
          * `data_fetcher.py`: **Adquisición de datos**. Un recolector asíncrono con caché inteligente para fuentes como SILSO y NOAA.
          * `analyzer.py`: **Análisis avanzado**. Módulo para correlación, detección de ciclos y validación de hipótesis, incluyendo las teorías de Chizhevsky.
          * `predictor.py`: **Motor de predicción**. Utiliza modelos de series de tiempo para pronosticar picos de actividad solar y posibles eventos biológicos.
          * `alert_system.py`: **Sistema de alertas**. Basado en umbrales y predicciones, genera notificaciones para eventos críticos.

  * **Módulo 4: `app/database`** 💾

      * **Propósito:** Capa de acceso a datos que abstrae la complejidad de la base de datos.
      * **Tecnologías:** SQLAlchemy, PostgreSQL.
      * **Componentes Clave:** `connection.py` y `repositories/` (repositorios para manejar las operaciones CRUD).

  * **Módulo 5: `app/services`** 🤝

      * **Propósito:** Lógica de negocio de alto nivel que orquesta las interacciones entre los módulos `core` y `database`.
      * **Componentes Clave:** `solar_service.py` y `analysis_service.py`.

  * **Módulo 6: `app/api`** 🌐

      * **Propósito:** Proporciona los *endpoints* de la API para que otras aplicaciones puedan consumir los datos y análisis.
      * **Tecnologías:** FastAPI.
      * **Componentes Clave:** `main.py` (punto de entrada) y `endpoints/` (rutas para datos solares, biológicos, análisis, etc.).

-----

### Cómo Empezar

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/mechmind-dwv/HelioBio-API.git
    cd HelioBio-API
    ```
2.  **Configurar el entorno:**
      * Crea un archivo `.env` a partir de `.env.example`.
      * Configura las variables de entorno necesarias (base de datos, etc.).
3.  **Ejecutar con Docker Compose:**
    ```bash
    docker-compose up --build
    ```
4.  **Acceder a la API:**
      * La documentación interactiva estará disponible en `http://localhost:8000/docs`.

### Contribuciones

Este es un proyecto impulsado por la ciencia y la convicción. Buscamos colaboradores en las áreas de:

  * **Científicos de datos:** Para mejorar los modelos de predicción y análisis.
  * **Ingenieros de software:** Para optimizar el rendimiento y la arquitectura.
  * **Investigadores en heliobiología:** Para validar los hallazgos y proponer nuevas hipótesis.

Juntos, podemos honrar el legado de Chizhevsky y usar la ciencia para ayudar a salvar vidas.
