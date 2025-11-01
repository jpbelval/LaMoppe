from flask import Flask, request, jsonify
import os
import routes


app = Flask(__name__)
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
chroma_client = None


@app.route("/classifyText", methods=["POST"])
def classify():
        text = request.json.get("prompt")
        return f"prompt: {text}"


@app.route("/test-db", methods=["GET"])
def test():
        return routes.test_db()



# @app.post("/generatePrompt")

# @app.post("/formatPrompt")
