# ASCOM FilterWheel Interface

> This documentation is sourced from the official [ASCOM FilterWheel Interface](https://ascom-standards.org/newdocs/filterwheel.html) documentation.

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

**Notes:**
- Must be implemented but may throw `MethodNotImplementedException` if no custom actions are supported.
- Action names must be case insensitive.

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

**Notes:**
- **Deprecated** as of version 3. Use the more flexible `Action()` and `SupportedActions` mechanic.

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

**Notes:**
- **Deprecated** as of version 3. Use the more flexible `Action()` and `SupportedActions` mechanic.

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

**Notes:**
- **Deprecated** as of version 3. Use the more flexible `Action()` and `SupportedActions` mechanic.

---

### Connect()

**Description:** Connect to the device asynchronously. Use this to connect to a device rather than setting `Connected` to True.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- **Non-Blocking**. On return, `Connecting` must be True unless already connected. Connection has successfully completed when `Connecting` becomes (or is) False.
- This is a mandatory method and must not throw a `MethodNotImplementedException`.
- Added in version 3.

---

### Disconnect()

**Description:** Disconnect from the device asynchronously. Use this to disconnect from a device rather than setting `Connected` to False.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- **Non-Blocking**. On return, `Connecting` must be True unless already disconnected. Disconnect has successfully completed when `Connecting` becomes (or is) False.
- This is a mandatory method and must not throw a `MethodNotImplementedException`.
- Added in version 3.

---

### SetupDialog()

**Description:** Launches a configuration dialogue box for the driver. The call will not return until the user clicks OK or cancels manually.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- **Blocking**. It is permissible that the configuration dialog is modal.
- Only valid for COM drivers. Alpaca devices should provide configuration through the Alpaca HTML endpoints.
- Must be implemented, must not throw a `PropertyNotImplementedException`.

---

## Properties

### Connected

**Type:** `bool` (Read/Write)

**Description:** Retrieve or set the connected state of the device. Set True to connect to the device hardware. Set False to disconnect from the device hardware.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- **Writing is deprecated** as of version 3. Use the newer `Connect()` and `Disconnect()` methods, and the newer `Connecting` property.
- Must be implemented, must not throw a `PropertyNotImplementedException`.
- Do not use a `NotConnectedException` here.
- Multiple calls setting Connected to True or False will not cause an error.

---

### Connecting

**Type:** `bool` (Read-Only)

**Description:** Returns True while the device is undertaking an asynchronous connect or disconnect operation.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- This is the correct property for determining when the non-blocking methods `Connect()` or `Disconnect()` have completed.
- Must be implemented, must not throw a `PropertyNotImplementedException`.
- Added in version 3.

---

### Description

**Type:** `str` (Read-Only)

**Description:** Description of the device such as manufacturer and model number. Any ASCII characters may be used.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- This describes the device, not the driver. See the `DriverInfo` property for information on the ASCOM driver.
- The description length must be a maximum of 64 characters so that it can be used in FITS image headers.
- Must be implemented, must not throw a `PropertyNotImplementedException`.

---

### DeviceState

**Type:** `List[StateValue]` (Read-Only)

**Description:** Returns a list of `StateValue` objects representing the operational properties of this device.

**Notes:**
- This device must return the following operational properties if they are known:
  - `Position`
  - `TimeStamp`
- Available only for the FilterWheel Interface Version 4 and later.
- Added in version 3.

---

### DriverInfo

**Type:** `str` (Read-Only)

**Description:** Descriptive and version information about the ASCOM driver.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- This string may contain line endings and may be hundreds to thousands of characters long.
- It is intended to display detailed information on the ASCOM driver, including version and copyright data.
- See the `Description` property for information on the device itself.
- Must be implemented, must not throw a `PropertyNotImplementedException`.

---

### DriverVersion

**Type:** `str` (Read-Only)

**Description:** String containing only the major and minor version of the driver.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- This must be in the form "n.n".
- It should not be confused with the `InterfaceVersion` property.
- Must be implemented, must not throw a `PropertyNotImplementedException`.

---

### FocusOffsets

**Type:** `List[int]` (Read-Only)

**Description:** Focus offset of each filter in the wheel.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- For each valid slot number (from 0 to N-1), reports the focus offset for the given filter position.
- At least one filter must have an offset of zero so it may be used as the reference for the offsets of the others.
- The number of slots N can be determined from the length of the array.
- If focuser offsets are not available, then `FocusOffsets` should report zero for all filters.
- Must be implemented, must not throw a `PropertyNotImplementedException`.

---

### InterfaceVersion

**Type:** `int` (Read-Only)

**Description:** ASCOM Device interface definition version that this device supports. Should return 3 for this interface version.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- This is a single "short" integer indicating the version of this specific ASCOM universal interface definition.
- For IFilterWheelV3, this must be 3.
- It should not be confused with the `DriverVersion` property.
- Clients can detect legacy V1 drivers by trying to read this property. If the driver raises an error, it is a V1 driver.
- Must be implemented, must not throw a `PropertyNotImplementedException`.

---

### Name

**Type:** `str` (Read-Only)

**Description:** The short name of the driver, for display purposes.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- The `Description` property is used to return info about the device rather than the driver.
- Must be implemented, must not throw a `PropertyNotImplementedException`.

---

### Names

**Type:** `List[str]` (Read-Only)

**Description:** Array of the names of each filter in the wheel.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- For each valid slot number (from 0 to N-1), reports the name of the given filter.
- The number of slots N can be determined from the length of the array.
- If names are not available, the list should contain "Filter 1", "Filter 2", ... "FilterN".
- Must be implemented, must not throw a `PropertyNotImplementedException`.

---

### Position

**Type:** `int` (Read/Write)

**Description:** Start a change to, or return the filter wheel position (zero-based).

**Exceptions:**
- `InvalidValueException` - If an invalid filter number is written to Position.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- **Asynchronous** (non-blocking): Writing to `Position` returns as soon as the filter change operation has been successfully started.
- `Position` must return -1 while the change is in progress.
- After the requested position has been successfully reached and motion stops, `Position` must return the requested new filter number.
- Write a position number between 0 and N-1, where N is the number of filter slots.
- Returning a position of -1 is mandatory while the filter wheel is in motion; valid slot numbers must not be reported back while the filter wheel is rotating past filter positions.
- **Exception**: Some filter wheels are built into the camera. Some cameras may not actually rotate the wheel until the exposure is triggered. In this case, the written value must be available immediately as the read value, and -1 is never returned.
- Must be implemented, must not throw a `PropertyNotImplementedException`.

---

### SupportedActions

**Type:** `List[str]` (Read-Only)

**Description:** Returns the list of custom action names supported by this driver, to be used with `Action()`.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

**Notes:**
- This method, combined with `Action()`, is the supported mechanic for adding non-standard functionality.
- SupportedActions is a "discovery" mechanism that enables clients to know which Actions a device supports without having to exercise the Actions themselves.
- Returned names may use any casing because the `ActionName` parameter of `Action()` is case insensitive.
- Must be implemented, must not throw a `PropertyNotImplementedException`.
