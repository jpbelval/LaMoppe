from flask import Flask, request, jsonify
from uuid import uuid4
from db_actions import get_db_client
from json_formatter import format_json

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

                content = collection.get(ids=[doc_id])
                if content['ids']:
                        return format_json({"success": True, "results": {"collection": collection_name,"content": content}})

                else:
                        return { "success": False, "results": f"no document matched for id: {doc_id} in collection{collection_name}"}
            
        except Exception as e:
                print(f"Erreur lors du READ: {e}")
                return {"success": False, "error": str(e)}


def delete_document(collection_name, doc_id):
        try:
                client = get_db_client()
                collection = client.get_collection(name=collection_name)
                
                collection.delete(ids=[doc_id])
                return {"success": True, "results": {"collection": collection_name, "id": doc_id, "status": "deleted"}}
        except Exception as e:
                return {"success": False, "error": str(e)}

def read_documents_by_metadata(collection_name, filter_metadata):
        try:
                client = get_db_client()
                collection = client.get_collection(name=collection_name)

                content = collection.get(
                        where=filter_metadata
                )

                if not content:
                        return { "success": False, "results": f"no document matched filter: {filter_metadata} in collection {collection_name}"}

                return format_json({ "success": True, "results": {"collection": collection_name, "content": content }})
        except Exception as e:
                return { "success": False, "error": str(e)}

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
                        return { "success": False, "results": f"no document in collection {collection_name}"}

                content = collection.get( limit=collection.count() )
                return format_json({"success": True, "results": {"collection": collection_name,"content": content}})
        except Exception as e:
                return {"success": False, "error": str(e)}


def delete_collection(collection_name):
        try:
                client = get_db_client()
                collection = client.delete_collection(name=collection_name)
                return {"success": True, "results": {"collection": collection_name, "status": "deleted"}}  
        except Exception as e:
                return {"success": False, "error": str(e)}

def create_rating(risk_level, rating, problems, safe_prompt):
        try:
                client = get_db_client()
                collection = client.get_or_create_collection(name="JP_la_collection")
                doc_id = uuid4()

                metadata = {
                        "risk_level": risk_level,
                        "rating": rating,
                        "problems": problems
                }
                collection.add(
                        documents=[safe_prompt],
                        metadatas=[metadata],
                        ids=[str(doc_id)]   
                )
                return {"success": True, "results": {"collection": "JP_la_collection", "id": doc_id, "status": "created"}}

        except Exception as e:
                return {"success": False, "error": str(e)}
