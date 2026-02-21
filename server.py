from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get(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)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/auto",
            "messages": [
                {"role": "system", "content": "You are Jarvis, a smart AI assistant."},
                {"role": "user", "content": user_message}
            ]
        }
    )

    data = response.json()
    reply = data["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)