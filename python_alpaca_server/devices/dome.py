from abc import abstractmethod
from enum import Enum

from ..device import Device, DeviceType
from ..request import (
    CommonRequest,
    PutAltitudeRequest,
    PutAzimuthRequest,
    PutSlavedRequest,
)


class ShutterState(int, Enum):
    Open = 0
    Closed = 1
    Opening = 2
    Closing = 3
    Error = 4


class Dome(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Dome, unique_id)

    @abstractmethod
    def get_altitude(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_athome(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_atpark(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_azimuth(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_canfindhome(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_canpark(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansetaltitude(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansetazimuth(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansetpark(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansetshutter(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_canslave(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansyncazimuth(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_shutterstatus(self, req: CommonRequest) -> ShutterState:
        raise NotImplementedError(req)

    @abstractmethod
    def get_slaved(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def put_slaved(self, req: PutSlavedRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def get_slewing(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def put_abortslew(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_closeshutter(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_findhome(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_openshutter(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_park(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_setpark(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_slewtoaltitude(self, req: PutAltitudeRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_slewtoazimuth(self, req: PutAzimuthRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_synctoazimuth(self, req: PutAzimuthRequest) -> None:
        raise NotImplementedError(req)
