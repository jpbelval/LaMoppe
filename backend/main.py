from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

@app.route("/classifyText", methods=["POST"])
def classify():
        text = request.json.get("prompt")
        return jsonify({
            "message": "Received successfully",
            "received": text
        })


# @app.post("/generatePrompt")

# @app.post("/formatPrompt")
