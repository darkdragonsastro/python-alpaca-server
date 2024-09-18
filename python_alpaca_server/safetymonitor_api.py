from typing import Annotated, List

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from .device import Device, SafetyMonitor, UrlDeviceType, device_finder
from .response import CommonRequest, Response, common_endpoint_parameters

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

        logger.info("test", req=req, device=device)

        if isinstance(device, SafetyMonitor):
            return Response[bool].from_request(
                req,
                device.get_issafe(),
            )
        else:
            raise HTTPException(status_code=404)

    return router
