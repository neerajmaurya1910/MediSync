"""Data models shared by the server and every client device."""
import time
import uuid
from dataclasses import dataclass, field, asdict


@dataclass
class Vitals:
    heart_rate: int    # beats per minute
    systolic_bp: int   # mmHg
    resp_rate: int     # breaths per minute
    spo2: int          # oxygen saturation, %
    temp_c: float      # degrees Celsius


@dataclass
class Patient:
    name: str
    age: int
    complaint: str
    vitals: Vitals
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    priority: int = 5          # 1 = most urgent ... 5 = least urgent
    created_at: float = field(default_factory=time.time)
    version: int = 0           # set by the server on every change

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        data = dict(data)
        data["vitals"] = Vitals(**data["vitals"])
        return cls(**data)
