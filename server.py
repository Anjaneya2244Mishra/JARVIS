from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")


@app.route("/")
def home():
    return "Jarvis AI Server is running 🚀"


@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not OPENROUTER_API_KEY:
            return jsonify({"error": "API key missing"}), 500

        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400

        user_message = data["message"]

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

        print("Status Code:", response.status_code)
        print("Raw Response:", response.text)

        if response.status_code != 200:
            return jsonify({"error": response.text}), response.status_code

        result = response.json()

        if "choices" not in result:
            return jsonify({"error": result}), 500

        reply = result["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()

    app.run(host="0.0.0.0", port=10000)

