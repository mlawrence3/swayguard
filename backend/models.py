from datetime import datetime
from pydantic import BaseModel, Field

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