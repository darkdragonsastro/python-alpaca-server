import sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import HTTPException, Path
from pydantic import BaseModel, field_validator

from .errors import NotImplementedError
from .request import ActionRequest, CommandRequest, CommonRequest, PutConnectedRequest

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class DeviceType(str, Enum):
    Camera = "Camera"
    CoverCalibrator = "CoverCalibrator"
    Dome = "Dome"
    FilterWheel = "FilterWheel"
    Focuser = "Focuser"
    ObservingConditions = "ObservingConditions"
    Rotator = "Rotator"
    SafetyMonitor = "SafetyMonitor"
    Switch = "Switch"
    Telescope = "Telescope"


class UrlDeviceType(str, Enum):
    Camera = "camera"
    CoverCalibrator = "covercalibrator"
    Dome = "dome"
    FilterWheel = "filterwheel"
    Focuser = "focuser"
    ObservingConditions = "observingconditions"
    Rotator = "rotator"
    SafetyMonitor = "safetymonitor"
    Switch = "switch"
    Telescope = "telescope"


class Device(ABC):
    def __init__(self, device_type: DeviceType, unique_id: str):
        self.device_type = device_type
        self.unique_id = unique_id
        self.device_number: int = -1

    @abstractmethod
    def put_action(self, req: ActionRequest) -> str:
        raise NotImplementedError(req)

    @abstractmethod
    def put_command_blind(self, req: CommandRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_command_bool(self, req: CommandRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def put_command_string(self, req: CommandRequest) -> str:
        raise NotImplementedError(req)

    @abstractmethod
    def get_connected(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def put_connected(self, req: PutConnectedRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def get_description(self, req: CommonRequest) -> str:
        raise NotImplementedError(req)

    @abstractmethod
    def get_driverinfo(self, req: CommonRequest) -> str:
        raise NotImplementedError(req)

    @abstractmethod
    def get_driverversion(self, req: CommonRequest) -> str:
        raise NotImplementedError(req)

    @abstractmethod
    def get_interfaceversion(self, req: CommonRequest) -> int:
        raise NotImplementedError(req)

    @abstractmethod
    def get_name(self, req: CommonRequest) -> str:
        raise NotImplementedError(req)

    @abstractmethod
    def get_supportedactions(self, req: CommonRequest) -> List[str]:
        raise NotImplementedError(req)


class PathArgs(BaseModel):
    device_number: int
    device_type: Optional[UrlDeviceType] = None

    @field_validator("device_number", mode="before")
    def check_device_number(cls, value):
        if value is not None:
            try:
                return int(value)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid device number")

        raise HTTPException(status_code=400, detail="Invalid device number")

    @field_validator("device_type", mode="before")
    def check_device_type(cls, value):
        if value is not None:
            try:
                return UrlDeviceType(value)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid device type")

        return None


def device_finder(devices: List[Device], device_type: UrlDeviceType):
    def find_device(
        args: Annotated[PathArgs, Path()],
    ) -> Device:
        logger.debug(
            "looking for device",
            device_type=device_type,
            device_number=args.device_number,
        )
        device: Optional[Device] = None
        for d in devices:
            if (
                d.device_number == args.device_number
                and d.device_type.value.lower() == device_type.value.lower()
            ):
                device = d

        if not device:
            raise HTTPException(status_code=404)

        return device

    return find_device


def common_device_finder(devices: List[Device]):
    def find_device(
        args: Annotated[PathArgs, Path()],
    ) -> Device:
        logger.debug(
            "looking for device",
            device_type=args.device_type,
            device_number=args.device_number,
        )

        if args.device_type is None:
            raise HTTPException(status_code=400, detail="Invalid device type")

        device: Optional[Device] = None
        for d in devices:
            if (
                d.device_number == args.device_number
                and d.device_type.value.lower() == args.device_type.value.lower()
            ):
                device = d

        if not device:
            raise HTTPException(status_code=404)

        return device

    return find_device
