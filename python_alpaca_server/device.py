from abc import ABC, abstractmethod
from enum import Enum
from typing import Annotated, List, Optional

import structlog
from fastapi import HTTPException, Path

from .errors import NotImplementedError
from .request import CommonRequest, ActionRequest, PutConnectedRequest, CommandRequest

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

    def put_action(self, req: ActionRequest) -> str:
        raise NotImplementedError(req)

    def put_command_blind(self, req: CommandRequest) -> None:
        raise NotImplementedError(req)

    def put_command_bool(self, req: CommandRequest) -> bool:
        raise NotImplementedError(req)

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


class SafetyMonitor(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.SafetyMonitor, unique_id)

    @abstractmethod
    def get_issafe(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)


def test(device_type: Annotated[str, Path()]):
    logger.info("find device")


def device_finder(devices: List[Device], device_type: UrlDeviceType):
    def find_device(
        device_number: Annotated[int, Path()],
        device_type: Annotated[UrlDeviceType, Path()] = device_type,
    ) -> Device:
        logger.debug(
            "looking for device", device_type=device_type, device_number=device_number
        )
        device: Optional[Device] = None
        for d in devices:
            if (
                d.device_number == device_number
                and d.device_type.value.lower() == device_type.value.lower()
            ):
                logger.debug("found device")
                device = d

        if not device:
            raise HTTPException(status_code=404)

        return device

    return find_device


def common_device_finder(devices: List[Device]):
    def find_device(
        device_number: Annotated[int, Path()],
        device_type: Annotated[UrlDeviceType, Path()],
    ) -> Device:
        logger.debug(
            "looking for device", device_type=device_type, device_number=device_number
        )
        device: Optional[Device] = None
        for d in devices:
            if (
                d.device_number == device_number
                and d.device_type.value.lower() == device_type.value.lower()
            ):
                logger.debug("found device")
                device = d

        if not device:
            raise HTTPException(status_code=404)

        return device

    return find_device
