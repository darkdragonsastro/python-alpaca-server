from abc import abstractmethod
from typing import List

from ..device import Device, DeviceType
from ..request import CommonRequest, PutPositionRequest


class FilterWheel(Device):
    """Base class for ASCOM Alpaca FilterWheel devices.

    Implement this class to create a filter wheel driver. A filter wheel holds
    multiple optical filters and allows switching between them by rotating to
    different positions.

    **Position Indexing:**

    Filter positions are 0-indexed. A wheel with N filters has valid positions
    0 through N-1. The number of filters can be determined from the length of
    the arrays returned by `get_names()` or `get_focusoffsets()`.

    **Async Movement:**

    Filter wheel movement is asynchronous (non-blocking). When `put_position()`
    is called, it should start the rotation and return immediately. During
    movement, `get_position()` must return -1. Once the wheel reaches the
    target position and stops, `get_position()` returns the new position.

    **Exception:** Some filter wheels are integrated into cameras and may not
    physically rotate until an exposure is triggered. For these devices,
    `get_position()` should immediately return the requested position after
    `put_position()` is called, and -1 is never returned.
    """

    def __init__(self, unique_id: str):
        super().__init__(DeviceType.FilterWheel, unique_id)

    @abstractmethod
    def get_focusoffsets(self, req: CommonRequest) -> List[int]:
        """Return the focus offset for each filter in the wheel.

        Implement this to provide focus offsets that clients can use to adjust
        focuser position when changing filters. Each filter may require a
        different focus point due to optical path differences.

        Your implementation should return a list with one entry per filter slot,
        in position order (index 0 = filter 0, etc.). At least one filter must
        have an offset of zero to serve as the reference for other offsets.

        If focus offsets are not available or not applicable for your device,
        return a list of zeros with the same length as the number of filters.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            A list of integer focus offsets, one per filter position. The length
            of this list indicates the number of filter slots (N).

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_names(self, req: CommonRequest) -> List[str]:
        """Return the name of each filter in the wheel.

        Implement this to provide human-readable names for each filter slot.
        Names help users identify filters (e.g., "Red", "Green", "Blue",
        "H-alpha", "Luminance").

        Your implementation should return a list with one entry per filter slot,
        in position order (index 0 = filter 0, etc.).

        If filter names are not available or not configured, return default
        names in the format "Filter 1", "Filter 2", ... "Filter N" (note: 1-based
        naming for display, but 0-based indexing for positions).

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            A list of filter name strings, one per filter position. The length
            of this list indicates the number of filter slots (N).

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_position(self, req: CommonRequest) -> int:
        """Return the current filter wheel position.

        Implement this to report which filter is currently in the optical path.
        Positions are 0-indexed (0 to N-1, where N is the number of filters).

        Your implementation must return -1 while the wheel is rotating between
        positions. Once the wheel reaches the target position and stops moving,
        return the actual position number.

        **Exception:** For filter wheels integrated into cameras that don't
        physically rotate until exposure, return the last requested position
        immediately (never return -1).

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            The current filter position (0 to N-1), or -1 if the wheel is
            currently moving.

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_position(self, req: PutPositionRequest) -> None:
        """Start rotating the filter wheel to a new position.

        Implement this to initiate filter wheel movement. This method must be
        non-blocking: start the rotation and return immediately. Clients will
        poll `get_position()` to detect completion (when it stops returning -1).

        Your implementation should validate the position and raise
        InvalidValueException if it is outside the valid range (0 to N-1).

        Args:
            req: The Alpaca request containing the target position in
                `req.Position` (0 to N-1, where N is the number of filters).

        Raises:
            InvalidValueException: Raise if the position is outside the valid
                range (0 to N-1).
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for hardware communication errors.
        """
        raise NotImplementedError(req)
