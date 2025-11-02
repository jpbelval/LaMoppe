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


@app.route("/createDocument", methods=["POST"])
def create_doc():
        data = request.json
        return routes.create_document(data.get("collection"), data.get("text"), data.get("metadata"))

@app.route("/getDocument", methods=["GET"])
def get_doc():
        data = request.json
        return routes.read_document(data.get("collection"), data.get("id"))
        
@app.route("/deleteDocument", methods=["DELETE"])
def delete_doc():
        data = request.json
        return routes.delete_document(data.get("collection"), data.get("id"))

@app.route("/updateMetadata", methods=["PATCH"])
def update_meta():
        data = request.json
        return routes.update_document_metadata(data.get("collection"), data.get("id"), data.get("metadata"))

@app.route("/filterMetadata", methods=["GET"])
def filter_by_Meta():
        data = request.json
        return routes.read_documents_by_metadata(data.get("collection"), data.get("filter"))
        
@app.route("/getCollection", methods=["GET"])
def get_coll():
        data = request.json
        return routes.read_collection(data.get("collection"))

@app.route("/deleteCollection", methods=["DELETE"])
def delete_coll():
        data = request.json
        return routes.delete_collection(data.get("collection"))