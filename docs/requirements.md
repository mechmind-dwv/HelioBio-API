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
# Módulo 1: Web Framework & Entorno
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic==2.7.1
python-dotenv==1.0.1

# Módulo 2: Adquisición de Datos
aiohttp==3.9.5

# Módulo 3: Análisis Científico & Procesamiento de Datos
pandas==2.2.2
numpy==1.26.4
scipy==1.13.0
scikit-learn==1.4.2

# Módulo 4: Base de Datos & ORM
sqlalchemy==2.0.29
psycopg2-binary==2.9.9
alembic==1.13.1

# Herramientas de Desarrollo (Opcional, para pruebas y formateo)
pytest==8.2.0
black==24.4.2
flake8==7.0.0
```
