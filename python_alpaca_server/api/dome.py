import sys
from typing import List

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import APIRouter, Depends, Query

from ..device import Device, UrlDeviceType, device_finder
from ..devices.dome import Dome, ShutterState
from ..request import (
    CommonRequest,
    PutAltitudeRequest,
    PutAzimuthRequest,
    PutSlavedRequest,
)
from ..response import Response, common_endpoint_parameters

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def create_router(devices: List[Device]):
    router = APIRouter()

    async def get_altitude(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_altitude(req),
        )

    async def get_athome(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_athome(req),
        )

    async def get_atpark(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_atpark(req),
        )

    async def get_azimuth(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_azimuth(req),
        )

    async def get_canfindhome(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_canfindhome(req),
        )

    async def get_canpark(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_canpark(req),
        )

    async def get_cansetaltitude(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_cansetaltitude(req),
        )

    async def get_cansetazimuth(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_cansetazimuth(req),
        )

    async def get_cansetpark(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_cansetpark(req),
        )

    async def get_cansetshutter(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_cansetshutter(req),
        )

    async def get_canslave(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_canslave(req),
        )

    async def get_cansyncazimuth(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_cansyncazimuth(req),
        )

    async def get_shutterstatus(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[ShutterState]:
        return Response[ShutterState].from_request(
            req,
            device.get_shutterstatus(req),
        )

    async def get_slaved(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_slaved(req),
        )

    async def put_slaved(
        req: Annotated[PutSlavedRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_slaved(req),
        )

    async def get_slewing(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[bool]:
        return Response[bool].from_request(
            req,
            device.get_slewing(req),
        )

    async def put_abortslew(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_abortslew(req),
        )

    async def put_closeshutter(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_closeshutter(req),
        )

    async def put_findhome(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_findhome(req),
        )

    async def put_openshutter(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_openshutter(req),
        )

    async def put_park(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_park(req),
        )

    async def put_setpark(
        req: Annotated[CommonRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_setpark(req),
        )

    async def put_slewtoaltitude(
        req: Annotated[PutAltitudeRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_slewtoaltitude(req),
        )

    async def put_slewtoazimuth(
        req: Annotated[PutAzimuthRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_slewtoazimuth(req),
        )

    async def put_synctoazimuth(
        req: Annotated[PutAzimuthRequest, Query()],
        device: Dome = Depends(device_finder(devices, UrlDeviceType.Dome)),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_synctoazimuth(req),
        )

    router.get(
        "/dome/{device_number}/altitude",
        **common_endpoint_parameters,
    )(get_altitude)

    router.get(
        "/dome/{device_number}/athome",
        **common_endpoint_parameters,
    )(get_athome)

    router.get(
        "/dome/{device_number}/atpark",
        **common_endpoint_parameters,
    )(get_atpark)

    router.get(
        "/dome/{device_number}/azimuth",
        **common_endpoint_parameters,
    )(get_azimuth)

    router.get(
        "/dome/{device_number}/canfindhome",
        **common_endpoint_parameters,
    )(get_canfindhome)

    router.get(
        "/dome/{device_number}/canpark",
        **common_endpoint_parameters,
    )(get_canpark)

    router.get(
        "/dome/{device_number}/cansetaltitude",
        **common_endpoint_parameters,
    )(get_cansetaltitude)

    router.get(
        "/dome/{device_number}/cansetazimuth",
        **common_endpoint_parameters,
    )(get_cansetazimuth)

    router.get(
        "/dome/{device_number}/cansetpark",
        **common_endpoint_parameters,
    )(get_cansetpark)

    router.get(
        "/dome/{device_number}/cansetshutter",
        **common_endpoint_parameters,
    )(get_cansetshutter)

    router.get(
        "/dome/{device_number}/canslave",
        **common_endpoint_parameters,
    )(get_canslave)

    router.get(
        "/dome/{device_number}/cansyncazimuth",
        **common_endpoint_parameters,
    )(get_cansyncazimuth)

    router.get(
        "/dome/{device_number}/shutterstatus",
        **common_endpoint_parameters,
    )(get_shutterstatus)

    router.get(
        "/dome/{device_number}/slaved",
        **common_endpoint_parameters,
    )(get_slaved)

    router.put(
        "/dome/{device_number}/slaved",
        **common_endpoint_parameters,
    )(put_slaved)

    router.get(
        "/dome/{device_number}/slewing",
        **common_endpoint_parameters,
    )(get_slewing)

    router.put(
        "/dome/{device_number}/abortslew",
        **common_endpoint_parameters,
    )(put_abortslew)

    router.put(
        "/dome/{device_number}/closeshutter",
        **common_endpoint_parameters,
    )(put_closeshutter)

    router.put(
        "/dome/{device_number}/findhome",
        **common_endpoint_parameters,
    )(put_findhome)

    router.put(
        "/dome/{device_number}/openshutter",
        **common_endpoint_parameters,
    )(put_openshutter)

    router.put(
        "/dome/{device_number}/park",
        **common_endpoint_parameters,
    )(put_park)

    router.put(
        "/dome/{device_number}/setpark",
        **common_endpoint_parameters,
    )(put_setpark)

    router.put(
        "/dome/{device_number}/slewtoaltitude",
        **common_endpoint_parameters,
    )(put_slewtoaltitude)

    router.put(
        "/dome/{device_number}/slewtoazimuth",
        **common_endpoint_parameters,
    )(put_slewtoazimuth)

    router.put(
        "/dome/{device_number}/synctoazimuth",
        **common_endpoint_parameters,
    )(put_synctoazimuth)

    return router
