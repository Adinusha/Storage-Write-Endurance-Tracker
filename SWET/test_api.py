import requests

BASE_URL = "http://127.0.0.1:8000"

def send_write_event(sdcard_id, bytes_written):
    response = requests.post(
        f"{BASE_URL}/api/write-event/",
        json={"sdcard": sdcard_id, "bytes_written": bytes_written}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


send_write_event(sdcard_id=2, bytes_written=900_000)