import asyncio
from contextlib import asynccontextmanager
from typing import Dict, List

import structlog
from fastapi import FastAPI

from .common_api import create_router as create_common_router
from .device import Device, DeviceType
from .discovery import DiscoveryServer
from .management_api import create_router as create_management_router
from .middleware import ErrorHandlerMiddleware, LoggingMiddleware
from .safetymonitor_api import create_router as create_safetymonitor_router

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
    def __init__(self, devices: List[Device]):
        number_by_type: Dict[DeviceType, int] = {}

        for d in devices:
            d.device_number = number_by_type.get(d.device_type, 0)
            number_by_type[d.device_type] = d.device_number + 1

        self.devices = devices

    def create_app(self, http_port: int):
        self.app = FastAPI(lifespan=_start_discovery_server(http_port))

        self.app.add_middleware(LoggingMiddleware, logger=logger)
        self.app.add_middleware(ErrorHandlerMiddleware)

        self.app.include_router(
            create_management_router(self.devices),
            prefix="/management",
        )

        self.app.include_router(create_common_router(self.devices), prefix="/api/v1")
        self.app.include_router(
            create_safetymonitor_router(self.devices), prefix="/api/v1"
        )

        return self.app
