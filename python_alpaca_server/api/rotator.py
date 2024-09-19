import sys
from typing import List

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import APIRouter, Depends, Query

from ..device import Device, UrlDeviceType, device_finder
from ..devices.rotator import Rotator
from ..request import CommonRequest, PutPositionFloatRequest, PutReverseRequest
from ..response import Response, common_endpoint_parameters

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def create_router(devices: List[Device]):
    router = APIRouter()

    async def get_canreverse(
        req: Annotated[CommonRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_canreverse(req),
        )

    async def get_ismoving(
        req: Annotated[CommonRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_ismoving(req),
        )

    async def get_mechanicalposition(
        req: Annotated[CommonRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_mechanicalposition(req),
        )

    async def get_position(
        req: Annotated[CommonRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_position(req),
        )

    async def get_reverse(
        req: Annotated[CommonRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_reverse(req),
        )

    async def put_reverse(
        req: Annotated[PutReverseRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_reverse(req),
        )

    async def get_stepsize(
        req: Annotated[CommonRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_stepsize(req),
        )

    async def get_targetposition(
        req: Annotated[CommonRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_targetposition(req),
        )

    async def put_halt(
        req: Annotated[CommonRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_halt(req),
        )

    async def put_move(
        req: Annotated[PutPositionFloatRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_move(req),
        )

    async def put_moveabsolute(
        req: Annotated[PutPositionFloatRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_moveabsolute(req),
        )

    async def put_movemechanical(
        req: Annotated[PutPositionFloatRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_movemechanical(req),
        )

    async def put_sync(
        req: Annotated[PutPositionFloatRequest, Query()],
        device: Rotator = Depends(device_finder(devices, UrlDeviceType.Rotator)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_sync(req),
        )

    router.get(
        "/rotator/{device_number}/canreverse",
        **common_endpoint_parameters,
    )(get_canreverse)

    router.get(
        "/rotator/{device_number}/ismoving",
        **common_endpoint_parameters,
    )(get_ismoving)

    router.get(
        "/rotator/{device_number}/mechanicalposition",
        **common_endpoint_parameters,
    )(get_mechanicalposition)

    router.get(
        "/rotator/{device_number}/position",
        **common_endpoint_parameters,
    )(get_position)

    router.get(
        "/rotator/{device_number}/reverse",
        **common_endpoint_parameters,
    )(get_reverse)

    router.put(
        "/rotator/{device_number}/reverse",
        **common_endpoint_parameters,
    )(put_reverse)

    router.get(
        "/rotator/{device_number}/stepsize",
        **common_endpoint_parameters,
    )(get_stepsize)

    router.get(
        "/rotator/{device_number}/targetposition",
        **common_endpoint_parameters,
    )(get_targetposition)

    router.put(
        "/rotator/{device_number}/halt",
        **common_endpoint_parameters,
    )(put_halt)

    router.put(
        "/rotator/{device_number}/move",
        **common_endpoint_parameters,
    )(put_move)

    router.put(
        "/rotator/{device_number}/moveabsolute",
        **common_endpoint_parameters,
    )(put_moveabsolute)

    router.put(
        "/rotator/{device_number}/movemechanical",
        **common_endpoint_parameters,
    )(put_movemechanical)

    router.put(
        "/rotator/{device_number}/sync",
        **common_endpoint_parameters,
    )(put_sync)

    return router
