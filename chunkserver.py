from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="Mini-GFS Chunkserver")

PORT = 8001
STORAGE_DIR = f"chunks_{PORT}"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "Chunkserver is running", "port": PORT}

@app.post("/chunks/{chunk_id}")
def save_chunk(chunk_id: str, data: str):
    filepath = os.path.join(STORAGE_DIR, chunk_id)
    with open(filepath, "w") as f:
        f.write(data)
    return {"message": f"Chunk {chunk_id} saved"}

@app.get("/chunks/{chunk_id}")
def get_chunk(chunk_id: str):
    filepath = os.path.join(STORAGE_DIR, chunk_id)
    if not os.path.exists(filepath):
        return {"error": "Chunk not found"}
    with open(filepath, "r") as f:
        data = f.read()
    return {"chunk_id": chunk_id, "data": data}

@app.get("/chunks")
def list_chunks():
    chunks = os.listdir(STORAGE_DIR)
    return {"chunks": chunks, "total": len(chunks)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)