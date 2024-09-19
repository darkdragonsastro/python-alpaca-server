from typing import List

from .app import AlpacaServer, Description
from .devices.safetymonitor import SafetyMonitor
from .errors import NotImplementedError
from .request import ActionRequest, CommandRequest, CommonRequest, PutConnectedRequest


class MySafetyMonitor(SafetyMonitor):
    def __init__(self, unique_id: str):
        super().__init__(unique_id)
        self._connected = False

    def put_action(self, req: ActionRequest) -> str:
        raise NotImplementedError(req)

    def put_command_blind(self, req: CommandRequest) -> None:
        raise NotImplementedError(req)

    def put_command_bool(self, req: CommandRequest) -> bool:
        raise NotImplementedError(req)

    def put_command_string(self, req: CommandRequest) -> str:
        raise NotImplementedError(req)

    def get_connected(self, req: CommonRequest) -> bool:
        return self._connected

    def put_connected(self, req: PutConnectedRequest) -> None:
        self._connected = req.Connected

    def get_description(self, req: CommonRequest) -> str:
        return "My Description"

    def get_driverinfo(self, req: CommonRequest) -> str:
        return "My Driver Info"

    def get_driverversion(self, req: CommonRequest) -> str:
        return "0.1.0"

    def get_interfaceversion(self, req: CommonRequest) -> int:
        return 1

    def get_name(self, req: CommonRequest) -> str:
        return "MySafetyMonitor"

    def get_supportedactions(self, req: CommonRequest) -> List[str]:
        return []

    def get_issafe(self, req: CommonRequest) -> bool:
        if not self._connected:
            return False

        return True


def get_server_description() -> Description:
    return Description(
        ServerName="MyServer",
        Manufacturer="MyManufacturer",
        ManufacturerVersion="0.1.0",
        Location="MyLocation",
    )


if __name__ == "__main__":
    import uvicorn

    port = 8000

    svr = AlpacaServer(get_server_description, [MySafetyMonitor("other")])
    app = svr.create_app(port)

    try:
        uvicorn.run(app, host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        pass
