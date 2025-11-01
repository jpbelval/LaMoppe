import os
import chromadb
import time

_client = None

def get_db_client():
    """
    Gère la connexion à ChromaDB et la maintient en singleton.
    Tente de se reconnecter si la connexion est perdue.
    """
    global _client
    
    if _client:
        try:
            _client.heartbeat()
            # La connexion est toujours active, on le retourne
            return _client
        except Exception as e:
            print(f"Connexion à ChromaDB perdue ({e}), tentative de reconnexion...")
            _client = None # Force la reconnexion

    CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
    
    for attempt in range(3):
        try:
            print(f"Tentative de connexion à ChromaDB {attempt + 1}/3 sur: {CHROMA_HOST}:8000")
            client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
            client.heartbeat()
            
            print("Connexion à ChromaDB réussie !")
            _client = client 
            return _client
        
        except Exception as e:
            print(f"Échec de la tentative {attempt + 1}: {e}")
            time.sleep(2) 

    # Si la boucle se termine throw error
    raise ConnectionError(f"Impossible de se connecter à ChromaDB sur {CHROMA_HOST} après 3 tentatives.")



# def createCollection():
#         client = await chromadb.AsyncHttpClient()

#         collection = await client


