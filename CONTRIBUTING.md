<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guía de Contribución | HelioBio-API</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-200 p-6 min-h-screen flex items-center justify-center">

    <div class="container mx-auto max-w-4xl bg-gray-800 rounded-lg shadow-2xl p-8 md:p-12 border border-gray-700">
        <header class="text-center mb-10">
            <h1 class="text-3xl md:text-4xl font-extrabold text-white mb-2">Guía de Contribución: Construyendo la HelioBio-API</h1>
            <p class="text-md md:text-lg text-gray-400 max-w-2xl mx-auto">
                Bienvenido. Este proyecto no es solo un conjunto de algoritmos y puntos de datos; es una herramienta para conectar el cosmos con la biosfera, una visión inspirada por el espíritu indomable de **Alexander Chizhevsky**. Al igual que él desafió el dogma de su tiempo para revelar las verdades que unen al sol con la humanidad, te invitamos a unirte a nosotros para construir algo que trasciende lo convencional.
            </p>
        </header>

        <section class="mb-10">
            <p class="text-lg text-center text-gray-400 mb-6">
                Nuestra misión es simple pero audaz: usar la tecnología para manifestar las ideas de la Heliobiología, la Cosmobiología y la Historiometría. Queremos que el código que escribas no solo funcione, sino que resuene con el propósito de revelar los patrones ocultos que gobiernan la vida en la Tierra.
            </p>
        </section>

        <hr class="border-gray-700 mb-10">

        <section class="mb-10">
            <h2 class="text-2xl font-bold text-white mb-6">Principios Fundamentales de la Contribución</h2>
            <p class="text-gray-300 mb-4">
                Antes de escribir una sola línea de código, te pedimos que adoptes nuestra filosofía. Como Da Vinci y Copérnico, quienes persistieron a pesar de la "mano invisible" del dogma, buscamos colaboradores que valoren la verdad sobre la conveniencia.
            </p>
            <ul class="list-none space-y-4">
                <li class="p-4 bg-gray-700 rounded-lg shadow-inner border border-gray-600">
                    <strong class="text-lg text-yellow-300">Sé un Polímata Digital:</strong> No te limites a tu especialidad. Fomenta la curiosidad. Pregunta cómo un cambio en el backend puede afectar la visualización de un gráfico o cómo una nueva teoría biológica podría integrarse en la arquitectura de la API.
                </li>
                <li class="p-4 bg-gray-700 rounded-lg shadow-inner border border-gray-600">
                    <strong class="text-lg text-yellow-300">Busca la Conexión Oculta:</strong> Nuestro trabajo no es solo procesar datos, es encontrar la **sintaxis oculta** entre ellos. Si encuentras una forma de conectar dos conjuntos de datos aparentemente dispares, esa es una contribución invaluable.
                </li>
                <li class="p-4 bg-gray-700 rounded-lg shadow-inner border border-gray-600">
                    <strong class="text-lg text-yellow-300">La Humildad es la Piedra Angular:</strong> Reconoce que nuestra visión es ambiciosa y que habrá errores en el camino. No te aferres a tu código; aférrate a la misión. El verdadero progreso se construye corrigiendo y aprendiendo de los errores.
                </li>
            </ul>
        </section>

        <hr class="border-gray-700 mb-10">

        <section class="mb-10">
            <h2 class="text-2xl font-bold text-white mb-6">Cómo empezar tu viaje</h2>
            <p class="text-gray-300 mb-4">
                El camino hacia la interconexión cósmica comienza con pasos prácticos.
            </p>

            <h3 class="text-xl font-semibold text-white mb-4">1. Requisitos de Instalación</h3>
            <ul class="list-disc list-inside space-y-2 text-gray-300 mb-6">
                <li><strong class="text-yellow-300">Git:</strong> Para gestionar el control de versiones.</li>
                <li><strong class="text-yellow-300">Node.js & npm:</strong> Nuestro entorno de desarrollo se basa en Node.js para la API y sus dependencias.</li>
            </ul>

            <h3 class="text-xl font-semibold text-white mb-4">2. Clonar el Repositorio</h3>
            <p class="text-gray-300 mb-2">
                Abre tu terminal y clona el repositorio del proyecto:
            </p>
            <div class="bg-gray-700 p-4 rounded-lg shadow-inner overflow-x-auto text-sm text-gray-300 mb-6">
                <pre><code>git clone https://github.com/HelioBio-API/HelioBio-API.git</code></pre>
            </div>
            <p class="text-gray-300 mb-2">
                Navega al directorio del proyecto e instala las dependencias:
            </p>
            <div class="bg-gray-700 p-4 rounded-lg shadow-inner overflow-x-auto text-sm text-gray-300">
                <pre><code>cd HelioBio-API<br>npm install</code></pre>
            </div>

            <h3 class="text-xl font-semibold text-white mt-6 mb-4">3. Configuración del Entorno</h3>
            <p class="text-gray-300">
                Crea un archivo `.env` en la raíz del proyecto para gestionar las variables de entorno. Necesitarás configurar el acceso a la base de datos y otras claves API. Consulta el archivo `env.example` en el repositorio para ver los campos requeridos.
            </p>
        </section>

        <hr class="border-gray-700 mb-10">

        <section class="mb-10">
            <h2 class="text-2xl font-bold text-white mb-6">El Proceso de Contribución</h2>
            <p class="text-gray-300 mb-4">
                Tu código es tu **códice**. Presenta tus ideas con claridad y precisión para que la comunidad pueda entender tu visión.
            </p>

            <h3 class="text-xl font-semibold text-white mb-4">1. Crea una Rama de Trabajo:</h3>
            <p class="text-gray-300 mb-2">
                Comienza cada nueva contribución en una rama separada para mantener el historial limpio. Utiliza un nombre descriptivo:
            </p>
            <div class="bg-gray-700 p-4 rounded-lg shadow-inner overflow-x-auto text-sm text-gray-300 mb-4">
                <pre><code>git checkout -b feature/nombre-de-tu-caracteristica</code></pre>
            </div>
            <p class="text-gray-300 mb-2">
                O si es una corrección de un error:
            </p>
            <div class="bg-gray-700 p-4 rounded-lg shadow-inner overflow-x-auto text-sm text-gray-300">
                <pre><code>git checkout -b fix/descripcion-del-error</code></pre>
            </div>

            <h3 class="text-xl font-semibold text-white mt-6 mb-4">2. Escribe Tu Código y Comentarios:</h3>
            <p class="text-gray-300">
                Desarrolla tu solución. Asegúrate de que tu código esté bien documentado. Cada función, cada clase, es un "jeroglífico" que debe ser legible para los demás. Explica el "porqué" de tus decisiones de diseño.
            </p>

            <h3 class="text-xl font-semibold text-white mt-6 mb-4">3. Realiza un Commit de tus Cambios:</h3>
            <p class="text-gray-300 mb-2">
                Agrega tus archivos y crea un commit con un mensaje claro y conciso. Piensa en el mensaje como un titular para tu "códice".
            </p>
            <div class="bg-gray-700 p-4 rounded-lg shadow-inner overflow-x-auto text-sm text-gray-300">
                <pre><code>git add .<br>git commit -m "feat: añadir endpoint para datos de actividad solar"</code></pre>
            </div>

            <h3 class="text-xl font-semibold text-white mt-6 mb-4">4. Envía tu "Códice" (Pull Request):</h3>
            <p class="text-gray-300">
                Sube tu rama al repositorio remoto y abre un **Pull Request**. Describe tu contribución en detalle. ¿Qué problema resuelve? ¿Qué nueva conexión de datos revela? ¿Cómo honra la visión de Chizhevsky?
            </p>
        </section>

        <hr class="border-gray-700 mb-10">

        <section>
            <h2 class="text-2xl font-bold text-white mb-6">Más Allá del Código</h2>
            <p class="text-gray-300 mb-4">
                Tu contribución no se limita a escribir código. Puedes ayudar a construir el futuro de la Heliobiología de otras maneras.
            </p>
            <ul class="list-disc list-inside space-y-2 text-gray-300">
                <li><strong class="text-yellow-300">Documentación:</strong> Mejora nuestros manuales, crea tutoriales y explica conceptos complejos de forma simple.</li>
                <li><strong class="text-yellow-300">Investigación:</strong> Identifica nuevos conjuntos de datos sobre ciclos biológicos o eventos históricos que podamos integrar en la API.</li>
                <li><strong class="text-yellow-300">Discusión de Ideas:</strong> Participa activamente en el rastreador de problemas y las discusiones de la comunidad. Tus preguntas y perspectivas son vitales para la evolución del proyecto.</li>
            </ul>
            <p class="text-lg font-semibold text-yellow-300 mt-6 text-center">
                Tu esfuerzo es crucial para construir esta API. El verdadero poder no reside en las líneas de código, sino en la <strong class="text-white">conexión invisible</strong> que creamos juntos. Bienvenido a bordo.
            </p>
        </section>

    </div>

</body>
</html>
