# Mini-GFS — Distributed File System

A simplified version of Google File System implemented in Python.

## Team
- Nesibeli — Master Server, Chunkserver, Client
- [name] — Replication
- [name] — Tests
- [name] — AI Agent
- [name] — Presentation
- [name] — Docker

## Architecture
- **Master** (port 8080) — stores file metadata
- **Chunkserver** (port 8001) — stores actual data chunks
- **Client** — API for uploading and downloading files

## How to Run

### 1. Install dependencies
py -m pip install fastapi uvicorn requests
### 2. Start Master Server
py master.py
### 3. Start Chunkserver
py chunkserver.py
### 4. Test with Client
py client.py
## Technologies
- Python 3.12
- FastAPI
- Uvicorn