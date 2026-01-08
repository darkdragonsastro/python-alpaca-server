import asyncio
from contextlib import asynccontextmanager
from typing import Callable, Dict, List, Union

import structlog
from fastapi import FastAPI

from .api.common import create_router as create_common_router
from .api.covercalibrator import create_router as create_covercalibrator_router
from .api.dome import create_router as create_dome_router
from .api.filterwheel import create_router as create_filterwheel_router
from .api.focuser import create_router as create_focuser_router
from .api.management import Description
from .api.management import create_router as create_management_router
from .api.observingconditions import create_router as create_observingconditions_router
from .api.rotator import create_router as create_rotator_router
from .api.safetymonitor import create_router as create_safetymonitor_router
from .api.switch import create_router as create_switch_router
from .device import Device, DeviceType
from .discovery import DiscoveryServer
from .middleware import ErrorHandlerMiddleware

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def _start_discovery_server(http_port: int):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            discovery_server = DiscoveryServer(http_port)
            task = asyncio.create_task(discovery_server.start())
            yield
        finally:
            task.cancel()

    return lifespan


class AlpacaServer:
    def __init__(
        self,
        server_description: Union[Callable[[], Description], Description],
        devices: List[Device],
    ):
        number_by_type: Dict[DeviceType, int] = {}

        for d in devices:
            d.device_number = number_by_type.get(d.device_type, 0)
            number_by_type[d.device_type] = d.device_number + 1

        self.devices = devices
        self.server_description = server_description

    def create_app(self, http_port: int):
        self.app = FastAPI(lifespan=_start_discovery_server(http_port))

        self.app.add_middleware(ErrorHandlerMiddleware)

        self.app.include_router(
            create_management_router(self.server_description, self.devices),
            prefix="/management",
        )
        self.app.include_router(
            create_common_router(self.devices),
            prefix="/api/v1",
        )

        # Determine which device types are present
        device_types_present = {d.device_type for d in self.devices}

        # Conditionally register routers for each device type
        if DeviceType.SafetyMonitor in device_types_present:
            self.app.include_router(
                create_safetymonitor_router(self.devices),
                prefix="/api/v1",
            )

        if DeviceType.ObservingConditions in device_types_present:
            self.app.include_router(
                create_observingconditions_router(self.devices),
                prefix="/api/v1",
            )

        if DeviceType.Dome in device_types_present:
            self.app.include_router(
                create_dome_router(self.devices),
                prefix="/api/v1",
            )

        if DeviceType.Focuser in device_types_present:
            self.app.include_router(
                create_focuser_router(self.devices),
                prefix="/api/v1",
            )

        if DeviceType.FilterWheel in device_types_present:
            self.app.include_router(
                create_filterwheel_router(self.devices),
                prefix="/api/v1",
            )

        if DeviceType.Rotator in device_types_present:
            self.app.include_router(
                create_rotator_router(self.devices),
                prefix="/api/v1",
            )

        if DeviceType.CoverCalibrator in device_types_present:
            self.app.include_router(
                create_covercalibrator_router(self.devices),
                prefix="/api/v1",
            )

        if DeviceType.Switch in device_types_present:
            self.app.include_router(
                create_switch_router(self.devices),
                prefix="/api/v1",
            )

        return self.app
