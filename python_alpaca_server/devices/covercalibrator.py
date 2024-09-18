from abc import abstractmethod
from enum import Enum

from ..device import Device, DeviceType
from ..request import CommonRequest, PutBrightnessRequest


class CalibratorState(int, Enum):
    NotPresent = 0
    Off = 1
    NotReady = 2
    Ready = 3
    Unknown = 4
    Error = 5


class CoverState(int, Enum):
    NotPresent = 0
    Closed = 1
    Moving = 2
    Open = 3
    Unknown = 4
    Error = 5


class CoverCalibrator(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.CoverCalibrator, unique_id)

    @abstractmethod
    def get_brightness(self, req: CommonRequest) -> int:
        raise NotImplementedError(req)

    @abstractmethod
    def get_calibratorstate(self, req: CommonRequest) -> CalibratorState:
        raise NotImplementedError(req)

    @abstractmethod
    def get_coverstate(self, req: CommonRequest) -> CoverState:
        raise NotImplementedError(req)

    @abstractmethod
    def get_maxbrightness(self, req: CommonRequest) -> int:
        raise NotImplementedError(req)

    @abstractmethod
    def put_calibratoroff(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_calibratoron(self, req: PutBrightnessRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_closecover(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_haltcover(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_opencover(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)
