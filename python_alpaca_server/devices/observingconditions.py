from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import CommonRequest, PutAveragePeriodRequest, SensorNameRequest


class ObservingConditions(Device):
    """Base class for ASCOM ObservingConditions devices.

    Implement this class to create a weather station or environmental monitoring
    device that reports atmospheric and sky conditions. Your implementation can
    support any combination of sensors - raise PropertyNotImplementedException
    for sensors your hardware does not provide.

    Sensor properties and their units:
        - Cloud cover: percent (0.0 - 100.0)
        - Dew point: degrees Celsius
        - Humidity: percent (0.0 - 100.0)
        - Pressure: hectopascals (hPa) at observatory altitude
        - Rain rate: millimeters per hour (mm/hr)
        - Sky brightness: lux
        - Sky quality: magnitudes per square arcsecond
        - Sky temperature: degrees Celsius
        - Star FWHM (seeing): arcseconds
        - Temperature: degrees Celsius
        - Wind direction: degrees (0-360, meteorological convention)
        - Wind gust: meters per second (m/s)
        - Wind speed: meters per second (m/s)

    Note:
        The ASCOM specification requires that `get_dewpoint()` and
        `get_humidity()` are either both implemented or both raise
        PropertyNotImplementedException.
    """

    def __init__(self, unique_id: str):
        super().__init__(DeviceType.ObservingConditions, unique_id)

    @abstractmethod
    def get_averageperiod(self, req: CommonRequest) -> float:
        """Return the time period (hours) over which sensor values are averaged.

        This is a mandatory property. Return 0.0 if your device delivers
        instantaneous sensor readings without averaging.

        Args:
            req: The request object containing client information.

        Returns:
            The averaging period in hours, or 0.0 for instantaneous readings.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_averageperiod(self, req: PutAveragePeriodRequest) -> None:
        """Set the time period (hours) over which sensor values are averaged.

        Implement this to allow clients to configure the averaging period for
        sensor readings. Your implementation must accept 0.0 to specify that
        instantaneous values should be returned.

        Args:
            req: The request containing the new averaging period in hours
                via req.AveragePeriod.

        Raises:
            InvalidValueException: If the requested averaging period is not
                supported by your hardware. All implementations must accept 0.0.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_cloudcover(self, req: CommonRequest) -> float:
        """Return the amount of sky obscured by cloud.

        Implement this if your device has a cloud sensor. The value represents
        the percentage of sky covered by clouds.

        Args:
            req: The request object containing client information.

        Returns:
            Cloud cover as a percentage from 0.0 (clear sky) to 100.0
            (completely overcast).

        Raises:
            PropertyNotImplementedException: If your device does not have
                a cloud sensor.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_dewpoint(self, req: CommonRequest) -> float:
        """Return the atmospheric dew point temperature.

        Implement this if your device can measure or calculate dew point.
        If you implement this, you must also implement `get_humidity()`.

        Args:
            req: The request object containing client information.

        Returns:
            Dew point temperature in degrees Celsius.

        Raises:
            PropertyNotImplementedException: If your device cannot provide
                dew point. Must also raise this if `get_humidity()` raises it.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_humidity(self, req: CommonRequest) -> float:
        """Return the atmospheric relative humidity.

        Implement this if your device has a humidity sensor. If you implement
        this, you must also implement `get_dewpoint()`.

        Args:
            req: The request object containing client information.

        Returns:
            Relative humidity as a percentage from 0.0 to 100.0.

        Raises:
            PropertyNotImplementedException: If your device does not have
                a humidity sensor. Must also raise this if `get_dewpoint()`
                raises it.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_pressure(self, req: CommonRequest) -> float:
        """Return the atmospheric pressure at the observatory altitude.

        Implement this if your device has a barometric pressure sensor.
        Your implementation must return the actual pressure at the observatory's
        altitude, not the sea-level adjusted pressure.

        If your sensor returns sea-level pressure, convert it to the actual
        pressure at your observatory's altitude before returning.

        Args:
            req: The request object containing client information.

        Returns:
            Atmospheric pressure in hectopascals (hPa) at observatory altitude.

        Raises:
            PropertyNotImplementedException: If your device does not have
                a pressure sensor.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_rainrate(self, req: CommonRequest) -> float:
        """Return the rain rate at the observatory.

        Implement this if your device has a rain sensor. The value can be
        interpreted as: 0.0 = dry, any positive value = wet.

        Reference rainfall intensity:
            - Light rain: < 2.5 mm/hr
            - Moderate rain: 2.5 - 10 mm/hr
            - Heavy rain: 10 - 50 mm/hr
            - Violent rain: > 50 mm/hr

        Args:
            req: The request object containing client information.

        Returns:
            Rain rate in millimeters per hour (mm/hr).

        Raises:
            PropertyNotImplementedException: If your device does not have
                a rain sensor.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_skybrightness(self, req: CommonRequest) -> float:
        """Return the sky brightness at the observatory.

        Implement this if your device has a light sensor measuring sky
        brightness.

        Reference values:
            - 0.0001 lux: Moonless, overcast night (starlight)
            - 0.002 lux: Moonless clear night with airglow
            - 0.27-1.0 lux: Full moon, clear night
            - 3.4 lux: Dark limit of civil twilight
            - 100 lux: Very dark overcast day
            - 1000 lux: Overcast day
            - 10000-25000 lux: Full daylight (not direct sun)

        Args:
            req: The request object containing client information.

        Returns:
            Sky brightness in lux.

        Raises:
            PropertyNotImplementedException: If your device does not have
                a sky brightness sensor.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_skyquality(self, req: CommonRequest) -> float:
        """Return the sky quality at the observatory.

        Implement this if your device has a sky quality meter (SQM) or
        similar sensor measuring sky darkness.

        Args:
            req: The request object containing client information.

        Returns:
            Sky quality in magnitudes per square arcsecond.

        Raises:
            PropertyNotImplementedException: If your device does not have
                a sky quality sensor.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_skytemperature(self, req: CommonRequest) -> float:
        """Return the sky temperature at the observatory.

        Implement this if your device has an infrared sensor measuring sky
        temperature. Lower temperatures generally indicate clearer skies.

        Args:
            req: The request object containing client information.

        Returns:
            Sky temperature in degrees Celsius.

        Raises:
            PropertyNotImplementedException: If your device does not have
                an infrared sky temperature sensor.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_starfwhm(self, req: CommonRequest) -> float:
        """Return the seeing (star FWHM) at the observatory.

        Implement this if your device can measure astronomical seeing
        conditions.

        Args:
            req: The request object containing client information.

        Returns:
            Seeing as Full Width Half Maximum (FWHM) in arcseconds.

        Raises:
            PropertyNotImplementedException: If your device cannot measure
                seeing.
            ValueNotSetException: If seeing data is not currently available
                (e.g., during daylight or cloudy conditions).
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_temperature(self, req: CommonRequest) -> float:
        """Return the atmospheric temperature at the observatory.

        Implement this if your device has a temperature sensor.

        Args:
            req: The request object containing client information.

        Returns:
            Atmospheric temperature in degrees Celsius.

        Raises:
            PropertyNotImplementedException: If your device does not have
                a temperature sensor.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_winddirection(self, req: CommonRequest) -> float:
        """Return the wind direction at the observatory.

        Implement this if your device has a wind direction sensor. Use
        meteorological convention: direction is where the wind is blowing
        FROM, measured clockwise from True North.

        Reference directions:
            - North = 0 degrees
            - East = 90 degrees
            - South = 180 degrees
            - West = 270 degrees

        If wind speed is 0, return 0 for direction.

        Args:
            req: The request object containing client information.

        Returns:
            Wind direction in degrees (0.0 - 360.0).

        Raises:
            PropertyNotImplementedException: If your device does not have
                a wind direction sensor.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_windgust(self, req: CommonRequest) -> float:
        """Return the peak wind gust at the observatory.

        Implement this if your device can measure wind gusts. The value
        should represent the peak 3-second wind gust over the last 2 minutes.

        Args:
            req: The request object containing client information.

        Returns:
            Peak wind gust in meters per second (m/s).

        Raises:
            PropertyNotImplementedException: If your device cannot measure
                wind gusts.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_windspeed(self, req: CommonRequest) -> float:
        """Return the wind speed at the observatory.

        Implement this if your device has an anemometer or wind speed sensor.

        Args:
            req: The request object containing client information.

        Returns:
            Wind speed in meters per second (m/s).

        Raises:
            PropertyNotImplementedException: If your device does not have
                a wind speed sensor.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_refresh(self, req: CommonRequest) -> None:
        """Force the device to immediately query its hardware for fresh data.

        Implement this to trigger an immediate sensor refresh. This should be
        a short-lived synchronous call that initiates the refresh but does not
        wait for long-running processes to complete. Clients should poll
        `get_timesincelastupdate()` to determine when fresh data is available.

        Args:
            req: The request object containing client information.

        Raises:
            MethodNotImplementedException: If your device does not support
                on-demand refresh.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_sensordescription(self, req: SensorNameRequest) -> str:
        """Return a description of the sensor for the specified property.

        Implement this to provide information about the sensors used by your
        device. The description should identify the sensor hardware providing
        the measurement.

        Your implementation should:
            - Return a description if the sensor is implemented, even if not
              currently returning data
            - Raise MethodNotImplementedException if the sensor is not
              implemented at all
            - Handle property names case-insensitively

        Valid property names: CloudCover, DewPoint, Humidity, Pressure,
        RainRate, SkyBrightness, SkyQuality, SkyTemperature, StarFWHM,
        Temperature, WindDirection, WindGust, WindSpeed.

        Args:
            req: The request containing the property name via req.SensorName.

        Returns:
            A description of the sensor providing the specified measurement.

        Raises:
            MethodNotImplementedException: If the specified sensor is not
                implemented by your device.
            InvalidValueException: If the property name is not recognized.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_timesincelastupdate(self, req: SensorNameRequest) -> float:
        """Return elapsed time since the specified sensor was last updated.

        Implement this to report how stale sensor data is. This is particularly
        useful after calling `put_refresh()` to determine when fresh data is
        available.

        Your implementation should:
            - Return a negative value if no valid reading has ever been received
            - If an empty string is passed for the property name, return the
              time since the most recent update of ANY sensor
            - Handle property names case-insensitively

        Valid property names: CloudCover, DewPoint, Humidity, Pressure,
        RainRate, SkyBrightness, SkyQuality, SkyTemperature, StarFWHM,
        Temperature, WindDirection, WindGust, WindSpeed (or empty string
        for any sensor).

        Args:
            req: The request containing the property name via req.SensorName.

        Returns:
            Elapsed time in seconds since the sensor was last updated, or
            a negative value if no valid reading has ever been received.

        Raises:
            MethodNotImplementedException: If the specified sensor is not
                implemented by your device.
            InvalidValueException: If the property name is not recognized.
        """
        raise NotImplementedError(req)
