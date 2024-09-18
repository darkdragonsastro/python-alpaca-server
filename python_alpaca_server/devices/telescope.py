from ..device import Device, DeviceType


class Telescope(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Telescope, unique_id)
