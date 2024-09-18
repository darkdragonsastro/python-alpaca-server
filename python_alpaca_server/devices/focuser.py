from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import CommonRequest, PutPositionRequest, PutTempCompRequest


class Focuser(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Focuser, unique_id)

    @abstractmethod
    def get_absolute(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_ismoving(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_maxincrement(self, req: CommonRequest) -> int:
        raise NotImplementedError(req)

    @abstractmethod
    def get_maxstep(self, req: CommonRequest) -> int:
        raise NotImplementedError(req)

    @abstractmethod
    def get_position(self, req: CommonRequest) -> int:
        raise NotImplementedError(req)

    @abstractmethod
    def get_stepsize(self, req: CommonRequest) -> int:
        raise NotImplementedError(req)

    @abstractmethod
    def get_tempcomp(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def put_tempcomp(self, req: PutTempCompRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def get_tempcompavailable(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_temperature(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def put_halt(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_move(self, req: PutPositionRequest) -> None:
        raise NotImplementedError(req)
