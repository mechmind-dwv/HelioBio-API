Como arquitecto de software y fan de la visión de Chizhevsky, sé que un gran proyecto es inútil si no puede ser replicado. Una guía de instalación clara es nuestro mapa para que otros exploradores se unan a nuestra misión. Aquí está la guía de instalación para **HelioBio-API**, escrita para ser directa y fácil de seguir. ¡La ciencia debe ser accesible para todos\!

-----

### **HelioBio-API: Guía de Instalación** ⚛️

Esta guía te proporcionará los pasos para configurar y ejecutar el proyecto HelioBio-API en tu entorno local. Recomendamos encarecidamente el uso de **Docker Compose** para un despliegue rápido y sin complicaciones.

-----

### **Requisitos Previos**

Asegúrate de tener instalado lo siguiente en tu sistema:

  * **Git**: Para clonar el repositorio del proyecto.
  * **Docker y Docker Compose**: La forma más sencilla de ejecutar la aplicación, la base de datos y todas sus dependencias de manera consistente.
      * Puedes descargar Docker Desktop, que incluye ambos: [Docker Desktop](https://www.docker.com/products/docker-desktop/)

-----

### **Paso 1: Clonar el Repositorio**

Abre tu terminal o símbolo del sistema y ejecuta el siguiente comando para clonar el repositorio del proyecto:

```bash
git clone https://github.com/mechmind-dwv/HelioBio-API.git
cd HelioBio-API
```

-----

### **Paso 2: Configurar las Variables de Entorno**

El proyecto utiliza un archivo `.env` para manejar las configuraciones sensibles, como las credenciales de la base de datos y las claves secretas.

1.  Copia el archivo de ejemplo proporcionado:

    ```bash
    cp .env.example .env
    ```

2.  Abre el nuevo archivo `.env` en tu editor de texto favorito.

3.  Edita los valores según sea necesario. Para el despliegue local, los valores predeterminados en `.env.example` son suficientes, pero asegúrate de que la `SECRET_KEY` sea una cadena de caracteres aleatoria y segura.

-----

### **Paso 3: Construir y Ejecutar los Contenedores con Docker Compose**

Ahora que el entorno está configurado, puedes usar Docker Compose para construir y lanzar la aplicación y la base de datos. Este proceso puede tardar unos minutos la primera vez, ya que descargará las imágenes de Docker y construirá la aplicación.

Ejecuta el siguiente comando en la terminal desde el directorio raíz del proyecto:

```bash
docker-compose up --build
```

  * La bandera `--build` fuerza a Docker Compose a reconstruir las imágenes, lo que es útil si has hecho cambios en el `Dockerfile` o en los requisitos.
  * Si solo necesitas iniciar los contenedores después de la primera vez, puedes omitir la bandera `--build`.

-----

### **Paso 4: Acceder a la API**

Una vez que los contenedores estén activos, el servidor de la API estará disponible.

1.  Abre tu navegador web.
2.  Navega a la documentación de la API interactiva en **http://localhost:8000/docs**.

Aquí puedes explorar todos los *endpoints* disponibles, probar las consultas y ver ejemplos de las respuestas.

### **Paso 5: Detener la Aplicación**

Para detener la ejecución de los contenedores, regresa a la terminal y presiona `Ctrl+C`. Luego, ejecuta el siguiente comando para detener y eliminar los contenedores (los datos de la base de datos persistirán gracias al volumen de Docker).

```bash
docker-compose down
```

Con estos sencillos pasos, la visión de **Alexander Chizhevsky** está ahora en tus manos. La plataforma está lista para que comiences a explorar la fascinante conexión entre el sol y la vida en la Tierra.
