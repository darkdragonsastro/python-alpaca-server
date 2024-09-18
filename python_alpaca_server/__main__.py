from typing import List

from .app import AlpacaServer
from .device import SafetyMonitor


class MySafetyMonitor(SafetyMonitor):
    def __init__(self, unique_id: str):
        super().__init__(unique_id)
        self._connected = False

    def get_connected(self) -> bool:
        return self._connected

    def put_connected(self, connected: bool) -> None:
        self._connected = connected

    def get_description(self) -> str:
        return "My Description"

    def get_driverinfo(self) -> str:
        return "My Driver Info"

    def get_driverversion(self) -> str:
        return "0.1.0"

    def get_interfaceversion(self) -> int:
        return 1

    def get_name(self) -> str:
        return "MySafetyMonitor"

    def get_supportedactions(self) -> List[str]:
        return []

    def get_issafe(self) -> bool:
        return True


if __name__ == "__main__":
    import uvicorn

    svr = AlpacaServer([MySafetyMonitor("other")])

    app = svr.create_app(8000)

    uvicorn.run(app, host="0.0.0.0", port=8000)
