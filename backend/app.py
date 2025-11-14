from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from project root
load_dotenv(BASE_DIR / ".env")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load knowledge base
try:
    with open(BASE_DIR / "backend" / "knowledge_base.json", "r", encoding="utf-8") as f:
        knowledge_base = json.load(f)
except FileNotFoundError:
    print("Error: knowledge_base.json not found")
    knowledge_base = {}

# Load parties information
try:
    with open(BASE_DIR / "data" / "parties_info.json", "r", encoding="utf-8") as f:
        parties_info = json.load(f)
except FileNotFoundError:
    print("Error: parties_info.json not found")
    parties_info = {}

# Load system prompt
try:
    with open(BASE_DIR / "system_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()
except FileNotFoundError:
    print("Error: system_prompt.txt not found")
    system_prompt = "Du bist ein hilfreicher Wahl-Chatbot."

app = Flask(__name__)
CORS(app)

def get_ai_response(user_message, chat_history=[]):
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
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return f"Entschuldigung, es gab einen Fehler bei der Verarbeitung Ihrer Anfrage. Bitte versuchen Sie es später erneut."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("user_message", "")
    chat_history = data.get("chat_history", [])
    bot_response = get_ai_response(user_message, chat_history)
    return jsonify({"bot_response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)