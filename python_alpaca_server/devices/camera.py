from ..device import Device, DeviceType


class Camera(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Camera, unique_id)
