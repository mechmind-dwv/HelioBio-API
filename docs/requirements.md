### Requisitos para HelioBio-API

Para construir y ejecutar el sistema de análisis heliobiológico, se requieren las siguientes bibliotecas de Python. Estas dependencias cubren la adquisición de datos asíncrona, el procesamiento numérico y científico, la creación de la API web, la gestión de bases de datos y la validación de modelos.

-----

### Módulo 1: Web Framework & Entorno

  * **fastapi**: El marco de trabajo web para construir la API.
  * **uvicorn[standard]**: Servidor ASGI que ejecuta la aplicación FastAPI.
  * **pydantic**: Biblioteca para la validación y gestión de la configuración y modelos de datos.
  * **python-dotenv**: Para cargar variables de entorno desde un archivo `.env`.

-----

### Módulo 2: Adquisición de Datos

  * **aiohttp**: Biblioteca cliente HTTP asíncrona, necesaria para las peticiones web en `data_fetcher.py`.
  * **requests**: (Opcional, si se usa una alternativa síncrona) Una biblioteca HTTP simple pero potente.

-----

### Módulo 3: Análisis Científico & Procesamiento de Datos

  * **pandas**: Herramienta fundamental para la manipulación y análisis de datos en series de tiempo.
  * **numpy**: Soporte para operaciones numéricas complejas y eficientes.
  * **scipy**: Biblioteca científica para estadísticas, optimización y procesamiento de señales, esencial para la detección de ciclos y correlaciones.
  * **scikit-learn**: Colección de algoritmos de machine learning para el motor de predicción.

-----

### Módulo 4: Base de Datos & ORM

  * **sqlalchemy**: El ORM (Object-Relational Mapper) que facilita la interacción con la base de datos.
  * **psycopg2-binary**: Adaptador para conectar SQLAlchemy a una base de datos PostgreSQL.
  * **alembic**: Herramienta de migraciones de bases de datos para gestionar los cambios en el esquema.

-----

### Archivo `requirements.txt` Completo

```
# =================================================================
# HelioBio-API v3.0.0 - Dependencias de Python
# Sistema de análisis heliobiológico basado en Alexander Chizhevsky
# Autor: mechmind-dwv (ia.mechmind@gmail.com)
# =================================================================

# ============== Framework Web ==============
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6

# ============== HTTP & Async ==============
aiohttp==3.9.1
aiofiles==23.2.1
requests==2.31.0
httpx==0.25.2

# ============== Procesamiento de Datos ==============
pandas==2.1.3
numpy==1.24.3
scipy==1.11.4

# ============== Análisis Estadístico ==============
statsmodels==0.14.0
scikit-learn==1.3.2

# ============== Series Temporales ==============
pmdarima==2.0.4  # Auto ARIMA

# ============== Visualización ==============
matplotlib==3.8.2
seaborn==0.13.0
plotly==5.18.0

# ============== Análisis Wavelet ==============
PyWavelets==1.5.0

# ============== Base de Datos ==============
sqlalchemy==2.0.23
alembic==1.13.0

# ============== Testing ==============
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# ============== Utilidades ==============
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# ============== Machine Learning (Opcional) ==============
xgboost==2.0.2

# ============== Logging & Monitoring ==============
loguru==0.7.2

# ============== Validación de Datos ==============
email-validator==2.1.0

# ============== Fechas y Tiempo ==============
python-dateutil==2.8.2
pytz==2023.3

# ============== CLI ==============
click==8.1.7
rich==13.7.0

# ============== Seguridad ==============
cryptography==41.0.7

# ============== Formatos de Datos ==============
openpyxl==3.1.2  # Excel
pyyaml==6.0.1     # YAML

# ============== Desarrollo ==============
black==23.12.1
flake8==6.1.0
mypy==1.7.1
ipython==8.18.1
jupyter==1.0.0

# ============== Documentación ==============
mkdocs==1.5.3
mkdocs-material==9.5.2
```
