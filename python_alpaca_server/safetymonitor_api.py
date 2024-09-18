from typing import Annotated, List

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from .device import Device, UrlDeviceType, device_finder
from .devices.safety_monitor import SafetyMonitor
from .response import Response, common_endpoint_parameters
from .request import CommonRequest

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class Action(BaseModel):
    Action: str
    Parameters: str


def create_router(devices: List[Device]):
    router = APIRouter()

    @router.get(
        "/safetymonitor/{device_number}/issafe",
        **common_endpoint_parameters,
    )
    async def get_issafe(
        req: Annotated[CommonRequest, Query()],
        device: Device = Depends(device_finder(devices, UrlDeviceType.SafetyMonitor)),
    ) -> Response[bool]:

        if isinstance(device, SafetyMonitor):
            return Response[bool].from_request(
                req,
                device.get_issafe(req),
            )
        else:
            raise HTTPException(status_code=404)

    return router
