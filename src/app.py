import os
import logging
from flask import Flask, jsonify, render_template, request
from .chat import Chat
from config.parameters import Parameters
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Flask application
#app = Flask(__name__)
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def index():
    return render_template('index.html')

# Initialize chat handler
parameters = Parameters().parameters
chat = Chat()

@app.route("/chat", methods=["POST"])
def virtual_assistant():
    """Endpoint for handling chat requests."""
    try:
        logger.info("Processing chat request...")
        #chat_response = chat.run()
        data = request.get_json(force=True)  # force=True helps avoid errors if the mimetype is not application/json
        logger.info(f"Received data: {data}")
        sessionID = data.get('sessionID')
        query = data.get('query')
        if not sessionID or not query:
            logger.error("Missing 'sessionID' or 'query' in the request.")
            return jsonify({"error": "Missing 'sessionID' or 'query' in the request."}), 400

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