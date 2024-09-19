import sys
from typing import Callable, List, Union

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

from fastapi import APIRouter, Query
from pydantic import BaseModel

from ..device import Device, DeviceType
from ..response import CommonRequest, Response, common_endpoint_parameters


class Description(BaseModel):
    ServerName: str
    Manufacturer: str
    ManufacturerVersion: str
    Location: str


class ConfiguredDevice(BaseModel):
    DeviceName: str
    DeviceType: DeviceType
    DeviceNumber: int
    UniqueID: str


def create_router(
    desc: Union[Callable[[], Description], Description], devices: List[Device]
):
    router = APIRouter()

    async def get_api_versions(
        req: Annotated[CommonRequest, Query()]
    ) -> Response[List[int]]:
        return Response[List[int]].from_request(req, [1])

    async def get_description(
        req: Annotated[CommonRequest, Query()]
    ) -> Response[Description]:
        return Response[Description].from_request(
            req,
            desc() if callable(desc) else desc,
        )

    async def get_configureddevices(
        req: Annotated[CommonRequest, Query()]
    ) -> Response[List[ConfiguredDevice]]:
        return Response[List[ConfiguredDevice]].from_request(
            req,
            [
                ConfiguredDevice(
                    DeviceName=d.get_name(req),
                    DeviceType=d.device_type,
                    DeviceNumber=d.device_number,
                    UniqueID=d.unique_id,
                )
                for d in devices
            ],
        )

    router.get(
        "/apiversions",
        **common_endpoint_parameters,
    )(get_api_versions)

    router.get(
        "/v1/description",
        **common_endpoint_parameters,
    )(get_description)

    router.get(
        "/v1/configureddevices",
        **common_endpoint_parameters,
    )(get_configureddevices)

    return router
