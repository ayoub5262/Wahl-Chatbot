from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from openai import OpenAI
import os
import sys
from pathlib import Path

# Add parent directory to path to allow imports when running directly
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.config import Config
from backend.utils import setup_logger

# Set up logger
logger = setup_logger(__name__)

# Validate configuration
try:
    Config.validate()
    logger.info("Configuration validated successfully")
except Exception as e:
    logger.error(f"Configuration validation failed: {e}")
    raise

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)
logger.info("OpenAI client initialized")

# Load knowledge base
try:
    with open(Config.KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
        knowledge_base = json.load(f)
    logger.info("Knowledge base loaded successfully")
except FileNotFoundError as e:
    logger.error(f"Error: knowledge_base.json not found at {Config.KNOWLEDGE_BASE_PATH}")
    knowledge_base = {}
except json.JSONDecodeError as e:
    logger.error(f"Error decoding knowledge_base.json: {e}")
    knowledge_base = {}

# Load parties information
try:
    with open(Config.PARTIES_INFO_PATH, "r", encoding="utf-8") as f:
        parties_info = json.load(f)
    logger.info("Parties information loaded successfully")
except FileNotFoundError as e:
    logger.error(f"Error: parties_info.json not found at {Config.PARTIES_INFO_PATH}")
    parties_info = {}
except json.JSONDecodeError as e:
    logger.error(f"Error decoding parties_info.json: {e}")
    parties_info = {}

# Load system prompt
try:
    with open(Config.SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    logger.info("System prompt loaded successfully")
except FileNotFoundError as e:
    logger.error(f"Error: system_prompt.txt not found at {Config.SYSTEM_PROMPT_PATH}")
    system_prompt = "Du bist ein hilfreicher Wahl-Chatbot."

app = Flask(__name__, static_folder=str(Config.FRONTEND_DIR), static_url_path='')
CORS(app)
logger.info("Flask app initialized")

def get_ai_response(user_message, chat_history=[]):
    """
    Get AI response from OpenAI API.
    
    Args:
        user_message: User's message
        chat_history: List of previous messages
    
    Returns:
        str: AI response
    """
    # Build context with knowledge base
    context = system_prompt + "\n\nWISSENSBASIS:\n"
    context += json.dumps(knowledge_base, ensure_ascii=False, indent=2)
    context += "\n\nPARTEIEN-INFORMATIONEN:\n"
    context += json.dumps(parties_info, ensure_ascii=False, indent=2)
    
    messages = [{"role": "system", "content": context}]
    
    # Add chat history
    for h in chat_history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["bot"]})
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        logger.debug(f"Sending request to OpenAI API for message: {user_message[:50]}...")
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=messages,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS
        )
        ai_response = response.choices[0].message.content
        logger.debug("Received response from OpenAI API")
        return ai_response
    except Exception as e:
        logger.error(f"OpenAI API Error: {str(e)}", exc_info=True)
        return f"Entschuldigung, es gab einen Fehler bei der Verarbeitung Ihrer Anfrage. Bitte versuchen Sie es später erneut."

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/data/<path:path>")
def serve_data(path):
    return send_from_directory(Config.DATA_DIR, path)

@app.route("/wahl-chatbot-logo.png")
def serve_logo():
    return send_from_directory(Config.FRONTEND_DIR, 'wahl-chatbot-logo.png')

@app.route("/wahl-chatbot-logo1.PNG")
def serve_logo1():
    return send_from_directory(Config.FRONTEND_DIR, 'wahl-chatbot-logo1.PNG')

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle chat requests with input validation and error handling.
    
    Returns:
        JSON response with bot response or error message
    """
    try:
        # Get and validate request data
        data = request.get_json()
        
        if not data:
            logger.warning("Chat request received with no data")
            return jsonify({"error": "No data provided"}), 400
        
        # Validate user message
        user_message = data.get("user_message", "").strip()
        
        if not user_message:
            logger.warning("Chat request received with empty message")
            return jsonify({"error": "Message cannot be empty"}), 400
        
        if len(user_message) > Config.MAX_MESSAGE_LENGTH:
            logger.warning(f"Chat request received with message too long: {len(user_message)} characters")
            return jsonify({"error": f"Message too long (max {Config.MAX_MESSAGE_LENGTH} characters)"}), 400
        
        # Validate chat history
        chat_history = data.get("chat_history", [])
        
        if not isinstance(chat_history, list):
            logger.warning("Chat request received with invalid chat_history type")
            return jsonify({"error": "Chat history must be a list"}), 400
        
        if len(chat_history) > Config.MAX_CHAT_HISTORY_LENGTH:
            logger.warning(f"Chat request received with chat history too long: {len(chat_history)} entries")
            return jsonify({"error": f"Chat history too long (max {Config.MAX_CHAT_HISTORY_LENGTH} entries)"}), 400
        
        # Process the request
        logger.info(f"Processing chat request: '{user_message[:50]}...'")
        bot_response = get_ai_response(user_message, chat_history)
        logger.info("Chat request processed successfully")
        
        return jsonify({"bot_response": bot_response})
    
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    logger.info(f"Starting Wahl-Chatbot server on port {Config.PORT}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)