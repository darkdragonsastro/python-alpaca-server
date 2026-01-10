from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import CommonRequest, PutPositionFloatRequest, PutReverseRequest


class Rotator(Device):
    """Base class for ASCOM Rotator devices.

    Implement this class to create a rotator driver that controls the angular
    position of an instrument (typically an imager) attached to a telescope.

    Position vs MechanicalPosition
    ------------------------------
    Your implementation must track two related angles:

    - **MechanicalPosition**: The raw physical angle of the rotator relative to
      the optical axis. This never changes except through physical rotation.

    - **Position**: The synced position angle, which may include an offset
      established via `put_sync()`. If `put_sync()` has never been called,
      Position equals MechanicalPosition.

    The sync offset allows applications to work in equatorial position angle (PA)
    coordinates after plate-solving, while your hardware tracks mechanical angles.
    Your implementation must persist the sync offset across driver restarts and
    device reboots.

    Async Move Operations
    ---------------------
    All move methods (`put_move()`, `put_moveabsolute()`, `put_movemechanical()`)
    are non-blocking. Your implementation should:

    1. Validate the requested position
    2. Update the target position
    3. Start the physical rotation
    4. Return immediately with `get_ismoving()` returning True
    5. Set `get_ismoving()` to False only when motion completes

    Position Range
    --------------
    All position values are in degrees, ranging from 0 to 360 (exclusive).
    Your implementation should normalize angles to this range.

    Cable Wrap Prevention
    ---------------------
    Your implementation must prevent cable wrapping. The rotator should be able
    to move between any two angles without limits or dead zones, handling wrap
    internally and transparently to the application.

    Rotation Direction
    ------------------
    Normal rotation is counterclockwise as viewed from behind the rotator,
    looking toward the sky. This matches the direction of increasing equatorial
    position angle. When `get_reverse()` returns True, rotation direction is
    reversed (clockwise).
    """

    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Rotator, unique_id)

    @abstractmethod
    def get_canreverse(self, req: CommonRequest) -> bool:
        """Return whether the rotation direction can be reversed.

        Return True if your rotator supports the `put_reverse()` method to
        change the direction of rotation.

        Note:
            Per the ASCOM specification, this must always return True.

        Raise:
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_ismoving(self, req: CommonRequest) -> bool:
        """Return whether the rotator is currently moving.

        Return True if the rotator is in motion due to a call to `put_move()`,
        `put_moveabsolute()`, or `put_movemechanical()`.

        Your implementation should:

        - Return True immediately after starting any move operation
        - Continue returning True while the rotator is physically moving
        - Return False only when the rotator has reached its target and stopped

        Note:
            This is the correct way for clients to determine when a non-blocking
            move operation has completed. Do not rely on position matching the
            target, as the position may transit through the target before settling.

        Raise:
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_mechanicalposition(self, req: CommonRequest) -> float:
        """Return the raw mechanical position in degrees.

        Return the physical angle of the rotator relative to the optical axis,
        as a float from 0.0 to less than 360.0 degrees.

        This value is unaffected by any sync offset established via `put_sync()`.
        It represents the actual physical orientation of the rotator hardware.

        Use this for operations that require the physical rotation angle, such as
        taking sky flats where the physical orientation matters.

        Raise:
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_position(self, req: CommonRequest) -> float:
        """Return the current position angle in degrees, including any sync offset.

        Return the synced position angle as a float from 0.0 to less than 360.0
        degrees. This value includes any offset established via `put_sync()`.

        Your implementation should:

        - Return MechanicalPosition if `put_sync()` has never been called
        - Apply the sync offset if `put_sync()` has been called
        - Persist the sync offset across driver restarts and device reboots

        Note:
            Do not use this to determine if a move has completed. The position
            may transit through the target before settling. Use `get_ismoving()`
            instead.

        Raise:
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_reverse(self, req: CommonRequest) -> bool:
        """Return whether rotation direction is reversed.

        Return True if rotation is clockwise (opposite to normal). Normal
        rotation is counterclockwise as viewed from behind the rotator, looking
        toward the sky, which matches increasing equatorial position angle.

        Raise:
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_reverse(self, req: PutReverseRequest) -> None:
        """Set the rotation direction reversal state.

        Set to True to reverse rotation direction (clockwise). Set to False for
        normal counterclockwise rotation.

        The `req.Reverse` field contains the desired reversal state.

        Raise:
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_stepsize(self, req: CommonRequest) -> float:
        """Return the minimum rotation step size in degrees.

        Return the smallest angular increment that the rotator can achieve.

        Raise:
            PropertyNotImplementedException: If the rotator does not know its
                step size.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_targetposition(self, req: CommonRequest) -> float:
        """Return the target position angle in degrees.

        Return the destination angle for the current or most recent move
        operation, as a float from 0.0 to less than 360.0 degrees.

        This value is updated immediately when `put_move()` or `put_moveabsolute()`
        is called, before the physical rotation begins. It includes any sync
        offset.

        Raise:
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_halt(self, req: CommonRequest) -> None:
        """Immediately stop any rotator motion.

        Stop any rotation currently in progress due to a previous `put_move()`,
        `put_moveabsolute()`, or `put_movemechanical()` call.

        Your implementation should:

        - Stop motion as quickly as safely possible
        - Return promptly (this should be synchronous and short-lived)
        - Allow `get_ismoving()` to reflect the actual motion state

        Note:
            Clients may poll `get_ismoving()` after calling this to determine
            when motion has actually stopped.

        Raise:
            MethodNotImplementedException: If halt is not supported.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_move(self, req: PutPositionFloatRequest) -> None:
        """Start a relative rotation by the specified number of degrees.

        Rotate by the angle specified in `req.Position` relative to the current
        position. Positive values rotate counterclockwise (normal direction),
        negative values rotate clockwise.

        This is a non-blocking method. Your implementation should:

        1. Calculate the new target: (current Position + req.Position) mod 360
        2. Update the target position immediately
        3. Start the physical rotation
        4. Return immediately (do not wait for motion to complete)
        5. Ensure `get_ismoving()` returns True until motion completes

        Raise:
            InvalidValueException: If the position value is invalid.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_moveabsolute(self, req: PutPositionFloatRequest) -> None:
        """Start rotation to an absolute position angle in degrees.

        Rotate to the angle specified in `req.Position`. This is the synced
        position angle (including any offset from `put_sync()`), not the
        mechanical position.

        The position must be in the range 0.0 to less than 360.0 degrees.

        This is a non-blocking method. Your implementation should:

        1. Validate the requested position
        2. Update the target position to req.Position
        3. Start the physical rotation
        4. Return immediately (do not wait for motion to complete)
        5. Ensure `get_ismoving()` returns True until motion completes

        Raise:
            InvalidValueException: If the position is outside 0-360 range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_movemechanical(self, req: PutPositionFloatRequest) -> None:
        """Start rotation to an absolute mechanical position in degrees.

        Rotate to the mechanical angle specified in `req.Position`, ignoring any
        sync offset. Use this for operations requiring a specific physical
        orientation, such as taking sky flats.

        The position must be in the range 0.0 to less than 360.0 degrees.

        This is a non-blocking method. Your implementation should:

        1. Validate the requested position
        2. Start the physical rotation to the mechanical angle
        3. Return immediately (do not wait for motion to complete)
        4. Ensure `get_ismoving()` returns True until motion completes

        Note:
            Unlike `put_moveabsolute()`, this method ignores the sync offset and
            moves directly to the physical angle.

        Raise:
            InvalidValueException: If the position is outside 0-360 range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_sync(self, req: PutPositionFloatRequest) -> None:
        """Sync the rotator to the specified position angle without moving.

        Set the current position to `req.Position` without physically rotating.
        This establishes an offset between the mechanical position and the
        reported position, allowing applications to work in equatorial position
        angle coordinates.

        The position must be in the range 0.0 to less than 360.0 degrees.

        Your implementation should:

        1. Calculate the sync offset: req.Position - MechanicalPosition
        2. Store this offset persistently (survive restarts and reboots)
        3. Apply this offset to all future `get_position()` calls
        4. Use synced coordinates for `put_move()` and `put_moveabsolute()`

        This is typically called after plate-solving to calibrate the rotator
        to match the actual sky position angle.

        Raise:
            InvalidValueException: If the position is outside 0-360 range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)
