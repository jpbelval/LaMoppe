from flask import Flask, request, jsonify, render_template
import os
import routes
from flask_cors import CORS
from intelligence.app import SafetyIntelligence
import json
from dashboard_logic import get_mock_data, get_new_recent_ratings, get_rating_color_class, get_risk_color_class


app = Flask(__name__)

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
chroma_client = None
CORS(app, origins="*")
safetyIntelligence = SafetyIntelligence()

# Register Jinja2 helper functions
@app.context_processor
def utility_processor():
    return {
        'get_rating_color_class': get_rating_color_class,
        'get_risk_color_class': get_risk_color_class
    }

@app.route("/classifyText", methods=["POST"])
def classify():
        text = request.json.get("prompt")
        safetyAnalysis = safetyIntelligence.analyze_prompt(text)
        json_result = safetyAnalysis.to_json()
        return json_result

@app.route("/stats/dashboard")
def dashboard():
    data = get_mock_data()
    return render_template('index.html', **data)

@app.route('/stats/fetch')
def getStats():
    data = {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "values": [12, 19, 3, 5, 2, 3, 7],
        "avg": 7.3
    }
    return jsonify(data)

@app.route('/api/recent-ratings')
def recent_ratings():
    """API endpoint for polling recent ratings from the dashboard."""
    recent_data = get_new_recent_ratings()
    return jsonify(recent_data)

@app.route('/api/dashboard-data')
def dashboard_data():
    """API endpoint for polling all dashboard data."""
    data = get_mock_data()
    return jsonify(data)

@app.route("/createDocument", methods=["POST"])
def create_doc():
        data = request.json
        return routes.create_document(data.get("collection"), data.get("text"), data.get("metadata"))

@app.route("/createRating", methods=["POST"])
def create_data():
        data = request.json
        return routes.create_rating(data.get("risk_level"), data.get("rating"), data.get("problems"), data.get("safe_prompt"))

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