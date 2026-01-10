from abc import abstractmethod
from enum import Enum

from ..device import Device, DeviceType
from ..request import (
    CommonRequest,
    PutAltitudeRequest,
    PutAzimuthRequest,
    PutSlavedRequest,
)


class ShutterState(int, Enum):
    """Shutter or roof state enumeration.

    Represents the current operational state of a dome shutter or roll-off roof.
    Use this enum when implementing `get_shutterstatus()` to report the current
    state of the shutter mechanism.

    Attributes:
        Open: The shutter or roof is fully open.
        Closed: The shutter or roof is fully closed.
        Opening: The shutter or roof is currently opening. Return this state
            immediately after `put_openshutter()` is called.
        Closing: The shutter or roof is currently closing. Return this state
            immediately after `put_closeshutter()` is called.
        Error: The shutter or roof has encountered a problem and its state
            is unknown or it cannot be controlled.
    """

    Open = 0
    Closed = 1
    Opening = 2
    Closing = 3
    Error = 4


class Dome(Device):
    """Base class for ASCOM Dome device implementations.

    Implement this class to create a dome controller that can manage dome rotation,
    shutter control, and telescope slaving. The dome interface supports various
    configurations including rotating domes with shutters, roll-off roofs, and
    clamshell designs.

    Your implementation should handle asynchronous operations properly. All slewing
    and shutter operations are non-blocking - they start the operation and return
    immediately. Clients monitor progress via `get_slewing()` and `get_shutterstatus()`.

    Capability methods (`get_canfindhome()`, `get_canpark()`, etc.) must return
    consistent values and match the actual capabilities of your hardware. If a
    capability method returns False, the corresponding operation method should
    raise `MethodNotImplementedException`.

    Example:
        A minimal dome implementation for a roll-off roof (no azimuth control)::

            class RollOffRoof(Dome):
                def get_cansetazimuth(self, req: CommonRequest) -> bool:
                    return False  # Roll-off roofs don't rotate

                def get_cansetshutter(self, req: CommonRequest) -> bool:
                    return True  # Can open/close the roof

                # ... implement other required methods
    """

    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Dome, unique_id)

    @abstractmethod
    def get_altitude(self, req: CommonRequest) -> float:
        """Return the dome opening's altitude in degrees.

        Return the altitude of the part of the sky that is exposed through
        the dome opening. This is typically controlled by a movable shutter
        slit or adjustable opening within a rotating dome.

        Your implementation should return a value between 0 (horizon) and 90
        (zenith) degrees.

        Raise `PropertyNotImplementedException` if your dome does not support
        altitude control. In this case, `get_cansetaltitude()` must return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            The altitude in degrees (0-90, horizon to zenith).
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_athome(self, req: CommonRequest) -> bool:
        """Return True if the dome is at its home position.

        Return whether the dome is currently at its home position. The home
        position is typically a known reference point used for calibration
        and synchronization of the azimuth encoder.

        Your implementation should return False as soon as any azimuth slew
        operation moves the dome away from home. Do not use this property
        to indicate completion of `put_findhome()` - clients should use
        `get_slewing()` for that purpose.

        Raise `PropertyNotImplementedException` if your dome does not support
        homing. In this case, `get_canfindhome()` must return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if the dome is at home, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_atpark(self, req: CommonRequest) -> bool:
        """Return True if the dome is at its park position.

        Return whether the dome is currently at its programmed park position.
        The park position is typically a safe position for closing down the
        observatory.

        Your implementation should return False as soon as any azimuth slew
        operation moves the dome away from the park position. Do not use this
        property to indicate completion of `put_park()` - clients should use
        `get_slewing()` for that purpose.

        Raise `PropertyNotImplementedException` if your dome does not support
        parking. In this case, `get_canpark()` must return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if the dome is parked, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_azimuth(self, req: CommonRequest) -> float:
        """Return the dome's current azimuth in degrees.

        Return the azimuth of the dome opening to the sky. Azimuth uses the
        standard convention: 0 is North, 90 is East, 180 is South, 270 is West.

        Your implementation should return the current azimuth position regardless
        of whether the shutter is open or closed. Do not use this property to
        determine if `put_slewtoazimuth()` has completed - clients should use
        `get_slewing()` for that purpose.

        Raise `PropertyNotImplementedException` if your dome does not support
        azimuth control (e.g., a roll-off roof). In this case, `get_cansetazimuth()`
        must return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            The azimuth in degrees (0-360, North-referenced, clockwise).
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_canfindhome(self, req: CommonRequest) -> bool:
        """Return True if the dome can find its home position.

        Indicate whether your dome hardware supports a home-finding operation
        via `put_findhome()`. Return True if the dome has a home sensor or
        other mechanism to locate and synchronize to a reference position.

        This value must remain constant while connected and must accurately
        reflect hardware capability.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if `put_findhome()` is supported, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_canpark(self, req: CommonRequest) -> bool:
        """Return True if the dome can be parked.

        Indicate whether your dome hardware supports parking via `put_park()`.
        Return True if the dome can slew to a predefined park position.

        This value must remain constant while connected and must accurately
        reflect hardware capability.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if `put_park()` is supported, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansetaltitude(self, req: CommonRequest) -> bool:
        """Return True if the dome opening altitude can be controlled.

        Indicate whether your dome hardware supports altitude control via
        `put_slewtoaltitude()`. Return True if the dome has an adjustable
        shutter slit or similar mechanism for controlling the vertical
        position of the opening.

        This value must remain constant while connected and must accurately
        reflect hardware capability.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if `put_slewtoaltitude()` is supported, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansetazimuth(self, req: CommonRequest) -> bool:
        """Return True if the dome azimuth can be controlled.

        Indicate whether your dome hardware supports azimuth control via
        `put_slewtoazimuth()`. Return True for rotating domes. Return False
        for roll-off roofs and other non-rotating enclosures.

        This value must remain constant while connected and must accurately
        reflect hardware capability. Clients can detect a roll-off roof by
        checking that this returns False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if `put_slewtoazimuth()` is supported, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansetpark(self, req: CommonRequest) -> bool:
        """Return True if the park position can be configured.

        Indicate whether your dome hardware supports setting the park position
        via `put_setpark()`. Return True if the user can define where the dome
        should park.

        This value must remain constant while connected and must accurately
        reflect hardware capability.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if `put_setpark()` is supported, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansetshutter(self, req: CommonRequest) -> bool:
        """Return True if the shutter can be opened and closed.

        Indicate whether your dome hardware supports shutter control via
        `put_openshutter()` and `put_closeshutter()`. Return True for domes
        with motorized shutters or roll-off roofs. Return False if there is
        no controllable shutter mechanism.

        This value must remain constant while connected and must accurately
        reflect hardware capability.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if shutter operations are supported, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_canslave(self, req: CommonRequest) -> bool:
        """Return True if the dome can slave to the telescope.

        Indicate whether your dome is part of an integrated telescope/dome
        control system that supports automatic slaving. When slaved, the dome
        automatically tracks the telescope to keep the opening aligned with
        the telescope's optical path.

        Return True only if your system provides this integrated slaving
        capability. Most standalone dome controllers should return False.

        This value must remain constant while connected and must accurately
        reflect hardware capability.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if telescope slaving is supported, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_cansyncazimuth(self, req: CommonRequest) -> bool:
        """Return True if the azimuth can be synchronized.

        Indicate whether your dome hardware supports azimuth synchronization
        via `put_synctoazimuth()`. Return True if the dome's azimuth encoder
        can be set to a known value without physically moving the dome.

        This value must remain constant while connected and must accurately
        reflect hardware capability.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if `put_synctoazimuth()` is supported, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_shutterstatus(self, req: CommonRequest) -> ShutterState:
        """Return the current shutter state.

        Return the current operational state of the dome shutter or roll-off
        roof. This is the correct way to monitor shutter operations in progress.

        Your implementation must return `ShutterState.Opening` immediately after
        `put_openshutter()` is called, and `ShutterState.Closing` immediately
        after `put_closeshutter()` is called. Transition to `ShutterState.Open`
        or `ShutterState.Closed` when the operation completes successfully.

        Return `ShutterState.Error` if the shutter encounters a problem or its
        state cannot be determined.

        Raise `PropertyNotImplementedException` if your dome does not have a
        controllable shutter. In this case, `get_cansetshutter()` must return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            The current ShutterState value.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_slaved(self, req: CommonRequest) -> bool:
        """Return True if the dome is currently slaved to the telescope.

        Return the current slaving state. When True, the dome automatically
        tracks the telescope to keep the opening aligned with the telescope's
        optical path.

        Raise `PropertyNotImplementedException` if your dome is not part of an
        integrated telescope/dome control system. In this case, `get_canslave()`
        must return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if currently slaved, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_slaved(self, req: PutSlavedRequest) -> None:
        """Enable or disable telescope slaving.

        Enable or disable automatic dome slaving to the telescope. When enabled,
        your dome should automatically track the telescope to keep the opening
        aligned with the telescope's optical path.

        Raise `PropertyNotImplementedException` if your dome is not part of an
        integrated telescope/dome control system. In this case, `get_canslave()`
        must return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request with `Slaved` indicating the desired state.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_slewing(self, req: CommonRequest) -> bool:
        """Return True if any part of the dome is moving.

        Return whether any dome component is currently in motion. This includes
        azimuth rotation, altitude adjustment, shutter opening/closing, or any
        other mechanical movement.

        This is the correct property for clients to monitor completion of
        asynchronous operations. Your implementation must:

        - Return True immediately after `put_slewtoazimuth()` starts a slew
        - Return True immediately after `put_slewtoaltitude()` starts a slew
        - Return True immediately after `put_findhome()` starts homing
        - Return True immediately after `put_park()` starts parking
        - Return True while shutter is opening or closing
        - Return False only when all motion has stopped

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.

        Returns:
            True if any dome component is moving, False otherwise.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_abortslew(self, req: CommonRequest) -> None:
        """Immediately stop all dome motion.

        Stop any dome movement currently in progress. This includes azimuth
        rotation, altitude adjustment, shutter opening/closing, and any other
        mechanical motion.

        This is an asynchronous (non-blocking) method. Return immediately after
        initiating the stop. Clients should monitor `get_slewing()` to determine
        when all motion has actually stopped.

        Your implementation should also disable slaving when aborting - after
        abort completes, `get_slaved()` should return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_closeshutter(self, req: CommonRequest) -> None:
        """Start closing the shutter or roof.

        Begin closing the dome shutter or roll-off roof. This is an asynchronous
        (non-blocking) method - return immediately after successfully starting
        the close operation.

        Your implementation must:

        - Set shutter status to `ShutterState.Closing` before returning
        - Transition to `ShutterState.Closed` when fully closed
        - Set `get_slewing()` to True while closing

        Clients monitor progress via `get_shutterstatus()`.

        Raise `MethodNotImplementedException` if your dome does not have a
        controllable shutter. In this case, `get_cansetshutter()` must return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_findhome(self, req: CommonRequest) -> None:
        """Start searching for the dome's home position.

        Begin a search for the dome's home position and synchronize the azimuth.
        This is an asynchronous (non-blocking) method - return immediately after
        successfully starting the homing operation.

        Your implementation must:

        - Set `get_slewing()` to True before returning
        - Synchronize `get_azimuth()` when home is found
        - Set `get_slewing()` to False when complete
        - Set `get_athome()` to True when complete

        Clients monitor progress via `get_slewing()`, not `get_athome()`.

        Raise `MethodNotImplementedException` if your dome does not support
        homing. In this case, `get_canfindhome()` must return False.

        Raise `SlavedException` if `get_slaved()` is True.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_openshutter(self, req: CommonRequest) -> None:
        """Start opening the shutter or roof.

        Begin opening the dome shutter or roll-off roof to expose the telescope
        to the sky. This is an asynchronous (non-blocking) method - return
        immediately after successfully starting the open operation.

        Your implementation must:

        - Set shutter status to `ShutterState.Opening` before returning
        - Transition to `ShutterState.Open` when fully open
        - Set `get_slewing()` to True while opening

        Clients monitor progress via `get_shutterstatus()`.

        Raise `MethodNotImplementedException` if your dome does not have a
        controllable shutter. In this case, `get_cansetshutter()` must return False.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_park(self, req: CommonRequest) -> None:
        """Start slewing the dome to its park position.

        Begin slewing the dome to its programmed park position. This is an
        asynchronous (non-blocking) method - return immediately after successfully
        starting the park operation.

        Your implementation must:

        - Set `get_slewing()` to True before returning
        - Set `get_slewing()` to False when the park position is reached
        - Set `get_atpark()` to True when the park position is reached

        Clients monitor progress via `get_slewing()`, not `get_atpark()`.

        Raise `MethodNotImplementedException` if your dome does not support
        parking. In this case, `get_canpark()` must return False.

        Raise `ParkedException` if `get_atpark()` is already True.

        Raise `SlavedException` if `get_slaved()` is True.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_setpark(self, req: CommonRequest) -> None:
        """Set the current azimuth as the park position.

        Record the current dome azimuth as the park position. Future calls to
        `put_park()` will slew to this position.

        Raise `MethodNotImplementedException` if your dome does not support
        setting the park position. In this case, `get_cansetpark()` must return
        False.

        Raise `SlavedException` if `get_slaved()` is True.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request object containing client information.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_slewtoaltitude(self, req: PutAltitudeRequest) -> None:
        """Start slewing to the requested altitude.

        Begin slewing the dome opening to the requested viewing altitude. This
        is an asynchronous (non-blocking) method - return immediately after
        successfully starting the slew.

        Your implementation must:

        - Set `get_slewing()` to True before returning
        - Set `get_slewing()` to False when the altitude is reached
        - Accept the requested altitude even if the shutter is closed

        Clients monitor progress via `get_slewing()`, not `get_altitude()`.

        The altitude value is in degrees from 0 (horizon) to 90 (zenith).

        Raise `MethodNotImplementedException` if your dome does not support
        altitude control. In this case, `get_cansetaltitude()` must return False.

        Raise `InvalidValueException` if the altitude is outside the valid
        range for your hardware.

        Raise `SlavedException` if `get_slaved()` is True.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request with `Altitude` in degrees (0-90).
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_slewtoazimuth(self, req: PutAzimuthRequest) -> None:
        """Start slewing to the requested azimuth.

        Begin slewing the dome to the requested viewing azimuth. This is an
        asynchronous (non-blocking) method - return immediately after successfully
        starting the slew.

        Your implementation must:

        - Set `get_slewing()` to True before returning
        - Set `get_slewing()` to False when the azimuth is reached
        - Accept the requested azimuth even if the shutter is closed

        Clients monitor progress via `get_slewing()`, not `get_azimuth()`.

        Azimuth uses the standard convention: 0 is North, 90 is East, 180 is
        South, 270 is West.

        Raise `MethodNotImplementedException` if your dome does not support
        azimuth control. In this case, `get_cansetazimuth()` must return False.

        Raise `InvalidValueException` if the azimuth is outside the valid
        range (0-360 degrees).

        Raise `SlavedException` if `get_slaved()` is True.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request with `Azimuth` in degrees (0-360).
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_synctoazimuth(self, req: PutAzimuthRequest) -> None:
        """Synchronize the dome's azimuth to the given value.

        Set the dome's current azimuth reading to the specified value without
        physically moving the dome. Use this to correct encoder drift or
        calibrate the azimuth position.

        Azimuth uses the standard convention: 0 is North, 90 is East, 180 is
        South, 270 is West.

        Raise `MethodNotImplementedException` if your dome does not support
        azimuth synchronization. In this case, `get_cansyncazimuth()` must
        return False.

        Raise `InvalidValueException` if the azimuth is outside the valid
        range (0-360 degrees).

        Raise `SlavedException` if `get_slaved()` is True.

        Raise `NotConnectedException` if the device is not connected.

        Args:
            req: The Alpaca request with `Azimuth` in degrees (0-360).
        """
        raise NotImplementedError(req)
