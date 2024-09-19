import sys
from typing import List

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import APIRouter, Depends, Query

from ..device import Device, UrlDeviceType, device_finder
from ..devices.observingconditions import ObservingConditions
from ..request import CommonRequest, PutAveragePeriodRequest, SensorNameRequest
from ..response import Response, common_endpoint_parameters

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def create_router(devices: List[Device]):
    router = APIRouter()

    async def get_averageperiod(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_averageperiod(req),
        )

    async def put_averageperiod(
        req: Annotated[PutAveragePeriodRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_averageperiod(req),
        )

    async def get_cloudcover(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_cloudcover(req),
        )

    async def get_dewpoint(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_dewpoint(req),
        )

    async def get_humidity(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_humidity(req),
        )

    async def get_pressure(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_pressure(req),
        )

    async def get_rainrate(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_rainrate(req),
        )

    async def get_skybrightness(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_skybrightness(req),
        )

    async def get_skyquality(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_skyquality(req),
        )

    async def get_skytemperature(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_skytemperature(req),
        )

    async def get_starfwhm(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_starfwhm(req),
        )

    async def get_temperature(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_temperature(req),
        )

    async def get_winddirection(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_winddirection(req),
        )

    async def get_windgust(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_windgust(req),
        )

    async def get_windspeed(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_windspeed(req),
        )

    async def put_refresh(
        req: Annotated[CommonRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[None]:
        return Response[None].from_request(
            req,
            device.put_refresh(req),
        )

    async def get_sensordescription(
        req: Annotated[SensorNameRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[str]:
        return Response[str].from_request(
            req,
            device.get_sensordescription(req),
        )

    async def get_timesincelastupdate(
        req: Annotated[SensorNameRequest, Query()],
        device: ObservingConditions = Depends(
            device_finder(devices, UrlDeviceType.ObservingConditions)
        ),
    ) -> Response[float]:
        return Response[float].from_request(
            req,
            device.get_timesincelastupdate(req),
        )

    router.get(
        "/observingconditions/{device_number}/averageperiod",
        **common_endpoint_parameters,
    )(get_averageperiod)

    router.put(
        "/observingconditions/{device_number}/averageperiod",
        **common_endpoint_parameters,
    )(put_averageperiod)

    router.get(
        "/observingconditions/{device_number}/cloudcover",
        **common_endpoint_parameters,
    )(get_cloudcover)

    router.get(
        "/observingconditions/{device_number}/dewpoint",
        **common_endpoint_parameters,
    )(get_dewpoint)

    router.get(
        "/observingconditions/{device_number}/humidity",
        **common_endpoint_parameters,
    )(get_humidity)

    router.get(
        "/observingconditions/{device_number}/pressure",
        **common_endpoint_parameters,
    )(get_pressure)

    router.get(
        "/observingconditions/{device_number}/rainrate",
        **common_endpoint_parameters,
    )(get_rainrate)

    router.get(
        "/observingconditions/{device_number}/skybrightness",
        **common_endpoint_parameters,
    )(get_skybrightness)

    router.get(
        "/observingconditions/{device_number}/skyquality",
        **common_endpoint_parameters,
    )(get_skyquality)

    router.get(
        "/observingconditions/{device_number}/skytemperature",
        **common_endpoint_parameters,
    )(get_skytemperature)

    router.get(
        "/observingconditions/{device_number}/starfwhm",
        **common_endpoint_parameters,
    )(get_starfwhm)

    router.get(
        "/observingconditions/{device_number}/temperature",
        **common_endpoint_parameters,
    )(get_temperature)

    router.get(
        "/observingconditions/{device_number}/winddirection",
        **common_endpoint_parameters,
    )(get_winddirection)

    router.get(
        "/observingconditions/{device_number}/windgust",
        **common_endpoint_parameters,
    )(get_windgust)

    router.get(
        "/observingconditions/{device_number}/windspeed",
        **common_endpoint_parameters,
    )(get_windspeed)

    router.put(
        "/observingconditions/{device_number}/refresh",
        **common_endpoint_parameters,
    )(put_refresh)

    router.get(
        "/observingconditions/{device_number}/sensordescription",
        **common_endpoint_parameters,
    )(get_sensordescription)

    router.get(
        "/observingconditions/{device_number}/timesincelastupdate",
        **common_endpoint_parameters,
    )(get_timesincelastupdate)

    return router
