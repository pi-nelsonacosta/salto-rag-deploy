import os
import logging
from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS  # Importa CORS
from config.parameters import Parameters
import uuid
import sys
from chat import Chat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Flask application
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "0#$%&kLSOKMC#5&/(/sdfk{%}_)")

# Configura CORS
CORS(app)  # Habilita CORS para todas las rutas con configuración predeterminada

# Initialize chat handler
parameters = Parameters().parameters
chat = Chat()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/check_env")
def check_env():
    python_path = sys.executable  # Ruta del ejecutable de Python
    installed_packages = os.popen("pip freeze").read()  # Paquetes instalados
    
    # Listar archivos en el directorio raíz de la aplicación
    root_files = os.listdir("/home/site/wwwroot")  # Ruta raíz en Azure Web App
    has_requirements = "requirements.txt" in root_files

    return jsonify({
        "python_path": python_path,
        "installed_packages": installed_packages,
        "root_files": root_files,  # Lista todos los archivos en el directorio raíz
        "requirements_txt_exists": has_requirements  # Confirma si requirements.txt está presente
    })

@app.route("/chat", methods=["POST"])
def virtual_assistant():
    """Endpoint para manejar las solicitudes de chat."""
    try:
        logger.info("Processing chat request...")

        # Intentar obtener el sessionID de la solicitud o de la sesión almacenada en la cookie
        data = request.get_json(silent=True)
        if not data:
            logger.error("No se recibió JSON en la solicitud.")
            return jsonify({"error": "No se recibió JSON en la solicitud."}), 400

        sessionID = data.get('sessionID') or session.get('sessionID')

        # Si no existe sessionID en la sesión, generar uno nuevo
        if not sessionID:
            sessionID = str(uuid.uuid4())  # Generar un nuevo sessionID único
            session['sessionID'] = sessionID  # Guardar en la sesión

        logger.info(f"Received data: {data}")

        query = data.get('query')

        # Verificar si hay query
        if not query:
            logger.error("Missing 'query' in the request.")
            return jsonify({"error": "Missing 'query' in the request."}), 400

        # Procesar la solicitud de chat
        chat_response, status_code = chat.run(sessionID, query)

        # Verificar si hubo un error en la respuesta de `chat.run()`
        if status_code != 200:
            return jsonify({"error": chat_response.get("error")}), status_code

        # Devolver la respuesta del asistente junto con el sessionID
        response_data = {
            "response": chat_response.get("response"),
            "sessionID": sessionID
        }

        return jsonify(response_data), status_code

    except KeyError as e:
        logger.error(f"Missing key in JSON data: {e}")
        return jsonify({"error": f"Missing key in JSON data: {e}"}), 400
    except Exception as e:
        logger.error(f"Error during chat processing: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    """Starts the Flask application."""
    # Set local parameters
    app.run(host="0.0.0.0", port=5000)
