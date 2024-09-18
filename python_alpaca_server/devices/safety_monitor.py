from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import CommonRequest


class SafetyMonitor(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.SafetyMonitor, unique_id)

    @abstractmethod
    def get_issafe(self, req: CommonRequest) -> bool:
        raise NotImplementedError(req)
