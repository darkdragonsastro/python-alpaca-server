import sys
from typing import List

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import APIRouter, Depends, Query

from ..device import Device, UrlDeviceType, device_finder
from ..devices.safetymonitor import SafetyMonitor
from ..request import CommonRequest
from ..response import Response, common_endpoint_parameters

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def create_router(devices: List[Device]):
    router = APIRouter()

    async def get_issafe(
        req: Annotated[CommonRequest, Query()],
        device: SafetyMonitor = Depends(
            device_finder(devices, UrlDeviceType.SafetyMonitor)
        ),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_issafe(req),
        )

    router.get(
        "/safetymonitor/{device_number}/issafe",
        **common_endpoint_parameters,
    )(get_issafe)

    return router
