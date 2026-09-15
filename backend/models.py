from datetime import datetime
from pydantic import BaseModel, Field, model_validator

class AccelerometerReading(BaseModel):
    x: float
    y: float
    z: float
    

class GyroscopeReading(BaseModel):
    yaw_rate: float
    


class TelemetryReading(BaseModel):
    device_id: str
    timestamp: datetime
    speed_mph: float = Field(ge=0)
    accelerometer: AccelerometerReading
    gyroscope: GyroscopeReading

class DeviceSettings(BaseModel):
    warning_threshold_g: float = Field(gt=0)
    alert_threshold_g: float = Field(gt=0)
    brake_force_percent: int = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_thresholds(self):
        if self.warning_threshold_g >= self.alert_threshold_g:
            raise ValueError(
                "Warning threshold must be less than alert threshold"
            )

        return self