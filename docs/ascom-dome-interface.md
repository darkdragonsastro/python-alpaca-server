# ASCOM Dome Interface

> This documentation is sourced from the official [ASCOM Dome Interface](https://ascom-standards.org/newdocs/dome.html) documentation.

**See Also:** [ASCOM Exceptions](ascom-exceptions.md) | [Common Types](ascom-common-types.md)

## Methods

### AbortSlew()

**Description:** Immediately stops any part of the dome from moving, opening, or closing.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Use the `Slewing` property to monitor stopping of the movement. When the dome has successfully stopped, `Slewing` becomes False. When motion stops, slaving must also have stopped as indicated by `Slaved` becoming False.

---

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

### CloseShutter()

**Description:** Start to close the shutter or otherwise shield the telescope from the sky.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the dome does not have a controllable shutter/roof. In this case `CanSetShutter` must be False.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Returns immediately with `ShutterStatus` = `shutterClosing` after successfully starting the operation. Use `ShutterStatus` to monitor an in-progress shutter movement. A transition to `shutterClosed` indicates a successfully completed closure.

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

### FindHome()

**Description:** Start a search for the dome's home position and synchronize Azimuth.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the dome does not support homing. In this case `CanFindHome` must be False.
- `SlavedException` - If `Slaved` is True.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Returns immediately with `Slewing` = True if the homing operation has successfully been started. Use the `Slewing` property to monitor the operation. When the home position has been successfully reached, `Azimuth` is synchronized to the appropriate value, `Slewing` becomes False and `AtHome` becomes True. Do not use `AtHome` to indicate completion.

---

### OpenShutter()

**Description:** Start to open shutter or otherwise expose telescope to the sky.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the dome does not have a controllable shutter/roof. In this case `CanSetShutter` must be False.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Returns immediately with `ShutterStatus` = `shutterOpening` if the opening has successfully been started. Use `ShutterStatus` to monitor an in-progress shutter movement. A transition to `shutterOpen` indicates a successfully completed opening.

---

### Park()

**Description:** Start slewing the dome to its park position.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the dome does not support parking. In this case `CanPark` must be False.
- `ParkedException` - If `AtPark` is True.
- `SlavedException` - If `Slaved` is True.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Returns immediately with `Slewing` = True if the park operation has successfully been started. Use the `Slewing` property to monitor the operation. When the park position has been successfully reached, `Slewing` becomes False and `AtPark` becomes True. Do not use `AtPark` to indicate completion.

---

### SetPark()

**Description:** Set current azimuth position of dome to be the park position.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the dome does not support the setting of the park position. In this case `CanSetPark` must be False.
- `SlavedException` - If `Slaved` is True.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### SetupDialog()

**Description:** Launches a configuration dialogue box for the driver. The call will not return until the user clicks OK or cancels manually.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This method is only valid for COM drivers. Alpaca devices should provide configuration through the Alpaca HTML endpoints.

---

### SlewToAltitude()

**Description:** Start slewing so that requested viewing altitude (degrees) is available for observing.

**Parameters:**
- `Altitude` (`float`) - The desired viewing altitude (degrees, horizon zero and increasing positive to 90 degrees at the zenith).

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the dome opening does not support vertical (altitude) control. In this case `CanSetAltitude` must be False.
- `InvalidValueException` - If the supplied `Altitude` is out of range.
- `SlavedException` - If `Slaved` is True.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Use the `Slewing` property to monitor the operation. When the requested Altitude has been successfully reached, `Slewing` becomes False. If the opening is closed, this method must still complete, with the dome controller accepting the requested position as its `Altitude` property.

---

### SlewToAzimuth()

**Description:** Start slewing so that requested viewing azimuth (degrees) is available for observing.

**Parameters:**
- `Azimuth` (`float`) - Desired viewing azimuth (degrees, North zero and increasing clockwise. i.e., 90 East, 180 South, 270 West).

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the dome does not support azimuth control. In this case `CanSetAzimuth` must be False.
- `InvalidValueException` - If the supplied `Azimuth` is out of range.
- `SlavedException` - If `Slaved` is True.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Use the `Slewing` property to monitor the operation. When the requested `Azimuth` has been successfully reached, `Slewing` becomes False. If the shutter is closed, this method must still complete, with the dome controller accepting the requested position as its `Azimuth` property.

---

### SyncToAzimuth()

**Description:** Synchronize the current azimuth of the dome (degrees) to the given azimuth.

**Parameters:**
- `Azimuth` (`float`) - Target azimuth (degrees, North zero and increasing clockwise. i.e., 90 East, 180 South, 270 West).

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the dome does not support azimuth synchronization. In this case `CanSyncAzimuth` must be False.
- `InvalidValueException` - If the supplied `Azimuth` is out of range.
- `SlavedException` - If `Slaved` is True.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

## Properties

### Altitude

**Type:** `float` (Read-Only)

**Description:** The altitude (degrees, horizon zero and increasing positive to 90 zenith) of the part of the sky that the observer wishes to observe.

**Exceptions:**
- `PropertyNotImplementedException` - If the dome does not support vertical (altitude) control / placement of its observing opening. In this case `CanSetAltitude` must be False.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Do not use `Altitude` as a way to determine if a (non-blocking) `SlewToAltitude()` has completed. Use the `Slewing` property.

---

### AtHome

**Type:** `bool` (Read-Only)

**Description:** True if the dome is in its home position.

**Exceptions:**
- `PropertyNotImplementedException` - If the dome does not support finding home. In this case `CanFindHome` must be False.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This should not be used to determine completion of an (async) `FindHome()` operation. Use `Slewing` for this. The `AtHome` value is reset with any azimuth slew operation that moves the dome away from the home position.

---

### AtPark

**Type:** `bool` (Read-Only)

**Description:** True if the dome is in the programmed park position.

**Exceptions:**
- `PropertyNotImplementedException` - If the dome does not support parking. In this case `CanPark` must be False.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This should not be used to determine completion of an (async) `Park()` operation. Use `Slewing` for this. The `AtPark` value is reset with any azimuth slew operation that moves the dome away from the park position.

---

### Azimuth

**Type:** `float` (Read-Only)

**Description:** Dome azimuth (degrees) of the opening to the sky. Azimuth has the usual sense of True North zero and increasing clockwise (i.e., 90 East, 180 South, 270 West).

**Exceptions:**
- `PropertyNotImplementedException` - If the dome does not support directional (azimuth) control / placement of its observing opening (such as a roll-off roof). In this case `CanSetAzimuth` must be False.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Do not use `Azimuth` as a way to determine if a (non-blocking) `SlewToAzimuth()` has completed. Use the `Slewing` property. You can detect a roll-off roof by seeing that `CanSetAzimuth` is False.

---

### CanFindHome

**Type:** `bool` (Read-Only)

**Description:** True if the dome can find its home position via `FindHome()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanPark

**Type:** `bool` (Read-Only)

**Description:** True if the dome can be programmatically parked via `Park()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanSetAltitude

**Type:** `bool` (Read-Only)

**Description:** True if the opening's altitude can be set via `SlewToAltitude()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanSetAzimuth

**Type:** `bool` (Read-Only)

**Description:** True if the opening's azimuth can be set via `SlewToAzimuth()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanSetPark

**Type:** `bool` (Read-Only)

**Description:** True if dome park position can be set via `SetPark()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanSetShutter

**Type:** `bool` (Read-Only)

**Description:** True if the shutter can be opened and closed via `OpenShutter()` and `CloseShutter()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanSlave

**Type:** `bool` (Read-Only)

**Description:** True if the opening can be slaved to the telescope/optics via `Slaved`. Only for integrated control systems.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** If this is True, then the exposed Dome interface is part of an integrated mount/dome control system that offers automatic slaving.

---

### CanSyncAzimuth

**Type:** `bool` (Read-Only)

**Description:** True if the opening's azimuth position can be synched via `SyncToAzimuth()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Connected

**Type:** `bool` (Read/Write)

**Description:** Retrieve or set the connected state of the device. Set True to connect to the device hardware. Set False to disconnect from the device hardware.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Property-write deprecated as of DomeV3. Use the newer `Connect()` and `Disconnect()` methods instead.

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
- `Altitude`
- `AtHome`
- `AtPark`
- `Azimuth`
- `ShutterStatus`
- `Slewing`
- `TimeStamp`

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

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

**Description:** ASCOM Device interface definition version that this device supports. Should return 3 for this interface version.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Name

**Type:** `str` (Read-Only)

**Description:** The short name of the driver, for display purposes.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### ShutterStatus

**Type:** `ShutterState` (Read-Only)

**Description:** Status of the dome shutter or roll-off roof. Returns a `ShutterState` enumeration value.

**Exceptions:**
- `PropertyNotImplementedException` - If the dome does not have a controllable shutter/roof. In this case `CanSetShutter` must be False.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property is the correct way to monitor an in-progress shutter movement. It must be `shutterOpening` immediately after returning from an `OpenShutter()` call, and `shutterClosing` immediately after returning from a `CloseShutter()` call.

---

### Slaved

**Type:** `bool` (Read/Write)

**Description:** Indicate or set whether the dome is slaved to the telescope. Only for integrated telescope/dome systems.

**Exceptions:**
- `PropertyNotImplementedException` - If the dome controller is not part of an integrated dome/telescope control system which offers controllable dome slaving. In this case `CanSlave` must be False.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Slewing

**Type:** `bool` (Read-Only)

**Description:** True if any part of the dome is moving, opening, or closing.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is the correct property to use to determine successful completion of a (non-blocking) `SlewToAzimuth()` and/or `SlewToAltitude()` request. `Slewing` must be True immediately upon returning from either of these calls, and must remain True until successful completion, at which time `Slewing` must become False. By "any part of the dome" is meant the roof, a shutter, clamshell leaves, a port, etc.

---

### SupportedActions

**Type:** `List[str]` (Read-Only)

**Description:** Returns the list of custom action names supported by this driver, to be used with `Action()`.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This method, combined with `Action()`, is the supported mechanic for adding non-standard functionality.

---

## Enumerated Constants

### ShutterState

Indicates the current state of the shutter or roof.

| Symbol | Value | Description |
|--------|-------|-------------|
| `shutterOpen` | 0 | The shutter or roof is open |
| `shutterClosed` | 1 | The shutter or roof is closed |
| `shutterOpening` | 2 | The shutter or roof is opening |
| `shutterClosing` | 3 | The shutter or roof is closing |
| `shutterError` | 4 | The shutter or roof has encountered a problem |
