import logging
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Parameters:
    """Class to load configuration parameters from a JSON file."""

    def __init__(self, config_path=None):
        # Si no se pasa un path, usar la ruta relativa correcta desde el directorio actual
        if config_path is None:
            # Obtener el directorio actual (donde está parameters.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Usar la ruta relativa correcta a parameters.json
            config_path = os.path.join(current_dir, "parameters.json")
        
        self.config_path = config_path
        self.parameters = self.load_parameters()

    def load_parameters(self):
        """Loads parameters from the JSON configuration file."""
        try:
            with open(self.config_path) as file:
                parameters = json.load(file)
            logger.info("Parameters loaded successfully.")
            return parameters
        except FileNotFoundError:
            logger.error(f"Configuration file not found at {self.config_path}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from the configuration file: {e}")
            return {}
