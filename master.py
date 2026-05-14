from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Mini-GFS Master Server")

files = {}       
chunks = {}      
chunkservers = []  
@app.get("/")
def home():
    return {"status": "Master server is running"}

@app.get("/files")
def list_files():
    return {"files": list(files.keys())}

@app.post("/files/{filename}")
def register_file(filename: str):
    if filename not in files:
        files[filename] = []
    return {"message": f"File {filename} registered", "filename": filename}

@app.get("/files/{filename}")
def get_file(filename: str):
    if filename not in files:
        return {"error": "File not found"}
    return {"filename": filename, "chunks": files[filename]}

@app.delete("/files/{filename}")
def delete_file(filename: str):
    if filename not in files:
        return {"error": "File not found"}
    del files[filename]
    return {"message": f"File {filename} deleted"}

@app.post("/chunkservers/register")
def register_chunkserver(address: str):
    if address not in chunkservers:
        chunkservers.append(address)
    return {"message": f"Chunkserver {address} registered", "total": len(chunkservers)}

@app.get("/chunkservers")
def list_chunkservers():
    return {"chunkservers": chunkservers, "total": len(chunkservers)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)