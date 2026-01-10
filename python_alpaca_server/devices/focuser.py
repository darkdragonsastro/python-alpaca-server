from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import CommonRequest, PutPositionRequest, PutTempCompRequest


class Focuser(Device):
    """Base class for ASCOM Alpaca Focuser devices.

    Implement this class to create a focuser driver. A focuser controls the
    focus position of a telescope, either through absolute positioning (moving
    to a specific step) or relative positioning (moving by a step offset).

    Your implementation must define whether the focuser is absolute or relative
    by implementing `get_absolute()`. This determines how `put_move()` interprets
    its position parameter.

    Movement Pattern:
        Focuser movement is asynchronous. When `put_move()` is called, it should
        start the motion and return immediately. Clients poll `get_ismoving()`
        to determine when movement completes. Implement `put_halt()` to allow
        emergency stops.

    Temperature Compensation:
        If your hardware supports automatic temperature compensation, implement
        `get_tempcompavailable()` to return True and handle `get_tempcomp()` /
        `put_tempcomp()` accordingly. If not supported, `get_tempcompavailable()`
        should return False and `get_tempcomp()` should always return False.
    """

    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Focuser, unique_id)

    @abstractmethod
    def get_absolute(self, req: CommonRequest) -> bool:
        """Return whether this focuser uses absolute positioning.

        Implement this to indicate your focuser's positioning mode. This value
        determines how clients interpret the position parameter in `put_move()`:

        - If True (absolute): positions are step numbers from 0 to `get_maxstep()`
        - If False (relative): positions are step offsets from current position

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            True for absolute positioning, False for relative positioning.

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_ismoving(self, req: CommonRequest) -> bool:
        """Return whether the focuser is currently moving.

        Implement this to query your hardware's motion state. Clients poll
        this method to determine when a `put_move()` operation completes.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            True while moving, False when stationary.

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_maxincrement(self, req: CommonRequest) -> int:
        """Return the maximum step change allowed in a single move.

        Implement this to report the largest step distance your focuser can
        move in one `put_move()` call. For most focusers, this equals
        `get_maxstep()`.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Maximum number of steps for a single move operation.

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_maxstep(self, req: CommonRequest) -> int:
        """Return the maximum focuser position in steps.

        Implement this to report the travel range of your focuser. Valid
        positions range from 0 to this value. If `put_move()` would exceed
        these limits, the focuser should stop at the limit.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Maximum step position (focuser range is 0 to this value).

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_position(self, req: CommonRequest) -> int:
        """Return the current focuser position in steps.

        Implement this for absolute focusers to report the current step
        position. For relative focusers, raise PropertyNotImplementedException.

        Note: Clients should not use this to detect move completion. They
        should poll `get_ismoving()` instead.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Current position as a step count from 0 to `get_maxstep()`.

        Raises:
            PropertyNotImplementedException: Raise if this is a relative
                focuser (i.e., `get_absolute()` returns False).
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_stepsize(self, req: CommonRequest) -> float:
        """Return the step size in microns.

        Implement this if your focuser knows its physical step size. This
        helps clients calculate focus in physical units rather than steps.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Size of one step in microns.

        Raises:
            PropertyNotImplementedException: Raise if step size is unknown.
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_tempcomp(self, req: CommonRequest) -> bool:
        """Return whether temperature compensation is enabled.

        Implement this to report the current temperature compensation state.
        If `get_tempcompavailable()` returns False, this must always return
        False.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            True if temperature compensation is active, False otherwise.

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_tempcomp(self, req: PutTempCompRequest) -> None:
        """Enable or disable temperature compensation.

        Implement this to control your focuser's temperature tracking mode.
        When enabled, the focuser automatically adjusts position to compensate
        for thermal expansion/contraction.

        Args:
            req: The Alpaca request containing the desired TempComp state
                in `req.TempComp` (True to enable, False to disable).

        Raises:
            PropertyNotImplementedException: Raise if temperature compensation
                is not supported (i.e., `get_tempcompavailable()` returns False).
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_tempcompavailable(self, req: CommonRequest) -> bool:
        """Return whether temperature compensation is supported.

        Implement this to indicate if your focuser hardware supports
        temperature compensation. If False, `get_tempcomp()` must always
        return False and `put_tempcomp()` must raise
        PropertyNotImplementedException.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            True if temperature compensation can be enabled, False otherwise.

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_temperature(self, req: CommonRequest) -> float:
        """Return the current ambient temperature in degrees Celsius.

        Implement this if your focuser has a temperature sensor. This value
        is used for temperature compensation calculations and client display.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Current temperature in degrees Celsius.

        Raises:
            PropertyNotImplementedException: Raise if no temperature sensor
                is available.
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_halt(self, req: CommonRequest) -> None:
        """Immediately stop any focuser motion.

        Implement this to provide emergency stop functionality. This method
        must be synchronous and return quickly. If your focuser cannot be
        halted programmatically, raise MethodNotImplementedException.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Raises:
            MethodNotImplementedException: Raise if the focuser cannot be
                programmatically halted.
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_move(self, req: PutPositionRequest) -> None:
        """Start moving the focuser to a new position.

        Implement this to initiate focuser movement. This method must be
        non-blocking: start the motion and return immediately. Clients will
        poll `get_ismoving()` to detect completion.

        The meaning of `req.Position` depends on `get_absolute()`:

        - If absolute: move to step position (0 to `get_maxstep()`)
        - If relative: move by step offset (-`get_maxincrement()` to
          +`get_maxincrement()`)

        Your implementation should validate the position and raise
        InvalidValueException if out of range.

        Args:
            req: The Alpaca request containing the target position in
                `req.Position`.

        Raises:
            InvalidValueException: Raise if the position is out of range
                or would move beyond `get_maxstep()`.
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)
