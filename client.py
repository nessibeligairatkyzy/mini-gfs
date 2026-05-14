import requests

MASTER_URL = "http://localhost:8080"

def list_files():
    r = requests.get(f"{MASTER_URL}/files")
    print("Файлы:", r.json())

def upload_file(filename):
    r = requests.post(f"{MASTER_URL}/files/{filename}")
    print("Загружено:", r.json())

def get_file(filename):
    r = requests.get(f"{MASTER_URL}/files/{filename}")
    print("Файл:", r.json())

def delete_file(filename):
    r = requests.delete(f"{MASTER_URL}/files/{filename}")
    print("Удалено:", r.json())


print("=== Mini-GFS Client ===")
upload_file("test.txt")
upload_file("photo.jpg")
list_files()
get_file("test.txt")
delete_file("test.txt")
list_files()