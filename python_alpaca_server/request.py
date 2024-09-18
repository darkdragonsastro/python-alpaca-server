import threading
from typing import Any

import structlog
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

counter_lock = threading.Lock()
counter = 0


def _server_transaction_id() -> int:
    global counter

    with counter_lock:
        counter += 1

    return counter


def _lenient_int_validator(value: Any) -> int:
    if value is not None:
        try:
            return int(value)
        except ValueError:
            return 0

    return 0


def _strict_int_validator(value: Any) -> int:
    if value is not None:
        try:
            return int(value)
        except ValueError:
            raise HTTPException(status_code=400, detail="invalid integer value")

    raise HTTPException(status_code=400, detail="invalid integer value")


def _strict_bool_validator(value) -> bool:
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

    raise HTTPException(status_code=400, detail="invalid boolean value")


def _strict_float_validator(value) -> float:
    if value is not None:
        try:
            return float(value)
        except ValueError:
            raise HTTPException(status_code=400, detail="invalid float value")

    raise HTTPException(status_code=400, detail="invalid float value")


class CommonRequest(BaseModel):
    ClientTransactionID: int = 0
    ClientID: int = 0
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

    _check_ids = field_validator("ClientTransactionID", "ClientID", mode="before")(
        _lenient_int_validator
    )


class ActionRequest(CommonRequest):
    Action: str
    Parameters: str


class CommandRequest(CommonRequest):
    Command: str
    Raw: str


class PutConnectedRequest(CommonRequest):
    Connected: bool

    _check_connected = field_validator("Connected", mode="before")(
        _strict_bool_validator
    )


class PutBrightnessRequest(CommonRequest):
    Brightness: int

    _check_brightness = field_validator("Brightness", mode="before")(
        _strict_int_validator
    )


class PutSlavedRequest(CommonRequest):
    Slaved: bool

    _check_slaved = field_validator("Slaved", mode="before")(_strict_bool_validator)


class PutAltitudeRequest(CommonRequest):
    Altitude: float

    _check_altitude = field_validator("Altitude", mode="before")(
        _strict_float_validator
    )


class PutAzimuthRequest(CommonRequest):
    Azimuth: float

    _check_azimuth = field_validator("Azimuth", mode="before")(_strict_float_validator)


class PutPositionRequest(CommonRequest):
    Position: int

    _check_position = field_validator("Position", mode="before")(_strict_int_validator)


class PutPositionFloatRequest(CommonRequest):
    Position: float

    _check_position = field_validator("Position", mode="before")(
        _strict_float_validator
    )


class PutTempCompRequest(CommonRequest):
    TempComp: int

    _check_tempcomp = field_validator("TempComp", mode="before")(_strict_int_validator)


class PutAveragePeriodRequest(CommonRequest):
    AveragePeriod: float

    _check_average_period = field_validator("AveragePeriod", mode="before")(
        _strict_float_validator
    )


class SensorNameRequest(CommonRequest):
    SensorName: str


class PutReverseRequest(CommonRequest):
    Reverse: bool

    _check_reverse = field_validator("Reverse", mode="before")(_strict_bool_validator)


class IdRequest(CommonRequest):
    Id: int

    _check_id = field_validator("Id", mode="before")(_strict_int_validator)


class PutIdValueRequest(CommonRequest):
    Id: int
    Value: float

    _check_id = field_validator("Id", mode="before")(_strict_int_validator)
    _check_value = field_validator("Value", mode="before")(_strict_float_validator)


class PutIdNameRequest(CommonRequest):
    Id: int
    Name: str

    _check_id = field_validator("Id", mode="before")(_strict_int_validator)


class PutIdStateRequest(CommonRequest):
    Id: int
    State: bool

    _check_id = field_validator("Id", mode="before")(_strict_int_validator)
    _check_state = field_validator("State", mode="before")(_strict_bool_validator)
