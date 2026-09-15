from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from backend.models import TelemetryReading
from backend.state import get_device_state, update_device_state

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
    
@app.post("/api/telemetry")
def receive_telemetry(telemetry: TelemetryReading):
    update_device_state(telemetry)
    return{
        "recevied": True,
        "device_id": telemetry.device_id,
        "lateral acceleration": telemetry.accelerometer.y
    }

@app.get("/api/device/{device_id}/state")
def read_device_state(device_id: str):
    state = get_device_state(device_id)

    if state is None:
        raise HTTPException(
            status_code=404,
            detail=f"Device '{device_id}' not found"
        )
    return state

app.mount(
    "/",
    StaticFiles(directory="dashboard", html=True),
    name="dashboard"
)