from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import (
    CommonRequest,
    IdRequest,
    PutIdNameRequest,
    PutIdStateRequest,
    PutIdValueRequest,
)


class Switch(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Switch, unique_id)

    @abstractmethod
    def get_maxswitch(self, req: CommonRequest) -> int:
        raise NotImplementedError(req)

    @abstractmethod
    def get_canwrite(self, req: IdRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_getswitch(self, req: IdRequest) -> bool:
        raise NotImplementedError(req)

    @abstractmethod
    def get_getswitchdescription(self, req: IdRequest) -> str:
        raise NotImplementedError(req)

    @abstractmethod
    def get_getswitchname(self, req: IdRequest) -> str:
        raise NotImplementedError(req)

    @abstractmethod
    def get_getswitchvalue(self, req: IdRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_minswitchvalue(self, req: IdRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_maxswitchvalue(self, req: IdRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def put_setswitch(self, req: PutIdStateRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_setswitchname(self, req: PutIdNameRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def put_setswitchvalue(self, req: PutIdValueRequest) -> None:
        raise NotImplementedError(req)
