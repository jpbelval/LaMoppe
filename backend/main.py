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

@app.route("/createDocument", methods=["POST"])
def create_doc():
        data = request.json
        return routes.create_document(data.get("collection"), data.get("text"), data.get("metadata"))

@app.route("/getDocument", methods=["GET"])
def get_doc():
        data = request.json
        return routes.read_document(data.get("collection"), data.get("id"))

@app.route("/queryDocument", methods=["GET"])
def query_doc():
        data = request.json
        return routes.query_document(data.get("collection"), data.get("query"), data.get("quantity"), data.get("filter"))

@app.route("/deleteDocument", methods=["DELETE"])
def delete_doc():
        data = request.json
        return routes.delete_document(data.get("collection"), data.get("id"))

@app.route("/updateMetadata", methods=["PATCH"])
def update_meta():
        data = request.json
        return routes.update_document_metadata(data.get("collection"), data.get("id"), data.get("metadata"))

@app.route("/getCollection", methods=["GET"])
def get_coll():
        data = request.json
        return routes.read_collection(data.get("collection"))

@app.route("/deleteCollection", methods=["DELETE"])
def delete_coll():
        data = request.json
        return routes.delete_collection(data.get("collection"))