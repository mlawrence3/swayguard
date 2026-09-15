from backend.models import DeviceSettings


DEFAULT_SETTINGS = DeviceSettings(
    warning_threshold_g=0.20,
    alert_threshold_g=0.30,
    brake_force_percent=40
)

device_settings: dict[str, DeviceSettings] = {}

def get_device_settings(device_id: str):
    return device_settings.get(device_id, DEFAULT_SETTINGS)

def update_device_settings(
        device_id: str,
        settings: DeviceSettings
):
    device_settings[device_id] = settings
    return settings