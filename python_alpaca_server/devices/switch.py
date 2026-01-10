from abc import abstractmethod

from ..device import Device, DeviceType
from ..request import (
    CommonRequest,
    IdRequest,
    PutIdNameRequest,
    PutIdStateRequest,
    PutIdValueRequest,
)


class Switch(Device):
    """Base class for ASCOM Switch devices.

    A Switch device manages one or more switches, which can be simple on/off
    boolean switches or multi-state switches with a range of values. Switches
    are numbered from 0 to MaxSwitch - 1.

    **Switch Types:**

    - **Boolean switches**: Simple on/off state. Use `get_getswitch()` and
      `put_setswitch()` for boolean access. For these switches,
      `get_minswitchvalue()` returns 0.0 and `get_maxswitchvalue()` returns 1.0.

    - **Multi-state switches**: Support a range of values between
      `get_minswitchvalue()` and `get_maxswitchvalue()` in steps of
      `get_switchstep()`. Use `get_getswitchvalue()` and `put_setswitchvalue()`
      for numeric access.

    **Read-only vs Writable:**

    Some switches are read-only sensors (e.g., limit switches). Check
    `get_canwrite()` before attempting to set a switch value.

    **Async Operations:**

    For switches that take time to change state (e.g., motorized switches),
    implement async operations. Check `get_canasync()` for async support, use
    `put_setasync()` or `put_setasyncvalue()` to start the operation, and poll
    `get_statechangecomplete()` to monitor progress.

    Implement this class to create a concrete Switch device by providing
    implementations for all abstract methods.
    """

    def __init__(self, unique_id: str):
        super().__init__(DeviceType.Switch, unique_id)

    @abstractmethod
    def get_maxswitch(self, req: CommonRequest) -> int:
        """Return the number of switches managed by this device.

        Implement this to return the count of switches available. Switches are
        numbered from 0 to MaxSwitch - 1.

        Args:
            req: The request object containing client information.

        Returns:
            The number of switches. Valid switch IDs are 0 to this value minus 1.

        Raises:
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_canwrite(self, req: IdRequest) -> bool:
        """Return whether the specified switch can be written to.

        Implement this to indicate if the switch supports setting its state.
        Read-only switches include limit switches and sensors that can only
        report their state.

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            True if the switch can be written to, False if read-only.

        Raises:
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_getswitch(self, req: IdRequest) -> bool:
        """Return the state of the specified switch as a boolean.

        Implement this to return the on/off state of a switch. For multi-state
        switches, return False if at minimum value, True otherwise.

        Your implementation should not use this method to determine if an async
        operation has completed; use `get_statechangecomplete()` instead.

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            True if the switch is on, False if off.

        Raises:
            InvalidValueException: If the switch ID is out of range.
            InvalidOperationException: If the switch state cannot be determined
                (e.g., after power-up before state is known).
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_getswitchdescription(self, req: IdRequest) -> str:
        """Return a description of the specified switch.

        Implement this to provide a fuller description of the switch, suitable
        for display in a tooltip or detailed view.

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            A description string for the switch.

        Raises:
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_getswitchname(self, req: IdRequest) -> str:
        """Return the short name of the specified switch.

        Implement this to provide a brief name for the switch, suitable for
        display in a list or compact view.

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            A short name string for the switch.

        Raises:
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_getswitchvalue(self, req: IdRequest) -> float:
        """Return the value of the specified switch as a float.

        Implement this to return the numeric value of a switch. The value should
        be between `get_minswitchvalue()` and `get_maxswitchvalue()`.

        For boolean on/off switches, return `get_minswitchvalue()` if off, or
        `get_maxswitchvalue()` if on.

        Your implementation should not use this method to determine if an async
        operation has completed; use `get_statechangecomplete()` instead.

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            The current value of the switch.

        Raises:
            InvalidValueException: If the switch ID is out of range.
            InvalidOperationException: If the switch value cannot be determined
                (e.g., after power-up before state is known).
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_minswitchvalue(self, req: IdRequest) -> float:
        """Return the minimum value for the specified switch.

        Implement this to return the minimum allowed value for the switch. This
        must be less than `get_maxswitchvalue()`.

        For boolean on/off switches, return 0.0.

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            The minimum value for the switch.

        Raises:
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_maxswitchvalue(self, req: IdRequest) -> float:
        """Return the maximum value for the specified switch.

        Implement this to return the maximum allowed value for the switch. This
        must be greater than `get_minswitchvalue()`.

        For boolean on/off switches, return 1.0.

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            The maximum value for the switch.

        Raises:
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_switchstep(self, req: IdRequest) -> float:
        """Return the step size for the specified switch.

        Implement this to return the difference between successive values of the
        switch. The step must be greater than zero.

        The number of possible values is:
        ``((MaxSwitchValue - MinSwitchValue) / SwitchStep) + 1``

        For boolean on/off switches, return 1.0.

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            The step size for the switch.

        Raises:
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_setswitch(self, req: PutIdStateRequest) -> None:
        """Set the specified switch to the given boolean state.

        Implement this to set a switch to on (True) or off (False). After
        setting, `get_getswitchvalue()` should return `get_maxswitchvalue()`
        if True, or `get_minswitchvalue()` if False.

        Args:
            req: The request containing the switch ID and the desired state.

        Raises:
            MethodNotImplementedException: If `get_canwrite()` returns False
                for this switch.
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_setswitchname(self, req: PutIdNameRequest) -> None:
        """Set the name of the specified switch.

        Implement this to allow clients to customize switch names. If your
        device does not support client-defined names, raise
        MethodNotImplementedException.

        Args:
            req: The request containing the switch ID and the new name.

        Raises:
            MethodNotImplementedException: If switch names cannot be set.
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_setswitchvalue(self, req: PutIdValueRequest) -> None:
        """Set the specified switch to the given float value.

        Implement this to set a switch to a specific numeric value. The value
        must be between `get_minswitchvalue()` and `get_maxswitchvalue()`.

        Args:
            req: The request containing the switch ID and the desired value.

        Raises:
            MethodNotImplementedException: If `get_canwrite()` returns False
                for this switch.
            InvalidValueException: If the switch ID is out of range, or if the
                value is outside the valid range for this switch.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_canasync(self, req: IdRequest) -> bool:
        """Return whether the specified switch supports async operations.

        Implement this to indicate if the switch can operate asynchronously.
        Async operations are useful for switches that take time to change state
        (e.g., motorized switches).

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            True if the switch supports async operations, False otherwise.

        Raises:
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def get_statechangecomplete(self, req: IdRequest) -> bool:
        """Return whether an async state change has completed.

        Implement this to report when a `put_setasync()` or `put_setasyncvalue()`
        operation has finished. Poll this method to monitor async operation
        progress.

        Your implementation should return True if:
        - No async operation is in progress, OR
        - The last async operation completed successfully

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Returns:
            True if the async operation has completed, False if still in progress.

        Raises:
            MethodNotImplementedException: If `get_canasync()` returns False
                for this switch.
            OperationCancelledException: If the operation was cancelled via
                `put_cancelasync()`.
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_cancelasync(self, req: IdRequest) -> None:
        """Cancel an in-progress async state change operation.

        Implement this to abort an ongoing async operation started by
        `put_setasync()` or `put_setasyncvalue()`. After cancellation,
        `get_statechangecomplete()` should raise OperationCancelledException.

        Args:
            req: The request containing the switch ID (0 to MaxSwitch - 1).

        Raises:
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_setasync(self, req: PutIdStateRequest) -> None:
        """Asynchronously set the specified switch to the given boolean state.

        Implement this to start an async operation that sets a switch to on
        (True) or off (False). This method should return immediately after
        starting the operation, with `get_statechangecomplete()` returning False.

        When the operation completes, `get_statechangecomplete()` should return
        True, and `get_getswitchvalue()` should return `get_maxswitchvalue()`
        if True, or `get_minswitchvalue()` if False.

        Args:
            req: The request containing the switch ID and the desired state.

        Raises:
            MethodNotImplementedException: If `get_canasync()` returns False
                for this switch.
            InvalidValueException: If the switch ID is out of range.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)

    @abstractmethod
    def put_setasyncvalue(self, req: PutIdValueRequest) -> None:
        """Asynchronously set the specified switch to the given float value.

        Implement this to start an async operation that sets a switch to a
        specific numeric value. This method should return immediately after
        starting the operation, with `get_statechangecomplete()` returning False.

        When the operation completes, `get_statechangecomplete()` should return
        True.

        Args:
            req: The request containing the switch ID and the desired value.

        Raises:
            MethodNotImplementedException: If `get_canwrite()` or `get_canasync()`
                returns False for this switch.
            InvalidValueException: If the switch ID is out of range, or if the
                value is outside the valid range for this switch.
            NotConnectedException: If the device is not connected.
        """
        raise NotImplementedError(req)
