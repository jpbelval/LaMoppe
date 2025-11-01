from flask import Flask, request, jsonify
from uuid import uuid4
from db_actions import get_db_client

def test_db():
    
    try:
        client = get_db_client()

        collection_name = "test_collection"
        collection = client.get_or_create_collection(name=collection_name)
        
        doc_id = f"doc_test_{int(uuid4())}" 
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

def create_document(collection_name, content, metadata):
        try:
                client = get_db_client()
                collection = client.get_or_create_collection(name=collection_name)
                doc_id = uuid4()
                collection.add(
                        documents=[content],
                        metadatas=[metadata],
                        ids=[str(doc_id)]
                )
                return {"success": True, "results": {"collection": collection_name, "id": doc_id, "status": "created"}}
                
        except Exception as e:
                print(f"Erreur lors du CREATE: {e}")
                return {"success": False, "error": str(e)}

def read_document(collection_name, doc_id):
        try:
                client = get_db_client()
                collection = client.get_collection(name=collection_name)

                result = collection.get(ids=[doc_id])
                if result['ids']:
                        return {"success": True, "results": result}
                else:
                        return {"success": False, "results": None, "message": f"Document {doc_id} non trouvé."}
            
        except Exception as e:
                print(f"Erreur lors du READ: {e}")
                return {"success": False, "error": str(e)}

def query_document(collection_name, query_text, n_results, filter_metadata=None): 
        try:
                client = get_db_client()
                collection = client.get_collection(name=collection_name)
                if not n_results:
                        n_results = 5

                if filter_metadata:
                        results = collection.query(
                        query_texts=[query_text],
                        n_results=int(n_results),
                        where=filter_metadata 
                )
                else:
                        results = collection.query(
                                query_texts=[query_text],
                                n_results=int(n_results)
                        )
            
                return {"success": True, "results": results}
        
        except Exception as e:
                return {"success": False, "error": str(e)}


def delete_document(collection_name, doc_id):
        try:
                client = get_db_client()
                collection = client.get_collection(name=collection_name)
                
                collection.delete(ids=[doc_id])
                return {"success": True, "results": {"collection": collection_name, "id": doc_id, "status": "deleted"}}
        except Exception as e:
                return {"success": False, "error": str(e)}

def update_document_metadata(collection_name, doc_id, new_metadata):
        try:
                client = get_db_client()
                collection = client.get_collection(name=collection_name)
                
                collection.update(
                ids=[doc_id],
                metadatas=[new_metadata] 
                )
                return {"success": True, "results": {"collection": collection_name, "id": doc_id, "status": "updated"}}
        except Exception as e:
                return {"success": False, "error": str(e)}


def read_collection(collection_name):
        try:
                client = get_db_client()
                collection = client.get_collection(name=collection_name)
                if collection.count() == 0:
                        return{"success": True, "results": None, "message": "collection vide"}
                print("there")
                documents = collection.get( limit=collection.count() )
                return {"success": True, "results": {"collection": collection_name,"content": documents}}
        except Exception as e:
                return {"success": False, "error": str(e)}


def delete_collection(collection_name):
        try:
                client = get_db_client()
                collection = client.delete_collection(name=collection_name)
                return {"success": True, "results": {"collection": collection_name, "status": "deleted"}}  
        except Exception as e:
                return {"success": False, "error": str(e)}


