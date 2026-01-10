import sys
from typing import List

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

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

    async def get_switchstep(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_switchstep(req),
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

    async def get_canasync(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_canasync(req),
        )

    async def get_statechangecomplete(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_statechangecomplete(req),
        )

    async def put_cancelasync(
        req: Annotated[IdRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_cancelasync(req),
        )

    async def put_setasync(
        req: Annotated[PutIdStateRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_setasync(req),
        )

    async def put_setasyncvalue(
        req: Annotated[PutIdValueRequest, Query()],
        device: Switch = Depends(device_finder(devices, UrlDeviceType.Switch)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_setasyncvalue(req),
        )

    router.get(
        "/switch/{device_number}/maxswitch",
        **common_endpoint_parameters,
    )(get_maxswitch)

    router.get(
        "/switch/{device_number}/canwrite",
        **common_endpoint_parameters,
    )(get_canwrite)

    router.get(
        "/switch/{device_number}/getswitch",
        **common_endpoint_parameters,
    )(get_getswitch)

    router.get(
        "/switch/{device_number}/getswitchdescription",
        **common_endpoint_parameters,
    )(get_getswitchdescription)

    router.get(
        "/switch/{device_number}/getswitchname",
        **common_endpoint_parameters,
    )(get_getswitchname)

    router.get(
        "/switch/{device_number}/getswitchvalue",
        **common_endpoint_parameters,
    )(get_getswitchvalue)

    router.get(
        "/switch/{device_number}/minswitchvalue",
        **common_endpoint_parameters,
    )(get_minswitchvalue)

    router.get(
        "/switch/{device_number}/maxswitchvalue",
        **common_endpoint_parameters,
    )(get_maxswitchvalue)

    router.get(
        "/switch/{device_number}/switchstep",
        **common_endpoint_parameters,
    )(get_switchstep)

    router.put(
        "/switch/{device_number}/setswitch",
        **common_endpoint_parameters,
    )(put_setswitch)

    router.put(
        "/switch/{device_number}/setswitchname",
        **common_endpoint_parameters,
    )(put_setswitchname)

    router.put(
        "/switch/{device_number}/setswitchvalue",
        **common_endpoint_parameters,
    )(put_setswitchvalue)

    router.get(
        "/switch/{device_number}/canasync",
        **common_endpoint_parameters,
    )(get_canasync)

    router.get(
        "/switch/{device_number}/statechangecomplete",
        **common_endpoint_parameters,
    )(get_statechangecomplete)

    router.put(
        "/switch/{device_number}/cancelasync",
        **common_endpoint_parameters,
    )(put_cancelasync)

    router.put(
        "/switch/{device_number}/setasync",
        **common_endpoint_parameters,
    )(put_setasync)

    router.put(
        "/switch/{device_number}/setasyncvalue",
        **common_endpoint_parameters,
    )(put_setasyncvalue)

    return router
