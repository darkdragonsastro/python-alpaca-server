import sys
from typing import List

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import APIRouter, Depends, Query

from ..device import Device, UrlDeviceType, device_finder
from ..devices.covercalibrator import CalibratorState, CoverCalibrator, CoverState
from ..request import CommonRequest, PutBrightnessRequest
from ..response import Response, common_endpoint_parameters

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def create_router(devices: List[Device]):
    router = APIRouter()

    async def get_brightness(
        req: Annotated[CommonRequest, Query()],
        device: CoverCalibrator = Depends(
            device_finder(devices, UrlDeviceType.CoverCalibrator)
        ),
    ) -> Response[int]:
        return Response[int].from_request(
            req,
            device.get_brightness(req),
        )

    async def get_calibratorstate(
        req: Annotated[CommonRequest, Query()],
        device: CoverCalibrator = Depends(
            device_finder(devices, UrlDeviceType.CoverCalibrator)
        ),
    ) -> Response[CalibratorState]:
        return Response[CalibratorState].from_request(
            req,
            device.get_calibratorstate(req),
        )

    async def get_coverstate(
        req: Annotated[CommonRequest, Query()],
        device: CoverCalibrator = Depends(
            device_finder(devices, UrlDeviceType.CoverCalibrator)
        ),
    ) -> Response[CoverState]:
        return Response[CoverState].from_request(
            req,
            device.get_coverstate(req),
        )

    async def get_maxbrightness(
        req: Annotated[CommonRequest, Query()],
        device: CoverCalibrator = Depends(
            device_finder(devices, UrlDeviceType.CoverCalibrator)
        ),
    ) -> Response[int]:
        return Response[int].from_request(
            req,
            device.get_maxbrightness(req),
        )

    async def put_calibratoroff(
        req: Annotated[CommonRequest, Query()],
        device: CoverCalibrator = Depends(
            device_finder(devices, UrlDeviceType.CoverCalibrator)
        ),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_calibratoroff(req),
        )

    async def put_calibratoron(
        req: Annotated[PutBrightnessRequest, Query()],
        device: CoverCalibrator = Depends(
            device_finder(devices, UrlDeviceType.CoverCalibrator)
        ),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_calibratoron(req),
        )

    async def put_closecover(
        req: Annotated[CommonRequest, Query()],
        device: CoverCalibrator = Depends(
            device_finder(devices, UrlDeviceType.CoverCalibrator)
        ),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_closecover(req),
        )

    async def put_haltcover(
        req: Annotated[CommonRequest, Query()],
        device: CoverCalibrator = Depends(
            device_finder(devices, UrlDeviceType.CoverCalibrator)
        ),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_haltcover(req),
        )

    async def put_opencover(
        req: Annotated[CommonRequest, Query()],
        device: CoverCalibrator = Depends(
            device_finder(devices, UrlDeviceType.CoverCalibrator)
        ),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_opencover(req),
        )

    router.get(
        "/covercalibrator/{device_number}/brightness",
        **common_endpoint_parameters,
    )(get_brightness)

    router.get(
        "/covercalibrator/{device_number}/calibratorstate",
        **common_endpoint_parameters,
    )(get_calibratorstate)

    router.get(
        "/covercalibrator/{device_number}/coverstate",
        **common_endpoint_parameters,
    )(get_coverstate)

    router.get(
        "/covercalibrator/{device_number}/maxbrightness",
        **common_endpoint_parameters,
    )(get_maxbrightness)

    router.put(
        "/covercalibrator/{device_number}/calibratoroff",
        **common_endpoint_parameters,
    )(put_calibratoroff)

    router.put(
        "/covercalibrator/{device_number}/calibratoron",
        **common_endpoint_parameters,
    )(put_calibratoron)

    router.put(
        "/covercalibrator/{device_number}/closecover",
        **common_endpoint_parameters,
    )(put_closecover)

    router.put(
        "/covercalibrator/{device_number}/haltcover",
        **common_endpoint_parameters,
    )(put_haltcover)

    router.put(
        "/covercalibrator/{device_number}/opencover",
        **common_endpoint_parameters,
    )(put_opencover)

    return router
