from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test the API connection
try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher politischer Chatbot."},
            {"role": "user", "content": "Was hält die Ökologische Partei von Atomkraft?"}
        ]
    )
    print("✅ OpenAI API Test erfolgreich!\n")
    print("Antwort:", response.choices[0].message.content)
except Exception as e:
    print("❌ Fehler beim API-Test:")
    print(str(e))
