from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")  # your HTML page

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a professional music assistant that can recommend songs, artists, and genres."},
            {"role": "user", "content": user_message}
        ]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
