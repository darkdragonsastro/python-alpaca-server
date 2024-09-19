import sys
from typing import List

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import APIRouter, Depends, Query

from ..device import Device, UrlDeviceType, device_finder
from ..devices.focuser import Focuser
from ..request import CommonRequest, PutPositionRequest, PutTempCompRequest
from ..response import Response, common_endpoint_parameters

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def create_router(devices: List[Device]):
    router = APIRouter()

    async def get_absolute(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_absolute(req),
        )

    async def get_ismoving(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_ismoving(req),
        )

    async def get_maxincrement(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[int]:
        return Response[int].from_request(
            req,
            device.get_maxincrement(req),
        )

    async def get_maxstep(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[int]:
        return Response[int].from_request(
            req,
            device.get_maxstep(req),
        )

    async def get_position(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[int]:
        return Response[int].from_request(
            req,
            device.get_position(req),
        )

    async def get_stepsize(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[int]:
        return Response[int].from_request(
            req,
            device.get_stepsize(req),
        )

    async def get_tempcomp(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_tempcomp(req),
        )

    async def put_tempcomp(
        req: Annotated[PutTempCompRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_tempcomp(req),
        )

    async def get_tempcompavailable(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_tempcompavailable(req),
        )

    async def get_temperature(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_temperature(req),
        )

    async def put_halt(
        req: Annotated[CommonRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_halt(req),
        )

    async def put_move(
        req: Annotated[PutPositionRequest, Query()],
        device: Focuser = Depends(device_finder(devices, UrlDeviceType.Focuser)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_move(req),
        )

    router.get(
        "/focuser/{device_number}/absolute",
        **common_endpoint_parameters,
    )(get_absolute)

    router.get(
        "/focuser/{device_number}/ismoving",
        **common_endpoint_parameters,
    )(get_ismoving)

    router.get(
        "/focuser/{device_number}/maxincrement",
        **common_endpoint_parameters,
    )(get_maxincrement)

    router.get(
        "/focuser/{device_number}/maxstep",
        **common_endpoint_parameters,
    )(get_maxstep)

    router.get(
        "/focuser/{device_number}/position",
        **common_endpoint_parameters,
    )(get_position)

    router.get(
        "/focuser/{device_number}/stepsize",
        **common_endpoint_parameters,
    )(get_stepsize)

    router.get(
        "/focuser/{device_number}/tempcomp",
        **common_endpoint_parameters,
    )(get_tempcomp)

    router.put(
        "/focuser/{device_number}/tempcomp",
        **common_endpoint_parameters,
    )(put_tempcomp)

    router.get(
        "/focuser/{device_number}/tempcompavailable",
        **common_endpoint_parameters,
    )(get_tempcompavailable)

    router.get(
        "/focuser/{device_number}/temperature",
        **common_endpoint_parameters,
    )(get_temperature)

    router.put(
        "/focuser/{device_number}/halt",
        **common_endpoint_parameters,
    )(put_halt)

    router.put(
        "/focuser/{device_number}/move",
        **common_endpoint_parameters,
    )(put_move)

    return router
