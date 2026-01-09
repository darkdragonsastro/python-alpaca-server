# ASCOM CoverCalibrator Interface

> This documentation is sourced from the official [ASCOM CoverCalibrator Interface](https://ascom-standards.org/newdocs/covercalibrator.html) documentation.

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

> **Note:** Action names must be case insensitive.

---

### CalibratorOff()

**Description:** Turns the calibrator off if the device has calibration capability.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - When `CalibratorState` returns `NotPresent`.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Non-blocking (asynchronous). If the calibrator requires time to safely shut down after use, `CalibratorState` must return `NotReady` and `CalibratorChanging` must be `True`. When shut down is complete, `CalibratorState` must change to `Off` and `CalibratorChanging` must change to `False`.

---

### CalibratorOn()

**Description:** Turns the calibrator on or changes its brightness, if the device has calibration capability.

**Parameters:**
- `Brightness` (`int`) - The calibrator illumination brightness to be set (0 to `MaxBrightness`).

**Returns:** Nothing

**Exceptions:**
- `InvalidValueException` - When `Brightness` is outside the range 0 to `MaxBrightness`.
- `MethodNotImplementedException` - When `CalibratorState` returns `NotPresent`.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Non-blocking (asynchronous). If the calibrator requires time to safely stabilise, `CalibratorState` must return `NotReady` and `CalibratorChanging` must be `True`. When ready, `CalibratorState` must change to `Ready` and `CalibratorChanging` must change to `False`. If an error occurs, `CalibratorState` must be set to `Error` rather than `Unknown`.

---

### CloseCover()

**Description:** Initiates cover closing if a cover is present.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - When `CoverState` returns `NotPresent`.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Non-blocking (asynchronous). While the cover is closing, `CoverMoving` must return `True` and `CoverState` must return `Moving`. When closed, `CoverMoving` must return `False` and `CoverState` must return `Closed`. If an error occurs, `CoverState` must be set to `Error` rather than `Unknown`.

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

### HaltCover()

**Description:** Stops any cover movement that may be in progress if a cover is present and cover movement can be interrupted.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - When `CoverState` returns `NotPresent`, or if cover movement cannot be interrupted.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This must be a short-lived method. It must stop any cover movement as soon as possible, set `CoverMoving` to `False`, and set `CoverState` to `Open`, `Closed`, or `Unknown` as appropriate.

---

### OpenCover()

**Description:** Initiates cover opening if a cover is present.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - When `CoverState` returns `NotPresent`.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Non-blocking (asynchronous). While the cover is opening, `CoverMoving` must return `True` and `CoverState` must return `Moving`. When open, `CoverMoving` must return `False` and `CoverState` must return `Open`. If an error occurs, `CoverState` must be set to `Error` rather than `Unknown`.

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

### Brightness

**Type:** `int` (Read-Only)

**Description:** The current calibrator brightness in the range 0 (completely off) to `MaxBrightness` (fully on).

**Exceptions:**
- `PropertyNotImplementedException` - When `CalibratorState` returns `NotPresent`.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** The brightness value must be 0 when `CalibratorState` is `Off`.

---

### CalibratorChanging

**Type:** `bool` (Read-Only)

**Description:** True whenever the calibrator is not ready to be used (illumination not yet stabilized), or not completely shut down.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Use this property to determine when an asynchronous `CalibratorOn()` or `CalibratorOff()` has completed, at which time it must transition from `True` to `False`.

---

### CalibratorState

**Type:** `CalibratorStatus` (Read-Only)

**Description:** Returns the state of the calibration device, if present, otherwise returns `NotPresent`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** If no calibrator is present, the state must be `NotPresent`. Must not throw a `PropertyNotImplementedException`. The `Brightness` value must be 0 when `CalibratorState` is `Off`. If something goes wrong, `CalibratorState` must be `Error` rather than throwing an exception.

---

### Connected

**Type:** `bool` (Read/Write)

**Description:** Retrieve or set the connected state of the device. Set True to connect to the device hardware. Set False to disconnect from the device hardware.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Property-write deprecated as of CoverCalibratorV2. Use the newer `Connect()` and `Disconnect()` methods instead.

---

### Connecting

**Type:** `bool` (Read-Only)

**Description:** Returns True while the device is undertaking an asynchronous connect or disconnect operation.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is the correct property for determining when the non-blocking methods `Connect()` or `Disconnect()` have completed.

---

### CoverMoving

**Type:** `bool` (Read-Only)

**Description:** True while the cover is moving. Used to determine completion of a non-blocking `OpenCover()` or `CloseCover()` operation.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is the correct property to use when determining completion of a non-blocking `OpenCover()` or `CloseCover()` operation.

---

### CoverState

**Type:** `CoverStatus` (Read-Only)

**Description:** Returns the state of the device cover.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** If no cover is present, the `CoverState` must be `NotPresent`. Must not throw a `PropertyNotImplementedException`. Whenever the cover is opening or closing, both `CoverMoving` must be `True` and `CoverState` must be `Moving`. If something goes wrong, `CoverState` must be `Error` rather than throwing an exception.

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
- `Brightness`
- `CalibratorChanging`
- `CalibratorState`
- `CoverMoving`
- `CoverState`
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

**Description:** ASCOM Device interface definition version that this device supports. Should return 2 for this interface version.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### MaxBrightness

**Type:** `int` (Read-Only)

**Description:** The Brightness value that makes the calibrator deliver its maximum illumination.

**Exceptions:**
- `PropertyNotImplementedException` - When `CalibratorState` returns `NotPresent`.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** The value will always be a positive integer between 1 and 2,147,483,647. A value of 1 indicates the calibrator can only be "off" or "on". A value of 10 indicates 10 discrete illumination levels in addition to "off".

---

### Name

**Type:** `str` (Read-Only)

**Description:** The short name of the driver, for display purposes.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### SupportedActions

**Type:** `List[str]` (Read-Only)

**Description:** Returns the list of custom action names supported by this driver, to be used with `Action()`.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This method, combined with `Action()`, is the supported mechanic for adding non-standard functionality.

---

## Enumerated Constants

### CalibratorStatus

Describes the state of a calibration device.

| Symbol | Value | Description |
|--------|-------|-------------|
| `NotPresent` | 0 | This device does not have a calibration capability |
| `Off` | 1 | The calibrator is off |
| `NotReady` | 2 | The calibrator is stabilising or is not yet in the commanded state |
| `Ready` | 3 | The calibrator is ready for use |
| `Unknown` | 4 | The calibrator state is unknown |
| `Error` | 5 | The calibrator encountered an error when changing state |

---

### CoverStatus

Describes the state of a telescope cover.

| Symbol | Value | Description |
|--------|-------|-------------|
| `NotPresent` | 0 | This device does not have a cover that can be closed independently |
| `Closed` | 1 | The cover is closed |
| `Moving` | 2 | The cover is moving to a new position |
| `Open` | 3 | The cover is open |
| `Unknown` | 4 | The state of the cover is unknown |
| `Error` | 5 | The device encountered an error when changing state |
