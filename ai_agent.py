import requests
from datetime import datetime

MASTER_URL = "http://localhost:8080"

CHUNKSERVERS = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
]


def check_server(url):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return "ONLINE"
    except requests.RequestException:
        pass

    return "OFFLINE"


def generate_ai_recommendation(master_status, alive_chunkservers):
    if master_status == "OFFLINE":
        return (
            "CRITICAL: Master server is offline. "
            "Restart master.py first because metadata service is unavailable."
        )

    if alive_chunkservers == 3:
        return (
            "Cluster is healthy. All chunkservers are online and replication is available."
        )

    if alive_chunkservers == 2:
        return (
            "Warning: One chunkserver is offline. "
            "The system can still work, but restart the failed node to restore full replication."
        )

    if alive_chunkservers == 1:
        return (
            "High risk: Only one chunkserver is online. "
            "Replication is weak, and data availability may be affected."
        )

    return (
        "CRITICAL: No chunkservers are online. "
        "File storage is unavailable. Restart chunkservers immediately."
    )


def main():
    print("===== MINI-GFS AI CLUSTER REPORT =====")
    print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    master_status = check_server(MASTER_URL)
    print(f"Master Server: {master_status}")

    alive_chunkservers = 0

    for index, server in enumerate(CHUNKSERVERS, start=1):
        status = check_server(server)
        print(f"Chunkserver {index}: {status}")

        if status == "ONLINE":
            alive_chunkservers += 1

    print()
    print("AI Analysis:")
    print(generate_ai_recommendation(master_status, alive_chunkservers))


if __name__ == "__main__":
    main()