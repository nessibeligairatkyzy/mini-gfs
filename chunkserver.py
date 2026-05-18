from fastapi import FastAPI
import uvicorn
import os
import sys

app = FastAPI(title="Mini-GFS Chunkserver")

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
STORAGE_DIR = f"chunks_{PORT}"

os.makedirs(STORAGE_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"status": "Chunkserver is running", "port": PORT}


@app.post("/chunks/{chunk_id}")
def save_chunk(chunk_id: str, data: str):
    filepath = os.path.join(STORAGE_DIR, chunk_id)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)

    return {"message": "Chunk saved", "chunk_id": chunk_id, "port": PORT}


@app.get("/chunks/{chunk_id}")
def get_chunk(chunk_id: str):
    filepath = os.path.join(STORAGE_DIR, chunk_id)

    if not os.path.exists(filepath):
        return {"error": "Chunk not found"}

    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()

    return {"chunk_id": chunk_id, "data": data, "port": PORT}


@app.delete("/chunks/{chunk_id}")
def delete_chunk(chunk_id: str):
    filepath = os.path.join(STORAGE_DIR, chunk_id)

    if os.path.exists(filepath):
        os.remove(filepath)
        return {"message": "Chunk deleted", "chunk_id": chunk_id, "port": PORT}

    return {"error": "Chunk not found", "port": PORT}


@app.get("/chunks")
def list_chunks():
    return {
        "chunks": os.listdir(STORAGE_DIR),
        "port": PORT
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)