from backend.models import TelemetryReading

device_states: dict[str, TelemetryReading] = {}

def update_device_state(telemetry: TelemetryReading):
    device_states[telemetry.device_id] = telemetry

def get_device_state(device_id: str):
    return device_states.get(device_id)