from typing import List, override

from .app import AlpacaServer, Description
from .devices.safetymonitor import SafetyMonitor
from .request import ActionRequest, CommandRequest, CommonRequest, PutConnectedRequest


class MySafetyMonitor(SafetyMonitor):
    def __init__(self, unique_id: str):
        super().__init__(unique_id)
        self._connected = False

    @override
    def put_action(self, req: ActionRequest) -> str:
        raise NotImplementedError(req)

    @override
    def put_command_blind(self, req: CommandRequest) -> None:
        raise NotImplementedError(req)

    @override
    def put_command_bool(self, req: CommandRequest) -> bool:
        raise NotImplementedError(req)

    @override
    def put_command_string(self, req: CommandRequest) -> str:
        raise NotImplementedError(req)

    @override
    def get_connected(self, req: CommonRequest) -> bool:
        return self._connected

    @override
    def put_connected(self, req: PutConnectedRequest) -> None:
        self._connected = req.Connected

    @override
    def get_description(self, req: CommonRequest) -> str:
        return "My Description"

    @override
    def get_driverinfo(self, req: CommonRequest) -> str:
        return "My Driver Info"

    @override
    def get_driverversion(self, req: CommonRequest) -> str:
        return "0.1.0"

    @override
    def get_interfaceversion(self, req: CommonRequest) -> int:
        return 1

    @override
    def get_name(self, req: CommonRequest) -> str:
        return "MySafetyMonitor"

    @override
    def get_supportedactions(self, req: CommonRequest) -> List[str]:
        return []

    @override
    def get_issafe(self, req: CommonRequest) -> bool:
        if not self._connected:
            return False

        return False


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
