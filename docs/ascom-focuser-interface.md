# ASCOM Focuser Interface

> This documentation is sourced from the official [ASCOM Focuser Interface](https://ascom-standards.org/newdocs/focuser.html) documentation.

**See Also:** [ASCOM Exceptions](ascom-exceptions.md) | [Common Types](ascom-common-types.md)

## Methods

### Action()

**Description:** Invoke the specified device-specific custom action.

**Parameters:**
- `ActionName` (`str`) - A name from `SupportedActions` that represents the action to be carried out.
- `ActionParameters` (`str`) - List of required arguments or empty string if none are required.

**Returns:** `str` - Action response. The meaning of returned strings is set by the driver author.

**Exceptions:**
- `MethodNotImplementedException` - If no actions at all are supported.
- `ActionNotImplementedException` - If the driver does not support the requested ActionName.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CommandBlind()

**Description:** Transmit an arbitrary string to the device and does not wait for a response.

**Parameters:**
- `Command` (`str`) - The literal command string to be transmitted.
- `Raw` (`bool`) - If True, command is transmitted 'as-is'. If False, then protocol framing characters may be added prior to transmission.

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Deprecated:** Use the more flexible `Action()` and `SupportedActions` mechanic instead.

---

### CommandBool()

**Description:** Transmit an arbitrary string to the device and wait for a boolean response.

**Parameters:**
- `Command` (`str`) - The literal command string to be transmitted.
- `Raw` (`bool`) - If True, command is transmitted 'as-is'. If False, then protocol framing characters may be added prior to transmission.

**Returns:** `bool` - True/False response from the command.

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Deprecated:** Use the more flexible `Action()` and `SupportedActions` mechanic instead.

---

### CommandString()

**Description:** Transmit an arbitrary string to the device and wait for a string response.

**Parameters:**
- `Command` (`str`) - The literal command string to be transmitted.
- `Raw` (`bool`) - If True, command is transmitted 'as-is'. If False, then protocol framing characters may be added prior to transmission.

**Returns:** `str` - String response from the command.

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Deprecated:** Use the more flexible `Action()` and `SupportedActions` mechanic instead.

---

### Connect()

**Description:** Connect to the device asynchronously. Use this to connect to a device rather than setting `Connected` to True.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Non-blocking. On return, `Connecting` must be True unless already connected. Connection has successfully completed when `Connecting` becomes (or is) False.

---

### Disconnect()

**Description:** Disconnect from the device asynchronously. Use this to disconnect from a device rather than setting `Connected` to False.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Non-blocking. On return, `Connecting` must be True unless already disconnected. Disconnect has successfully completed when `Connecting` becomes (or is) False.

---

### Halt()

**Description:** Immediately stop any focuser motion due to a previous `Move()` call.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - The focuser cannot be programmatically halted.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This method must be short-lived; it is defined as synchronous in this specification. Some focusers may not support this function.

---

### Move()

**Description:** Starts moving the focuser by the specified amount or to the specified position depending on the value of the `Absolute` property.

**Parameters:**
- `Position` (`int`) - Step distance or absolute position, depending on the value of the `Absolute` property.

**Returns:** Nothing

**Exceptions:**
- `InvalidValueException` - If Position would result in a movement beyond `MaxStep` or otherwise out of range for the focuser.
- `InvalidOperationException` - (IFocuserV2 and earlier only) Raised if `TempComp` is True and a `Move()` is attempted.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Non-blocking. Returns immediately after successfully starting the focus change with `IsMoving` = True.
>
> - If `Absolute` is True, this is an absolute positioning focuser. The Position parameter must be an integer between 0 and `MaxStep`.
> - If `Absolute` is False, this is a relative positioning focuser. The Position parameter is a step distance between minus `MaxIncrement` and plus `MaxIncrement`.

---

### SetupDialog()

**Description:** Launches a configuration dialogue box for the driver. The call will not return until the user clicks OK or cancels manually.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This method is only valid for COM drivers. Alpaca devices should provide configuration through the Alpaca HTML endpoints.

---

## Properties

### Absolute

**Type:** `bool` (Read-Only)

**Description:** Returns True if the focuser does absolute positioning; False if it is a relative positioning focuser. See the details in the documentation for the `Move()` method.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Connected

**Type:** `bool` (Read/Write)

**Description:** Retrieve or set the connected state of the device. Set True to connect to the device hardware. Set False to disconnect from the device hardware.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Property-write deprecated as of FocuserV4. Use the newer `Connect()` and `Disconnect()` methods instead.

---

### Connecting

**Type:** `bool` (Read-Only)

**Description:** Returns True while the device is undertaking an asynchronous connect or disconnect operation.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is the correct property for determining when the non-blocking methods `Connect()` or `Disconnect()` have completed.

---

### Description

**Type:** `str` (Read-Only)

**Description:** Description of the device such as manufacturer and model number. Any ASCII characters may be used. Maximum 64 characters.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### DeviceState

**Type:** `List[StateValue]` (Read-Only)

**Description:** List of `StateValue` objects representing the operational properties of this device. Returns the following properties if known:
- `IsMoving`
- `Position`
- `Temperature`
- `TimeStamp`

---

### DriverInfo

**Type:** `str` (Read-Only)

**Description:** Descriptive and version information about the ASCOM driver. This string may contain line endings and may be hundreds to thousands of characters long.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### DriverVersion

**Type:** `str` (Read-Only)

**Description:** String containing only the major and minor version of the driver in the form "n.n".

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### InterfaceVersion

**Type:** `int` (Read-Only)

**Description:** ASCOM Device interface definition version that this device supports. Should return 4 for this interface version.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### IsMoving

**Type:** `bool` (Read-Only)

**Description:** Returns True if the focuser is currently moving to a new position.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is the correct property to use to determine successful completion of a (non-blocking) `Move()` request.

---

### Link

**Type:** `bool` (Read/Write)

**Description:** Retrieve or set the connected state of the device.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Deprecated:** Use `Connected` property or the newer `Connect()` and `Disconnect()` methods instead. There is no Link endpoint in the Alpaca interface.

---

### MaxIncrement

**Type:** `int` (Read-Only)

**Description:** Maximum number of steps allowed in one `Move()` operation.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** For most focusers this is the same as the `MaxStep` property.

---

### MaxStep

**Type:** `int` (Read-Only)

**Description:** Maximum step position permitted. The focuser can step between 0 and MaxStep. If an attempt is made to move the focuser beyond these limits, it will automatically stop at the limit.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Name

**Type:** `str` (Read-Only)

**Description:** The short name of the driver, for display purposes.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Position

**Type:** `int` (Read-Only)

**Description:** Current focuser position, in steps. Valid only for absolute positioning focusers (see the `Absolute` property).

**Exceptions:**
- `PropertyNotImplementedException` - The device is a relative focuser (`Absolute` is False).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Applications must not use this as a way to determine if a (non-blocking) `Move()` has completed. Use the `IsMoving` property instead.

---

### StepSize

**Type:** `float` (Read-Only)

**Description:** Step size (microns) for the focuser.

**Exceptions:**
- `PropertyNotImplementedException` - If the focuser does not intrinsically know what the step size is.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### SupportedActions

**Type:** `List[str]` (Read-Only)

**Description:** Returns the list of custom action names supported by this driver, to be used with `Action()`.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This method, combined with `Action()`, is the supported mechanic for adding non-standard functionality.

---

### TempComp

**Type:** `bool` (Read/Write)

**Description:** Set or indicate the state of the focuser's temperature compensation. Setting `TempComp` to True puts the focuser into temperature tracking mode; setting it to False will turn off temperature tracking.

**Exceptions:**
- `PropertyNotImplementedException` - On writing to TempComp, if `TempCompAvailable` is False.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** If `TempCompAvailable` is False this property must always return False.

---

### TempCompAvailable

**Type:** `bool` (Read-Only)

**Description:** Returns True only if the focuser's temperature compensation can be turned on and off via the `TempComp` property.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Temperature

**Type:** `float` (Read-Only)

**Description:** Current ambient temperature (degrees Celsius) as measured by the focuser.

**Exceptions:**
- `PropertyNotImplementedException` - The temperature is not available for this device.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.
