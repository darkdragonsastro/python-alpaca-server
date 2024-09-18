from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import CommonRequest, PutPositionFloatRequest, PutReverseRequest


class Rotator(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Rotator, unique_id)

    @abstractmethod
    def get_canreverse(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_ismoving(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_mechanicalposition(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_position(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_reverse(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def put_reverse(self, req: PutReverseRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def get_stepsize(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_targetposition(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def put_halt(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_move(self, req: PutPositionFloatRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_moveabsolute(self, req: PutPositionFloatRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_movemechanical(self, req: PutPositionFloatRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_sync(self, req: PutPositionFloatRequest) -> None:
        raise NotImplementedError(req)
