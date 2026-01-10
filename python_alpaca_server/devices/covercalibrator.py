from abc import abstractmethod
from enum import Enum

from ..device import Device, DeviceType
from ..request import CommonRequest, PutBrightnessRequest


class CalibratorState(int, Enum):
    """
    Describes the state of a calibration device.

    Use this enum to report calibrator status from ``get_calibratorstate()``.

    States:
        NotPresent (0): This device does not have a calibration capability.
            Return this if your device is cover-only with no light source.

        Off (1): The calibrator is off. The ``get_brightness()`` value must
            be 0 when in this state.

        NotReady (2): The calibrator is stabilising or not yet in the commanded
            state. Return this during async operations when ``put_calibratoron()``
            or ``put_calibratoroff()`` has been called but the operation is still
            in progress. ``get_calibratorchanging()`` must return True while in
            this state.

        Ready (3): The calibrator is ready for use. The light is on and stable
            at the commanded brightness level. ``get_calibratorchanging()`` must
            return False when in this state.

        Unknown (4): The calibrator state is unknown. Use this only when the
            device cannot determine its actual state (e.g., after initialization
            before first status query).

        Error (5): The calibrator encountered an error when changing state.
            Use this instead of raising an exception from ``get_calibratorstate()``
            when something goes wrong during an operation.
    """

    NotPresent = 0
    Off = 1
    NotReady = 2
    Ready = 3
    Unknown = 4
    Error = 5


class CoverState(int, Enum):
    """
    Describes the state of a telescope cover.

    Use this enum to report cover status from ``get_coverstate()``.

    States:
        NotPresent (0): This device does not have a cover that can be closed
            independently. Return this if your device is calibrator-only with
            no motorized cover.

        Closed (1): The cover is closed. ``get_covermoving()`` must return False
            when in this state.

        Moving (2): The cover is moving to a new position. Return this during
            async operations when ``put_opencover()`` or ``put_closecover()`` has
            been called but the operation is still in progress.
            ``get_covermoving()`` must return True while in this state.

        Open (3): The cover is open. ``get_covermoving()`` must return False
            when in this state.

        Unknown (4): The state of the cover is unknown. Use this only when the
            device cannot determine its actual position (e.g., after a halt
            operation or after initialization before first status query).

        Error (5): The device encountered an error when changing state.
            Use this instead of raising an exception from ``get_coverstate()``
            when something goes wrong during an operation.
    """

    NotPresent = 0
    Closed = 1
    Moving = 2
    Open = 3
    Unknown = 4
    Error = 5


class CoverCalibrator(Device):
    """
    Abstract base class for ASCOM CoverCalibrator devices.

    A CoverCalibrator device can have a calibrator (flat panel light source),
    a motorized cover, or both. Implement the appropriate methods based on your
    device's capabilities.

    **Calibrator-only device:** Implement calibrator methods and return
    ``CoverState.NotPresent`` from ``get_coverstate()``.

    **Cover-only device:** Implement cover methods and return
    ``CalibratorState.NotPresent`` from ``get_calibratorstate()``.

    **Combined device:** Implement all methods.

    Async Behavior:
        The calibrator and cover operations (``put_calibratoron()``,
        ``put_calibratoroff()``, ``put_opencover()``, ``put_closecover()``)
        are non-blocking. Your implementation should:

        1. Initiate the operation and return immediately
        2. Update state properties to reflect the in-progress operation
        3. Track completion internally and update state when done

        Clients poll ``get_calibratorchanging()`` or ``get_covermoving()`` to
        detect completion.

    Example:
        A simple flat panel implementation::

            class MyFlatPanel(CoverCalibrator):
                def __init__(self):
                    super().__init__("my-flat-panel-123")
                    self._brightness = 0
                    self._max_brightness = 255

                def get_calibratorstate(self, req):
                    if self._brightness > 0:
                        return CalibratorState.Ready
                    return CalibratorState.Off

                def get_coverstate(self, req):
                    return CoverState.NotPresent  # No cover on this device

                # ... implement remaining methods
    """

    def __init__(self, unique_id: str):
        super().__init__(DeviceType.CoverCalibrator, unique_id)

    @abstractmethod
    def get_brightness(self, req: CommonRequest) -> int:
        """
        Return the current calibrator brightness.

        Return the brightness in the range 0 (completely off) to the value
        returned by ``get_maxbrightness()`` (fully on).

        Your implementation should:
            - Return 0 when ``get_calibratorstate()`` returns ``CalibratorState.Off``
            - Return the actual commanded brightness when the calibrator is on

        Raise:
            PropertyNotImplementedException: If ``get_calibratorstate()`` returns
                ``CalibratorState.NotPresent`` (no calibrator on this device).
            NotConnectedException: If the device is not connected.

        Returns:
            int: The current brightness level (0 to max_brightness).
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_calibratorstate(self, req: CommonRequest) -> CalibratorState:
        """
        Return the state of the calibration device.

        Your implementation should:
            - Return ``CalibratorState.NotPresent`` if no calibrator exists
            - Return ``CalibratorState.Off`` when the calibrator is off
            - Return ``CalibratorState.NotReady`` during async operations
              (stabilizing after ``put_calibratoron()`` or shutting down after
              ``put_calibratoroff()``)
            - Return ``CalibratorState.Ready`` when on and stable
            - Return ``CalibratorState.Error`` if an error occurred during
              state change (do not raise an exception)

        Important:
            This method must never raise ``PropertyNotImplementedException``.
            Return ``CalibratorState.NotPresent`` for devices without a calibrator.

        Raise:
            NotConnectedException: If the device is not connected.

        Returns:
            CalibratorState: The current calibrator state.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_coverstate(self, req: CommonRequest) -> CoverState:
        """
        Return the state of the device cover.

        Your implementation should:
            - Return ``CoverState.NotPresent`` if no cover exists
            - Return ``CoverState.Closed`` when the cover is fully closed
            - Return ``CoverState.Open`` when the cover is fully open
            - Return ``CoverState.Moving`` during async operations (while opening
              or closing after ``put_opencover()`` or ``put_closecover()``)
            - Return ``CoverState.Unknown`` if position cannot be determined
              (e.g., after ``put_haltcover()`` mid-movement)
            - Return ``CoverState.Error`` if an error occurred during state
              change (do not raise an exception)

        Important:
            This method must never raise ``PropertyNotImplementedException``.
            Return ``CoverState.NotPresent`` for devices without a cover.

        Raise:
            NotConnectedException: If the device is not connected.

        Returns:
            CoverState: The current cover state.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_calibratorchanging(self, req: CommonRequest) -> bool:
        """
        Return True while the calibrator is changing state.

        Implement this to indicate when an async ``put_calibratoron()`` or
        ``put_calibratoroff()`` operation is in progress.

        Your implementation should:
            - Return True immediately after ``put_calibratoron()`` is called
              if the calibrator needs time to stabilize
            - Return True immediately after ``put_calibratoroff()`` is called
              if the calibrator needs time to safely shut down
            - Return False when the calibrator has reached a stable state
              (``CalibratorState.Ready``, ``CalibratorState.Off``, or
              ``CalibratorState.Error``)
            - Return False if no calibrator is present

        This is the correct property for clients to poll to determine when
        async calibrator operations have completed.

        Raise:
            NotConnectedException: If the device is not connected.

        Returns:
            bool: True if the calibrator is changing state, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_covermoving(self, req: CommonRequest) -> bool:
        """
        Return True while the cover is moving.

        Implement this to indicate when an async ``put_opencover()`` or
        ``put_closecover()`` operation is in progress.

        Your implementation should:
            - Return True immediately after ``put_opencover()`` or
              ``put_closecover()`` is called
            - Return False when the cover has reached its final position
              (``CoverState.Open``, ``CoverState.Closed``, ``CoverState.Unknown``,
              or ``CoverState.Error``)
            - Return False if no cover is present

        This is the correct property for clients to poll to determine when
        async cover operations have completed.

        Raise:
            NotConnectedException: If the device is not connected.

        Returns:
            bool: True if the cover is moving, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_maxbrightness(self, req: CommonRequest) -> int:
        """
        Return the maximum brightness value supported by the calibrator.

        The return value defines the valid range for the ``brightness``
        parameter in ``put_calibratoron()``, which is 0 to this value.

        Your implementation should:
            - Return a positive integer between 1 and 2,147,483,647
            - Return 1 if the calibrator can only be "off" or "on" (no dimming)
            - Return a higher value for dimmable calibrators (e.g., 255 for
              8-bit PWM control, giving 256 levels including off)

        Raise:
            PropertyNotImplementedException: If ``get_calibratorstate()`` returns
                ``CalibratorState.NotPresent`` (no calibrator on this device).
            NotConnectedException: If the device is not connected.

        Returns:
            int: The maximum brightness value (1 to 2,147,483,647).
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_calibratoroff(self, req: CommonRequest) -> None:
        """
        Turn the calibrator off.

        This is a non-blocking (async) method. Your implementation should
        initiate the shut-down process and return immediately.

        Your implementation should:
            - Start turning off the calibrator and return immediately
            - If the calibrator needs time to safely shut down, set
              ``get_calibratorstate()`` to return ``CalibratorState.NotReady``
              and ``get_calibratorchanging()`` to return True
            - When shut down is complete, set ``get_calibratorstate()`` to
              return ``CalibratorState.Off`` and ``get_calibratorchanging()``
              to return False
            - Set ``get_brightness()`` to return 0 when off
            - If an error occurs during shut down, set ``get_calibratorstate()``
              to return ``CalibratorState.Error``

        Raise:
            MethodNotImplementedException: If ``get_calibratorstate()`` returns
                ``CalibratorState.NotPresent`` (no calibrator on this device).
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_calibratoron(self, req: PutBrightnessRequest) -> None:
        """
        Turn the calibrator on at the specified brightness.

        This is a non-blocking (async) method. Your implementation should
        initiate the operation and return immediately.

        The brightness value is available via ``req.Brightness`` and must be
        in the range 0 to the value returned by ``get_maxbrightness()``.

        Your implementation should:
            - Validate the brightness value and raise ``InvalidValueException``
              if out of range
            - Start turning on the calibrator and return immediately
            - If the calibrator needs time to stabilize, set
              ``get_calibratorstate()`` to return ``CalibratorState.NotReady``
              and ``get_calibratorchanging()`` to return True
            - When ready, set ``get_calibratorstate()`` to return
              ``CalibratorState.Ready`` and ``get_calibratorchanging()``
              to return False
            - Update ``get_brightness()`` to return the commanded brightness
            - If an error occurs, set ``get_calibratorstate()`` to return
              ``CalibratorState.Error``

        Args:
            req: Request containing the ``Brightness`` value to set.

        Raise:
            InvalidValueException: If ``req.Brightness`` is outside the range
                0 to ``get_maxbrightness()``.
            MethodNotImplementedException: If ``get_calibratorstate()`` returns
                ``CalibratorState.NotPresent`` (no calibrator on this device).
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_closecover(self, req: CommonRequest) -> None:
        """
        Initiate cover closing.

        This is a non-blocking (async) method. Your implementation should
        start the closing operation and return immediately.

        Your implementation should:
            - Start closing the cover and return immediately
            - Set ``get_coverstate()`` to return ``CoverState.Moving`` and
              ``get_covermoving()`` to return True while closing
            - When fully closed, set ``get_coverstate()`` to return
              ``CoverState.Closed`` and ``get_covermoving()`` to return False
            - If an error occurs during closing, set ``get_coverstate()`` to
              return ``CoverState.Error`` (not ``CoverState.Unknown``)

        Raise:
            MethodNotImplementedException: If ``get_coverstate()`` returns
                ``CoverState.NotPresent`` (no cover on this device).
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_haltcover(self, req: CommonRequest) -> None:
        """
        Stop any cover movement in progress.

        This must be a short-lived, synchronous method that stops cover
        movement as quickly as possible.

        Your implementation should:
            - Stop cover movement immediately
            - Set ``get_covermoving()`` to return False
            - Set ``get_coverstate()`` to return ``CoverState.Open``,
              ``CoverState.Closed``, or ``CoverState.Unknown`` as appropriate
              for the cover's final position

        Raise:
            MethodNotImplementedException: If ``get_coverstate()`` returns
                ``CoverState.NotPresent``, or if cover movement cannot be
                interrupted on this device.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_opencover(self, req: CommonRequest) -> None:
        """
        Initiate cover opening.

        This is a non-blocking (async) method. Your implementation should
        start the opening operation and return immediately.

        Your implementation should:
            - Start opening the cover and return immediately
            - Set ``get_coverstate()`` to return ``CoverState.Moving`` and
              ``get_covermoving()`` to return True while opening
            - When fully open, set ``get_coverstate()`` to return
              ``CoverState.Open`` and ``get_covermoving()`` to return False
            - If an error occurs during opening, set ``get_coverstate()`` to
              return ``CoverState.Error`` (not ``CoverState.Unknown``)

        Raise:
            MethodNotImplementedException: If ``get_coverstate()`` returns
                ``CoverState.NotPresent`` (no cover on this device).
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)
