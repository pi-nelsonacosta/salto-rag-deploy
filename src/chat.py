import json
import logging
from flask import request, jsonify
from dotenv import load_dotenv
from services.azopenai import AzureOpenAIClient
from services.azureaisearch import AzureAISearchClient
from services.cosmosdb import AzureCosmosDBClient
from config.parameters import Parameters


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Azure SDK logging level to WARNING to reduce noise
azure_logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
azure_logger.setLevel(logging.WARNING)

load_dotenv()

class Chat:
    """Class to handle chat interactions."""

    def __init__(self):
        try:
            # Set parameters
            parameters = Parameters().parameters
            self.prompts_path = parameters.get("prompts_path")
            logger.info("Parameters loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading parameters: {e}")
            raise
    
    @staticmethod
    def get_request_data(key):
        """Retrieves data from the request JSON body."""
        value = request.json.get(key)
        if value is None:
            logger.warning(f"Request key '{key}' not found in the request JSON body.")
        return value
    
    @staticmethod
    def read_file(file_path, as_json=False):
        """Reads content from a file."""
        try:
            with open(file_path, 'r') as file:
                logger.info(f"File '{file_path}' successfully loaded.")
                if as_json:
                    return json.load(file)
                else:
                    return file.read()
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON file: {file_path}")
            return ""
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return ""
    
    def run(self, sessionID, query):
        """Processes the chat request and returns a response."""
        try:
            logger.info("Starting chat response processing...")
            azurezopenai = AzureOpenAIClient()
            azureaisearch = AzureAISearchClient()
            azurecosmos = AzureCosmosDBClient()

            # Load prompt file
            system_prompt = self.read_file(f"{self.prompts_path}/system_prompt.prompt")

            session_id = sessionID
            query = query

            if not query or not session_id:
                return {"error": "Query or SessionID not provided"}, 400
            
            messages_history = []

            context_results = azureaisearch.run(query)
            if not context_results:
                raise ValueError("Empty response from Azure OpenAI")
            
            context = [item['content'] for item in context_results]
            input = f"Context: {context}\nQuery: \"{query}\""
            message_user = [{"role": "user", "content": input}]
            
            chat_history = azurecosmos.run(session_id, 'S')
            messages_history = chat_history['chat_history']
            
            response = azurezopenai.run(system_prompt, messages_history, message_user)
            if not response:
                raise ValueError("Empty response from Azure OpenAI")
            
            message_user_save = [{"role": "user", "content": query}]
            azurecosmos.run(session_id, 'I', message_user_save)
            message_assistant_save = [{"role": "assistant", "content": response}]
            azurecosmos.run(session_id, 'I', message_assistant_save)

            return {"response": response}, 200
        except Exception as e:
            logger.error(f"Error generating model response: {e}")
            return {"error": str(e)}, 500
