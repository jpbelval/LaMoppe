from flask import Flask, request, jsonify
import uuid
from db_actions import get_db_client

def test_db():
    
    try:
        client = get_db_client()

        collection_name = "test_collection"
        collection = client.get_or_create_collection(name=collection_name)
        
        doc_id = f"doc_test_{int(uuid.uuid4())}" 
        collection.add(
            documents=["Ceci est un document de test pour ChromaDB."],
            metadatas=[{"source": "flask_api"}],
            ids=[doc_id]
        )
        
        result = collection.get(ids=[doc_id])
        
        count = collection.count()
        
        return jsonify({
            "status": "succes",
            "message": "Document ajoute et recupere de ChromaDB.",
            "collection_comptage": count,
            "document_recupere": result
        }), 200

    except ConnectionError as e:
        return jsonify({"status": "échec", "error": f"Erreur de connexion ChromaDB: {e}"}), 500
    except Exception as e:
        return jsonify({"status": "échec", "error": f"Erreur lors de l'opération ChromaDB: {e}"}), 500
