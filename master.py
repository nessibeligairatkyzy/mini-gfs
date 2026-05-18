from fastapi import FastAPI
import uvicorn
import requests

app = FastAPI(title="Mini-GFS Master Server")

files = {}

chunkservers = [
    "http://chunkserver1:8001",
    "http://chunkserver2:8002",
    "http://chunkserver3:8003",
]

REPLICATION_FACTOR = 3


@app.get("/")
def home():
    return {"status": "Master server is running"}


@app.get("/files")
def list_files():
    return {"files": files}


@app.post("/files/{filename}")
def upload_file(filename: str, data: str):
    chunk_id = filename.replace(".", "_") + "_chunk1"
    replicas = chunkservers[:REPLICATION_FACTOR]

    saved_on = []

    for server in replicas:
        try:
            response = requests.post(
                f"{server}/chunks/{chunk_id}",
                params={"data": data}
            )

            if response.status_code == 200:
                saved_on.append(server)

        except requests.exceptions.RequestException:
            print(f"Failed to save chunk on {server}")

    if len(saved_on) == 0:
        return {"error": "File was not saved on any chunkserver"}

    files[filename] = {
        "chunk_id": chunk_id,
        "replicas": saved_on
    }

    return {
        "message": "File uploaded with replication",
        "filename": filename,
        "chunk_id": chunk_id,
        "replicas": saved_on,
        "replication_factor": len(saved_on)
    }


@app.get("/files/{filename}")
def get_file(filename: str):
    if filename not in files:
        return {"error": "File not found"}

    chunk_id = files[filename]["chunk_id"]
    replicas = files[filename]["replicas"]

    for server in replicas:
        try:
            response = requests.get(f"{server}/chunks/{chunk_id}")

            if response.status_code == 200:
                result = response.json()

                if "data" in result:
                    return {
                        "filename": filename,
                        "data": result["data"],
                        "read_from": server,
                        "replicas": replicas
                    }

        except requests.exceptions.RequestException:
            print(f"Failed to read from {server}")

    return {"error": "Could not read file from any replica"}


@app.delete("/files/{filename}")
def delete_file(filename: str):
    if filename not in files:
        return {"error": "File not found"}

    chunk_id = files[filename]["chunk_id"]
    replicas = files[filename]["replicas"]

    deleted_from = []

    for server in replicas:
        try:
            response = requests.delete(f"{server}/chunks/{chunk_id}")

            if response.status_code == 200:
                deleted_from.append(server)

        except requests.exceptions.RequestException:
            print(f"Failed to delete chunk from {server}")

    del files[filename]

    return {
        "message": "File deleted",
        "filename": filename,
        "deleted_from": deleted_from
    }


@app.get("/chunkservers")
def list_chunkservers():
    return {
        "chunkservers": chunkservers,
        "replication_factor": REPLICATION_FACTOR
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)