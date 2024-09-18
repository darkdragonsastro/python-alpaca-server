from typing import Annotated, List

import structlog
from fastapi import APIRouter, Depends, Query

from ..device import Device, UrlDeviceType, device_finder
from ..devices.switch import Switch
from ..request import (
    CommonRequest,
    IdRequest,
    PutIdNameRequest,
    PutIdStateRequest,
    PutIdValueRequest,
)
from ..response import Response, common_endpoint_parameters

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def create_router(devices: List[Device]):
    router = APIRouter()

    async def get_maxswitch(
        req: Annotated[CommonRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[int]:
        return Response[int].from_request(
            req,
            device.get_maxswitch(req),
        )

    async def get_canwrite(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_canwrite(req),
        )

    async def get_getswitch(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_getswitch(req),
        )

    async def get_getswitchdescription(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[str]:
        return Response[str].from_request(
            req,
            device.get_getswitchdescription(req),
        )

    async def get_getswitchname(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[str]:
        return Response[str].from_request(
            req,
            device.get_getswitchname(req),
        )

    async def get_getswitchvalue(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_getswitchvalue(req),
        )

    async def get_minswitchvalue(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_minswitchvalue(req),
        )

    async def get_maxswitchvalue(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_maxswitchvalue(req),
        )

    async def put_setswitch(
        req: Annotated[PutIdStateRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_setswitch(req),
        )

    async def put_setswitchname(
        req: Annotated[PutIdNameRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_setswitchname(req),
        )

    async def put_setswitchvalue(
        req: Annotated[PutIdValueRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_setswitchvalue(req),
        )

    router.get(
        "/switch/{device_number}/maxswitch",
        **common_endpoint_parameters,
    )(get_maxswitch)

    return router
