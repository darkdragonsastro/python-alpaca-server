from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import CommonRequest


class SafetyMonitor(Device):
    """Base class for ASCOM SafetyMonitor devices.

    A SafetyMonitor reports whether it is safe to operate the observatory. This
    is the simplest ASCOM device type, with only a single required method:
    `get_issafe()`.

    **Safety Semantics:**

    - ``True`` = safe to operate (e.g., weather is good, power is stable)
    - ``False`` = unsafe to operate (e.g., bad weather, power issues)

    **Multiple Monitors:**

    Multiple SafetyMonitor devices can be used together to monitor different
    aspects of observatory safety:

    - Weather conditions (rain, wind, humidity, clouds)
    - Power system status
    - Door/enclosure sensors
    - Emergency stop buttons

    Automation software typically requires ALL safety monitors to report safe
    before proceeding with operations.

    **Implementation Notes:**

    Your implementation must always return a definitive True or False value.
    Do not raise PropertyNotImplementedException from `get_issafe()`.

    Implement this class to create a concrete SafetyMonitor device by providing
    an implementation for the `get_issafe()` method.
    """

    def __init__(self, unique_id: str):
        super().__init__(DeviceType.SafetyMonitor, unique_id)

    @abstractmethod
    def get_issafe(self, req: CommonRequest) -> bool:
        """Return whether the monitored state is safe for use.

        Implement this to report the current safety status. This is the primary
        method for SafetyMonitor devices and must always return a definitive
        True or False value.

        Your implementation should:

        - Return True if conditions are safe for observatory operations
        - Return False if conditions are unsafe and operations should stop
        - Never raise PropertyNotImplementedException

        Args:
            req: The request object containing client information.

        Returns:
            True if safe to operate, False if unsafe.

        Raises:
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)
