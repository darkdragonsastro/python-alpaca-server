from abc import abstractmethod
from typing import List

from ..device import Device, DeviceType
from ..request import CommonRequest, PutPositionRequest


class FilterWheel(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.FilterWheel, unique_id)

    @abstractmethod
    def get_focusoffsets(self, req: CommonRequest) -> List[int]:
        raise NotImplementedError(req)

    @abstractmethod
    def get_names(self, req: CommonRequest) -> List[str]:
        raise NotImplementedError(req)

    @abstractmethod
    def get_position(self, req: CommonRequest) -> int:
        raise NotImplementedError(req)

    @abstractmethod
    def put_position(self, req: PutPositionRequest) -> None:
        raise NotImplementedError(req)
