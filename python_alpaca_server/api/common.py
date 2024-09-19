import sys
from typing import List

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import APIRouter, Depends, Form, Query

from ..device import Device, common_device_finder
from ..errors import NotImplementedError
from ..request import ActionRequest, CommonRequest, PutConnectedRequest
from ..response import Response, common_endpoint_parameters

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def create_router(devices: List[Device]):
    router = APIRouter()

    async def put_action(
        req: Annotated[ActionRequest, Form()],
        device: Device = Depends(common_device_finder(devices)),
    ) -> Response[str]:

        raise NotImplementedError(req)

    async def get_connected(
        req: Annotated[CommonRequest, Query()],
        device: Device = Depends(common_device_finder(devices)),
    ) -> Response[bool]:

        return Response[bool].from_request(
            req,
            device.get_connected(req),
        )

    async def put_connected(
        req: Annotated[PutConnectedRequest, Form()],
        device: Device = Depends(common_device_finder(devices)),
    ) -> Response[None]:
        device.put_connected(req)

        return Response[None].from_request(
            req,
            None,
        )

    async def get_description(
        req: Annotated[CommonRequest, Query()],
        device: Device = Depends(common_device_finder(devices)),
    ) -> Response[str]:

        return Response[str].from_request(
            req,
            device.get_description(req),
        )

    async def get_driverinfo(
        req: Annotated[CommonRequest, Query()],
        device: Device = Depends(common_device_finder(devices)),
    ) -> Response[str]:

        return Response[str].from_request(
            req,
            device.get_driverinfo(req),
        )

    async def get_driverversion(
        req: Annotated[CommonRequest, Query()],
        device: Device = Depends(common_device_finder(devices)),
    ) -> Response[str]:

        return Response[str].from_request(
            req,
            device.get_driverversion(req),
        )

    async def get_interfaceversion(
        req: Annotated[CommonRequest, Query()],
        device: Device = Depends(common_device_finder(devices)),
    ) -> Response[int]:

        return Response[int].from_request(
            req,
            device.get_interfaceversion(req),
        )

    async def get_name(
        req: Annotated[CommonRequest, Query()],
        device: Device = Depends(common_device_finder(devices)),
    ) -> Response[str]:

        return Response[str].from_request(
            req,
            device.get_name(req),
        )

    async def get_supportedactions(
        req: Annotated[CommonRequest, Query()],
        device: Device = Depends(common_device_finder(devices)),
    ) -> Response[List[str]]:

        return Response[List[str]].from_request(
            req,
            device.get_supportedactions(req),
        )

    router.put(
        "/{device_type}/{device_number}/action",
        **common_endpoint_parameters,
    )(put_action)

    router.get(
        "/{device_type}/{device_number}/connected",
        **common_endpoint_parameters,
        response_model=Response[bool],
    )(get_connected)

    router.put(
        "/{device_type}/{device_number}/connected",
        **common_endpoint_parameters,
    )(put_connected)

    router.get(
        "/{device_type}/{device_number}/description",
        **common_endpoint_parameters,
    )(get_description)

    router.get(
        "/{device_type}/{device_number}/driverinfo",
        **common_endpoint_parameters,
    )(get_driverinfo)

    router.get(
        "/{device_type}/{device_number}/driverversion",
        **common_endpoint_parameters,
    )(get_driverversion)

    router.get(
        "/{device_type}/{device_number}/interfaceversion",
        **common_endpoint_parameters,
    )(get_interfaceversion)

    router.get(
        "/{device_type}/{device_number}/name",
        **common_endpoint_parameters,
    )(get_name)

    router.get(
        "/{device_type}/{device_number}/supportedactions",
        **common_endpoint_parameters,
    )(get_supportedactions)

    return router
