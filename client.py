import requests

MASTER_URL = "http://localhost:8080"
CHUNKSERVER_URL = "http://localhost:8001"

def list_files():
    r = requests.get(f"{MASTER_URL}/files")
    print("Files:", r.json())

def upload_file(filename, content):
    # 1. Register file on master
    r = requests.post(f"{MASTER_URL}/files/{filename}")
    print("Registered on master:", r.json())

    # 2. Save actual data on chunkserver
    chunk_id = filename.replace(".", "_") + "_chunk1"
    r = requests.post(f"{CHUNKSERVER_URL}/chunks/{chunk_id}", params={"data": content})
    print("Saved on chunkserver:", r.json())

def get_file(filename):
    # 1. Ask master if file exists
    r = requests.get(f"{MASTER_URL}/files/{filename}")
    if "error" in r.json():
        print("File not found!")
        return

    # 2. Get actual data from chunkserver
    chunk_id = filename.replace(".", "_") + "_chunk1"
    r = requests.get(f"{CHUNKSERVER_URL}/chunks/{chunk_id}")
    print("File content:", r.json())

def delete_file(filename):
    r = requests.delete(f"{MASTER_URL}/files/{filename}")
    print("Deleted:", r.json())

# Test
print("=== Mini-GFS Client ===")
upload_file("test.txt", "Hello from Mini-GFS!")
list_files()
get_file("test.txt")
delete_file("test.txt")
list_files()