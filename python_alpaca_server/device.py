import sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Optional

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import structlog
from fastapi import HTTPException, Path
from pydantic import BaseModel, field_validator

from .errors import NotImplementedError
from .request import ActionRequest, CommandRequest, CommonRequest, PutConnectedRequest

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class DeviceType(str, Enum):
    Camera = "Camera"
    CoverCalibrator = "CoverCalibrator"
    Dome = "Dome"
    FilterWheel = "FilterWheel"
    Focuser = "Focuser"
    ObservingConditions = "ObservingConditions"
    Rotator = "Rotator"
    SafetyMonitor = "SafetyMonitor"
    Switch = "Switch"
    Telescope = "Telescope"


class UrlDeviceType(str, Enum):
    Camera = "camera"
    CoverCalibrator = "covercalibrator"
    Dome = "dome"
    FilterWheel = "filterwheel"
    Focuser = "focuser"
    ObservingConditions = "observingconditions"
    Rotator = "rotator"
    SafetyMonitor = "safetymonitor"
    Switch = "switch"
    Telescope = "telescope"


class StateValue(BaseModel):
    """A name/value pair for device state.

    Used by ``get_devicestate()`` to return aggregated device state
    for reduced polling overhead.

    Attributes:
        Name: The property name (e.g., "IsSafe", "Temperature").
        Value: The property value. Can be any JSON-serializable type.
    """

    Name: str
    Value: Any


class Device(ABC):
    """Base class for all ASCOM Alpaca device implementations.

    Subclass this to implement a concrete device driver. Each abstract method
    corresponds to an ASCOM Alpaca endpoint that your driver must support.

    Your subclass must:
        - Call ``super().__init__(device_type, unique_id)`` in your constructor
        - Implement all abstract methods defined here and in device-specific
          subclasses (e.g., ``Focuser``, ``Camera``)

    Attributes:
        device_type: The ASCOM device type (Camera, Focuser, etc.).
        unique_id: A globally unique identifier for this device instance.
        device_number: Assigned by the server; do not set directly.

    Example:
        >>> class MyFocuser(Focuser):
        ...     def __init__(self):
        ...         super().__init__(unique_id="my-focuser-001")
        ...
        ...     def get_connected(self, req: CommonRequest) -> bool:
        ...         return self._is_connected
    """

    def __init__(self, device_type: DeviceType, unique_id: str):
        self.device_type = device_type
        self.unique_id = unique_id
        self.device_number: int = -1

    @abstractmethod
    def put_action(self, req: ActionRequest) -> str:
        """Invoke a device-specific custom action.

        Implement this to support custom actions beyond the standard ASCOM
        interface. The action name must be listed in ``get_supportedactions()``.

        Args:
            req: The action request containing:
                - ``action``: Name of the action to invoke (from SupportedActions)
                - ``parameters``: Action-specific parameter string, or empty

        Returns:
            Action-specific response string. Define the format in your
            documentation.

        Raises:
            NotImplementedException: Raise if no custom actions are supported.
            ActionNotImplementedException: Raise if the requested action name
                is not recognized.
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_command_blind(self, req: CommandRequest) -> None:
        """Transmit an arbitrary command string without waiting for a response.

        .. deprecated::
            Use ``put_action()`` and ``get_supportedactions()`` instead.

        Implement this only if your hardware requires raw command support for
        legacy compatibility.

        Args:
            req: The command request containing:
                - ``command``: The literal command string to transmit
                - ``raw``: If True, send as-is; if False, add protocol framing

        Raises:
            NotImplementedException: Raise if raw commands are not supported.
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_command_bool(self, req: CommandRequest) -> bool:
        """Transmit a command string and return a boolean response.

        .. deprecated::
            Use ``put_action()`` and ``get_supportedactions()`` instead.

        Implement this only if your hardware requires raw command support for
        legacy compatibility.

        Args:
            req: The command request containing:
                - ``command``: The literal command string to transmit
                - ``raw``: If True, send as-is; if False, add protocol framing

        Returns:
            Boolean response from the device.

        Raises:
            NotImplementedException: Raise if raw commands are not supported.
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_command_string(self, req: CommandRequest) -> str:
        """Transmit a command string and return a string response.

        .. deprecated::
            Use ``put_action()`` and ``get_supportedactions()`` instead.

        Implement this only if your hardware requires raw command support for
        legacy compatibility.

        Args:
            req: The command request containing:
                - ``command``: The literal command string to transmit
                - ``raw``: If True, send as-is; if False, add protocol framing

        Returns:
            String response from the device.

        Raises:
            NotImplementedException: Raise if raw commands are not supported.
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for communication errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_connected(self, req: CommonRequest) -> bool:
        """Return whether the device is currently connected.

        Implement this to return your device's connection state. This should
        reflect whether communication with the hardware is active.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            True if connected to the hardware, False otherwise.

        Raises:
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_connected(self, req: PutConnectedRequest) -> None:
        """Connect to or disconnect from the device hardware.

        Implement this to establish or terminate the connection to your
        hardware. When ``req.connected`` is True, initialize the hardware
        connection. When False, release all hardware resources.

        Your implementation should:
            - Validate hardware availability before connecting
            - Clean up resources fully when disconnecting
            - Be idempotent (connecting when connected is a no-op)

        Args:
            req: The request containing:
                - ``connected``: True to connect, False to disconnect

        Raises:
            DriverException: Raise if the connection attempt fails.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_description(self, req: CommonRequest) -> str:
        """Return a description of the device.

        Implement this to return a human-readable description including
        manufacturer and model information.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Description string (maximum 64 characters). May contain any
            ASCII characters.

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_driverinfo(self, req: CommonRequest) -> str:
        """Return descriptive and version information about the driver.

        Implement this to return detailed information about your driver
        implementation. This may be a multi-line string with extensive
        details.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Driver information string. May contain line endings and be
            hundreds to thousands of characters long.

        Raises:
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_driverversion(self, req: CommonRequest) -> str:
        """Return the driver version string.

        Implement this to return your driver's version number.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Version string in "n.n" format (e.g., "1.0", "2.1").

        Raises:
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_interfaceversion(self, req: CommonRequest) -> int:
        """Return the ASCOM interface version supported by this driver.

        Implement this to return the version of the ASCOM device interface
        that your driver implements. Check the ASCOM documentation for the
        current version number for your device type.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Interface version number (e.g., 3 for IFocuserV3, 4 for IFocuserV4).

        Raises:
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_name(self, req: CommonRequest) -> str:
        """Return the short name of the device.

        Implement this to return a brief display name for the device,
        suitable for use in user interface elements like dropdown lists.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            Short display name for the device.

        Raises:
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_supportedactions(self, req: CommonRequest) -> List[str]:
        """Return the list of custom action names supported by this driver.

        Implement this to advertise which custom actions are available via
        ``put_action()``. Return an empty list if no custom actions are
        supported.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            List of action name strings. Return an empty list if no custom
            actions are supported.

        Raises:
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_connect(self, req: CommonRequest) -> None:
        """Connect to the device asynchronously.

        Implement this to initiate a non-blocking connection. On return,
        ``get_connecting()`` must return True unless already connected.
        Clients poll ``get_connecting()`` to determine when connection completes.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Raises:
            DriverException: Raise if the connection cannot be initiated.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_disconnect(self, req: CommonRequest) -> None:
        """Disconnect from the device asynchronously.

        Implement this to initiate a non-blocking disconnection. On return,
        ``get_connecting()`` must return True unless already disconnected.
        Clients poll ``get_connecting()`` to determine when disconnection completes.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Raises:
            DriverException: Raise if the disconnection cannot be initiated.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_connecting(self, req: CommonRequest) -> bool:
        """Return whether an async connect/disconnect operation is in progress.

        Implement this to indicate when ``put_connect()`` or ``put_disconnect()``
        operations are still in progress. Return False when the operation
        completes or if no async operation is active.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            True while connecting or disconnecting, False otherwise.

        Raises:
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_devicestate(self, req: CommonRequest) -> List["StateValue"]:
        """Return aggregated device state for reduced polling.

        Implement this to return a list of name/value pairs representing
        the device's current operational state. The specific properties
        returned depend on the device type.

        Args:
            req: The Alpaca request containing client/transaction IDs.

        Returns:
            List of StateValue objects with device-specific properties.
            Include a "TimeStamp" entry with the current UTC time.

        Raises:
            NotConnectedException: Raise if the device is not connected.
            DriverException: Raise for unexpected errors.
        """
        raise NotImplementedError(req)


class PathArgs(BaseModel):
    device_number: int
    device_type: Optional[UrlDeviceType] = None

    @field_validator("device_number", mode="before")
    def check_device_number(cls, value):
        if value is not None:
            try:
                return int(value)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid device number")

        raise HTTPException(status_code=400, detail="Invalid device number")

    @field_validator("device_type", mode="before")
    def check_device_type(cls, value):
        if value is not None:
            try:
                return UrlDeviceType(value)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid device type")

        return None


def device_finder(devices: List[Device], device_type: UrlDeviceType):
    def find_device(
        args: Annotated[PathArgs, Path()],
    ) -> Device:
        logger.debug(
            "looking for device",
            device_type=device_type,
            device_number=args.device_number,
        )
        device: Optional[Device] = None
        for d in devices:
            if (
                d.device_number == args.device_number
                and d.device_type.value.lower() == device_type.value.lower()
            ):
                device = d

        if not device:
            raise HTTPException(status_code=404)

        return device

    return find_device


def common_device_finder(devices: List[Device]):
    def find_device(
        args: Annotated[PathArgs, Path()],
    ) -> Device:
        logger.debug(
            "looking for device",
            device_type=args.device_type,
            device_number=args.device_number,
        )

        if args.device_type is None:
            raise HTTPException(status_code=400, detail="Invalid device type")

        device: Optional[Device] = None
        for d in devices:
            if (
                d.device_number == args.device_number
                and d.device_type.value.lower() == args.device_type.value.lower()
            ):
                device = d

        if not device:
            raise HTTPException(status_code=404)

        return device

    return find_device
