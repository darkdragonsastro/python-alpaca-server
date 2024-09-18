from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import CommonRequest, PutAveragePeriodRequest, SensorNameRequest


class ObservingConditions(Device):
    def __init__(self, unique_id: str):
        super().__init__(DeviceType.ObservingConditions, unique_id)

    @abstractmethod
    def get_averageperiod(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def put_averageperiod(self, req: PutAveragePeriodRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def get_cloudcover(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_dewpoint(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_humidity(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_pressure(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_rainrate(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_skybrightness(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_skyquality(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_skytemperature(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_starfwhm(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_temperature(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_winddirection(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_windgust(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def get_windspeed(self, req: CommonRequest) -> float:
        raise NotImplementedError(req)

    @abstractmethod
    def put_refresh(self, req: CommonRequest) -> None:
        raise NotImplementedError(req)

    @abstractmethod
    def get_sensordescription(self, req: SensorNameRequest) -> str:
        raise NotImplementedError(req)

    @abstractmethod
    def get_timesincelastupdate(self, req: SensorNameRequest) -> float:
        raise NotImplementedError(req)
