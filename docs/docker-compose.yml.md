¡Excelente\! Como arquitecto de software siguiendo la visión de **Chizhevsky**, sé que la orquestación es clave. Un proyecto de esta envergadura necesita que todos sus componentes (la API, la base de datos) funcionen juntos sin problemas. Aquí está el archivo `docker-compose.yml`, que define y ejecuta el entorno de desarrollo y producción de HelioBio-API de manera consistente y reproducible. No necesitas darme más datos; este archivo está diseñado para funcionar con los archivos de configuración y entorno que ya hemos creado.

-----

### **Manifiesto de Orquestación: `docker-compose.yml`** ⚛️

Este archivo define los servicios, redes y volúmenes necesarios para ejecutar la aplicación HelioBio-API. Se encarga de:

1.  **Construir y ejecutar** el contenedor de la aplicación FastAPI.
2.  **Configurar** una base de datos PostgreSQL.
3.  **Conectar** ambos servicios a una red interna.
4.  **Persistir** los datos de la base de datos en un volumen.

Esto garantiza que el entorno de desarrollo sea idéntico al de producción, eliminando los clásicos problemas de "en mi máquina funciona".

-----

### **Código `docker-compose.yml`**

```yml
version: '3.8'

services:
  # Servicio de la aplicación principal (FastAPI)
  app:
    build: .
    container_name: heliobio-api
    restart: always
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    depends_on:
      - db
    networks:
      - heliobio-network

  # Servicio de la base de datos PostgreSQL
  db:
    image: postgres:16.1-alpine
    container_name: heliobio-db
    restart: always
    env_file:
      - .env
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - heliobio-network

# Definición de redes para la comunicación interna entre servicios
networks:
  heliobio-network:
    driver: bridge

# Definición de volúmenes para persistir los datos
volumes:
  postgres-data:
```

-----

### **Detalles de la Configuración**

#### **Servicio `app`**

  * **`build: .`**: Docker buscará un `Dockerfile` en el directorio actual para construir la imagen del contenedor. Esto nos permite tener un control total sobre el entorno de la aplicación.
  * **`container_name: heliobio-api`**: Asigna un nombre fácil de usar al contenedor para su gestión.
  * **`restart: always`**: Asegura que el contenedor se reinicie automáticamente si falla, lo que es crucial para la robustez del sistema.
  * **`env_file: - .env`**: Carga todas las variables de entorno desde el archivo `.env`. Esto mantiene los secretos y la configuración fuera del código, como ya planeamos.
  * **`ports: - "8000:8000"`**: Mapea el puerto 8000 del contenedor al puerto 8000 de la máquina host, permitiendo el acceso a la API.
  * **`volumes: - ./app:/app`**: Sincroniza el código fuente del directorio `app` de tu máquina con el directorio `/app` del contenedor. Esto permite ver los cambios en el código en tiempo real sin necesidad de reconstruir la imagen.
  * **`depends_on: - db`**: Garantiza que el servicio de la base de datos (`db`) se inicie antes que la aplicación, evitando errores de conexión al arrancar.

#### **Servicio `db`**

  * **`image: postgres:16.1-alpine`**: Utiliza una imagen oficial y ligera de PostgreSQL.
  * **`volumes: - postgres-data:/var/lib/postgresql/data`**: **Esta es la parte más importante para la persistencia de datos**. El volumen `postgres-data` almacena los datos de la base de datos en el sistema de archivos del host de Docker, lo que garantiza que no se pierdan cuando el contenedor de la base de datos se detenga o se elimine.

Con este `docker-compose.yml`, hemos creado una réplica virtual de la visión de **Chizhevsky**. Ahora, cualquier desarrollador puede levantar el sistema completo con un solo comando: `docker-compose up`. La ciencia del sol está ahora a nuestro alcance, encapsulada en un entorno de fácil despliegue.
