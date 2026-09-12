import os
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI


# Load your private API key from .env
env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path)

print("API key loaded:", bool(os.getenv("OPENAI_API_KEY")))

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/")
def home():
    return jsonify({
        "message": "WML AI backend is running!"
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "error": "Please enter a message."
            }), 400

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=(
                "You are WML AI, a helpful multilingual AI assistant. "
                "Help with English, Thai, and Myanmar. "
                "Translate text, explain vocabulary, correct grammar, "
                "teach languages, and answer general questions clearly."
            ),
            input=message,
        )

        return jsonify({
            "reply": response.output_text
        })

    except Exception as e:
        print("AI ERROR:", e)

        return jsonify({
            "error": "AI request failed."
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False,
    )