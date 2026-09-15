from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from backend.models import TelemetryReading
from backend.state import get_device_state, update_device_state
from backend.models import DeviceSettings, TelemetryReading
from backend.settings import get_device_settings, update_device_settings

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

@app.get("/api/devices/{device_id}/settings")
def read_device_settings(device_id: str):
    return get_device_settings(device_id)


@app.put("/api/devices/{device_id}/settings")
def write_device_settings(
    device_id: str,
    settings: DeviceSettings
):
    return update_device_settings(device_id, settings)

app.mount(
    "/",
    StaticFiles(directory="dashboard", html=True),
    name="dashboard"
)