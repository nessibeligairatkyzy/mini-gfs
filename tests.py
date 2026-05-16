import requests

MASTER_URL = "http://localhost:8080"
CHUNKSERVER_URL = "http://localhost:8001"

def test_upload_file():
    r = requests.post(f"{MASTER_URL}/files/test.txt")
    assert r.status_code == 200
    print("✅ test_upload_file passed")

def test_list_files():
    r = requests.get(f"{MASTER_URL}/files")
    assert "test.txt" in r.json()["files"]
    print("✅ test_list_files passed")

def test_save_chunk():
    r = requests.post(f"{CHUNKSERVER_URL}/chunks/test_txt_chunk1", params={"data": "Hello!"})
    assert r.status_code == 200
    print("✅ test_save_chunk passed")

def test_get_chunk():
    r = requests.get(f"{CHUNKSERVER_URL}/chunks/test_txt_chunk1")
    assert r.json()["data"] == "Hello!"
    print("✅ test_get_chunk passed")

def test_delete_file():
    r = requests.delete(f"{MASTER_URL}/files/test.txt")
    assert r.status_code == 200
    print("✅ test_delete_file passed")

def test_file_gone():
    r = requests.get(f"{MASTER_URL}/files")
    assert "test.txt" not in r.json()["files"]
    print("✅ test_file_gone passed")

print("=== Running Mini-GFS Tests ===")
test_upload_file()
test_list_files()
test_save_chunk()
test_get_chunk()
test_delete_file()
test_file_gone()
print("\n✅ All tests passed!")