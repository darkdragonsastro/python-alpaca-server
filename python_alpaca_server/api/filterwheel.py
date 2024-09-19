import sys
from typing import List

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import APIRouter, Depends, Query

from ..device import Device, UrlDeviceType, device_finder
from ..devices.filterwheel import FilterWheel
from ..request import CommonRequest, PutPositionRequest
from ..response import Response, common_endpoint_parameters

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def create_router(devices: List[Device]):
    router = APIRouter()

    async def get_focusoffsets(
        req: Annotated[CommonRequest, Query()],
        device: FilterWheel = Depends(
            device_finder(devices, UrlDeviceType.FilterWheel)
        ),
    ) -> Response[List[int]]:
        return Response[List[int]].from_request(
            req,
            device.get_focusoffsets(req),
        )

    async def get_names(
        req: Annotated[CommonRequest, Query()],
        device: FilterWheel = Depends(
            device_finder(devices, UrlDeviceType.FilterWheel)
        ),
    ) -> Response[List[str]]:
        return Response[List[str]].from_request(
            req,
            device.get_names(req),
        )

    async def get_position(
        req: Annotated[CommonRequest, Query()],
        device: FilterWheel = Depends(
            device_finder(devices, UrlDeviceType.FilterWheel)
        ),
    ) -> Response[int]:
        return Response[int].from_request(
            req,
            device.get_position(req),
        )

    async def put_position(
        req: Annotated[PutPositionRequest, Query()],
        device: FilterWheel = Depends(
            device_finder(devices, UrlDeviceType.FilterWheel)
        ),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_position(req),
        )

    router.get(
        "/filterwheel/{device_number}/focusoffsets",
        **common_endpoint_parameters,
    )(get_focusoffsets)

    router.get(
        "/filterwheel/{device_number}/names",
        **common_endpoint_parameters,
    )(get_names)

    router.get(
        "/filterwheel/{device_number}/position",
        **common_endpoint_parameters,
    )(get_position)

    router.put(
        "/filterwheel/{device_number}/position",
        **common_endpoint_parameters,
    )(put_position)

    return router
