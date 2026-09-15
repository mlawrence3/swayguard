from fastapi import FastAPI
from backend.models import TelemetryReading

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
    
@app.post("/api/devices/telemetry")
def receive_telemetry(telemetry: TelemetryReading):
    return{
        "recevied": True,
        "device_id": telemetry.device_id,
        "lateral acceleration": telemetry.accelerometer.y
    }