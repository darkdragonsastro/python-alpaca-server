from typing import Annotated, List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from .device import Device, DeviceType
from .response import CommonRequest, Response, common_endpoint_parameters


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


def create_router(devices: List[Device]):
    router = APIRouter()

    @router.get(
        "/apiversions",
        **common_endpoint_parameters,
    )
    async def get_api_versions(
        req: Annotated[CommonRequest, Query()]
    ) -> Response[List[int]]:
        return Response[List[int]].from_request(req, [1])

    @router.get(
        "/v1/description",
        **common_endpoint_parameters,
    )
    async def get_description(
        req: Annotated[CommonRequest, Query()]
    ) -> Response[Description]:
        return Response[Description].from_request(
            req,
            Description(
                ServerName="Dark Dragons Python Alpaca Server",
                Manufacturer="Dark Dragons Astronomy",
                ManufacturerVersion="1.0.0",
                Location="Observatory",
            ),
        )

    @router.get(
        "/v1/configureddevices",
        **common_endpoint_parameters,
    )
    async def get_configureddevices(
        req: Annotated[CommonRequest, Query()]
    ) -> Response[List[ConfiguredDevice]]:
        return Response[List[ConfiguredDevice]].from_request(
            req,
            [
                ConfiguredDevice(
                    DeviceName=d.get_name(),
                    DeviceType=d.device_type,
                    DeviceNumber=d.device_number,
                    UniqueID=d.unique_id,
                )
                for d in devices
            ],
        )

    return router
