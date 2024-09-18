import threading
from typing import Optional
from pydantic import BaseModel, Field, model_validator, field_validator
import structlog
from fastapi import HTTPException

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

counter_lock = threading.Lock()
counter = 0


def _server_transaction_id() -> int:
    global counter

    with counter_lock:
        counter += 1

    return counter


class CommonRequest(BaseModel):
    ClientTransactionID: Optional[int] = None
    ClientID: Optional[int] = None
    ServerTransactionID: int = Field(default_factory=_server_transaction_id)

    @model_validator(mode="before")
    @classmethod
    def body_params_case_insensitive(cls, values: dict):
        for field in cls.model_fields:
            in_fields = list(
                filter(lambda f: f.lower() == field.lower(), values.keys())
            )
            for in_field in in_fields:
                values[field] = values.pop(in_field)

        return values

    @field_validator("ClientTransactionID", "ClientID", mode="before")
    @classmethod
    def check_int_not_required(cls, value):
        if value is not None:
            try:
                return int(value)
            except ValueError:
                return 0


class ActionRequest(CommonRequest):
    Action: str
    Parameters: str


class CommandRequest(CommonRequest):
    Command: str
    Raw: str


class PutConnectedRequest(CommonRequest):
    Connected: bool

    @field_validator("Connected", mode="before")
    @classmethod
    def check_bool(cls, value):
        if value is not None:
            if isinstance(value, str):
                if value.lower() in ["true", "1"]:
                    return True
                elif value.lower() in ["false", "0"]:
                    return False
            elif isinstance(value, int):
                if value == 1:
                    return True
                elif value == 0:
                    return False
            elif isinstance(value, bool):
                return value
        raise HTTPException(status_code=400, detail="Invalid value for Connected")


class PutBrightnessRequest(BaseModel):
    Brightness: int

    @field_validator("Brightness", mode="before")
    @classmethod
    def check_int(cls, value):
        if value is not None:
            try:
                return int(value)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Invalid value for Brightness"
                )


class PutSlavedRequest(CommonRequest):
    Slaved: bool

    @field_validator("Slaved", mode="before")
    @classmethod
    def check_bool(cls, value):
        if value is not None:
            if isinstance(value, str):
                if value.lower() in ["true", "1"]:
                    return True
                elif value.lower() in ["false", "0"]:
                    return False
            elif isinstance(value, int):
                if value == 1:
                    return True
                elif value == 0:
                    return False
            elif isinstance(value, bool):
                return value
        raise HTTPException(status_code=400, detail="Invalid value for Slaved")


class PutAltitudeRequest(BaseModel):
    Altitude: float

    @field_validator("Altitude", mode="before")
    @classmethod
    def check_float(cls, value):
        if value is not None:
            try:
                return float(value)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Invalid value for Altitude"
                )


class PutAzimuthRequest(BaseModel):
    Azimuth: float

    @field_validator("Azimuth", mode="before")
    @classmethod
    def check_float(cls, value):
        if value is not None:
            try:
                return float(value)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid value for Azimuth")
