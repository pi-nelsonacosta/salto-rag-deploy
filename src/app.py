import os
import logging
from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS
from chat import Chat
from config.parameters import Parameters
from dotenv import load_dotenv
import uuid

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Flask application
app = Flask(__name__)
#app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv("FLASK_SECRET_KEY")

cors=CORS(app, resources={r"*": {"origins":"*"}}, expose_headers='Authorization')

@app.route("/")
def index():
    return render_template('index.html')

# Initialize chat handler
parameters = Parameters().parameters
chat = Chat()

@app.route("/chat", methods=["POST"])
def virtual_assistant():
    """Endpoint para manejar las solicitudes de chat."""
    try:
        logger.info("Processing chat request...")

        # Intentar obtener el sessionID de la sesión almacenada en la cookie
        sessionID = session.get('sessionID')

        # Si no existe sessionID en la sesión, generar uno nuevo
        if not sessionID:
            sessionID = str(uuid.uuid4())  # Generar un nuevo sessionID único
            session['sessionID'] = sessionID  # Guardar en la sesión

        # Obtener los datos de la solicitud
        data = request.get_json(silent=True)  # Cambia force=True a silent=True para no lanzar errores
        if data is None:
            logger.error("No se recibió JSON en la solicitud.")
            return jsonify({"error": "No se recibió JSON en la solicitud."}), 400

        logger.info(f"Received data: {data}")
        
        query = data.get('query')

        # Verificar si hay query
        if not query:
            logger.error("Missing 'query' in the request.")
            return jsonify({"error": "Missing 'query' in the request."}), 400

        # Procesar la solicitud de chat
        chat_response = chat.run(sessionID, query)
        return chat_response
    except KeyError as e:
        logger.error(f"Missing key in JSON data: {e}")
        return jsonify({"error": f"Missing key in JSON data: {e}"}), 400
    except Exception as e:
        logger.error(f"Error during chat processing: {e}")
        return jsonify({"error": str(e)}), 500
    
def start_app():
    """Starts the Flask application."""
    # Set local parameters
    host=parameters.get("host", "127.0.0.1")
    port=parameters.get("port", 5000)

    # Run app
    app.run(host=host, port=port, debug=True)