# Salto Labs Project

Este proyecto es una aplicación RAG basada en Flask que integra varios servicios como Azure OpenAI, Azure AI Search, y CosmosDB.

## Estructura del Proyecto

- **`main.py`**: Archivo principal que inicia la aplicación.
- **`chat.py`**: Define la clase `Chat`, que es responsable de procesar las solicitudes del chat de los usuarios. Las principales funciones incluyen:

- **Carga de parámetros**: Carga parámetros de configuración desde un archivo para definir rutas y otros ajustes.
- **Procesamiento de consultas**: Recibe y maneja solicitudes de chat, obteniendo las consultas enviadas por el usuario.

- **Gestión de archivos**: Permite leer archivos necesarios para procesar correctamente las solicitudes.
- **`app.py`**: Este archivo es el punto de entrada de la aplicación Flask y expone los endpoints principales:
- **`/`**: Sirve la página principal de la aplicación web.
- **`/chat`**: Endpoint que recibe solicitudes POST con consultas de los usuarios y devuelve respuestas procesadas por el archivo `chat.py`.

- **Gestión de sesiones**: Asigna un `sessionID` único a cada usuario para mantener el estado de la sesión.
- **Arranque de la aplicación**: Ejecuta la aplicación Flask en el host y puerto especificados en los parámetros de configuración.

- **Servicios** (`services/`): Implementaciones de servicios que interactúan con APIs y bases de datos.
  - `azopenai.py`: Servicio para interactuar con la API de OpenAI de Azure.
  - `azureaisearch.py`: Servicio para realizar búsquedas con Azure AI Search.
  - `cosmosdb.py`: Servicio para interactuar con la base de datos CosmosDB.
- **Configuración** (`config/`): Archivos de configuración para los parámetros de la aplicación.
- **Estáticos** (`static/`): Contiene archivos estáticos como imágenes, estilos y scripts.
- **Plantillas** (`templates/`): Contiene las plantillas HTML para la aplicación web.

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instaladas las siguientes dependencias:

## Instrucciones para Windows

1. Abre una terminal (CMD o PowerShell) y navega hasta la carpeta del proyecto.
   
2. Crea el entorno virtual con el siguiente comando:

   ```bash
   python -m venv venv

3. Activa el entorno virtual con el siguiente comando:
   
    ```bash
    venv\Scripts\activate

4. Instala las dependencias del proyecto utilizando el siguiente comando:

   ```bash
   pip install -r requirements.txt


## Instrucciones para macOS/Linux

1. Abre una terminal y navega hasta la carpeta del proyecto.

2. Crea el entorno virtual con el siguiente comando:

   ```bash
   python3 -m venv venv

3. Activa el entorno virtual con el siguiente comando:

   ```bash
   source venv/bin/activate

4. Instala las dependencias del proyecto utilizando el siguiente comando:  

   ```bash
   pip install -r requirements.txt


## Ejecución del Proyecto

Una vez que hayas creado y activado el entorno virtual e instalado las dependencias, puedes ejecutar la aplicación con:

   ```bash
   uvicorn main:app --reload

- Esto iniciará la aplicación en modo de desarrollo, y podrás acceder a la API en http://127.0.0.1:8080/.