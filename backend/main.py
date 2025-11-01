from flask import Flask, request, jsonify
import os
import routes
from flask_cors import CORS
from intelligence.app import SafetyIntelligence


app = Flask(__name__)

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
chroma_client = None
CORS(app, origins="*")
safetyIntelligence = SafetyIntelligence()
@app.route("/classifyText", methods=["POST"])
def classify():
        text = request.json.get("prompt")
        safetyAnalysis = safetyIntelligence.analyze_prompt(text)
        safetyAnalysis = jsonify(safetyAnalysis)
        return jsonify({
            "message": "Received successfully",
            "received": text
        })


@app.route("/test-db", methods=["GET"])
def test():
        return routes.test_db()



# @app.post("/generatePrompt")

# @app.post("/formatPrompt")
