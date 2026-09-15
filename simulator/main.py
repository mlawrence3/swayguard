import random
import time
from datetime import datetime, timezone

import httpx

API_URL = "http://127.0.0.1:8000/api/telemetry"
DEVICE_ID = "trailer-002"
TELEMETRY_INTERVAL_SECONDS = 1

def generate_telemetry():
    return{
        "device_id": DEVICE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "speed_mph": round(random.uniform(58.0, 62.0), 2),
        "accelerometer": {
            "x": round(random.uniform(-0.03, 0.03), 3),
            "y": round(random.uniform(-0.05, 0.05), 3),
            "z": round(random.uniform(0.98, 1.02), 3)
        },
        "gyroscope": {
            "yaw_rate": round(random.uniform(-1.0, 1.0), 2)
        }
    }

def send_telemetry(client, telemetry):
    response = client.post(API_URL, json=telemetry)
    response.raise_for_status()
    return response.json()

def main():
    print(f"Starting SwayGuard simulator for {DEVICE_ID}")
    print(f"Sending telemtry to {API_URL}")

    with httpx.Client() as client:
        while True:
            telemetry = generate_telemetry()

            try:
                response = send_telemetry(client, telemetry)

                print(
                    f"speed={telemetry['speed_mph']:>5.2f} mph | "
                    f"lateral={telemetry['accelerometer']['y']:>6.3f} g | "
                    f"yaw={telemetry['gyroscope']['yaw_rate']:>5.2f} deg/s | "
                    f"stats=sent"
                )
            except httpx.HTTPError as error:
                print(f"Telemetry transmission failed: {error}")

            time.sleep(TELEMETRY_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()