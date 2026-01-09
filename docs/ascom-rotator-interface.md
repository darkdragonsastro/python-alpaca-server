# ASCOM Rotator Interface

> This documentation is sourced from the official [ASCOM Rotator Interface](https://ascom-standards.org/newdocs/rotator.html) documentation.

**See Also:** [ASCOM Exceptions](ascom-exceptions.md) | [Common Types](ascom-common-types.md)

The Rotator V4 interface provides for a common offset between its mechanical angle, plus the angle at which an attached imager may be mounted, and the equatorial position angle (PA) on the sky. By calling `Sync()` with a known current PA (from plate solving etc.), you can cause the rotator (and imager) to work directly in PA for you as well as other apps that might be using the rotator.

> **Important:** It is *vital* that an instrument rotator prevent wrapping of cables going to the imager. This must be transparent to the rotation commands coming from the application, allowing the application to freely move the rotator between any two angles without limits or "dead zones".

## Methods

### Action()

**Description:** Invoke the specified device-specific custom action.

**Parameters:**
- `ActionName` (`str`) - A name from `SupportedActions` that represents the action to be carried out.
- `ActionParameters` (`str`) - List of required arguments or empty string if none are required.

**Returns:** `str` - Action response. The meaning of returned strings is set by the driver author.

**Exceptions:**
- `MethodNotImplementedException` - If no actions at all are supported
- `ActionNotImplementedException` - If the driver does not support the requested ActionName
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** Action names must be case insensitive.

---

### CommandBlind()

**Description:** Transmit an arbitrary string to the device and does not wait for a response.

**Parameters:**
- `Command` (`str`) - The literal command string to be transmitted.
- `Raw` (`bool`) - If True, command is transmitted 'as-is'. If False, then protocol framing characters may be added prior to transmission.

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Deprecated:** Use the more flexible `Action()` and `SupportedActions` mechanic instead.

---

### CommandBool()

**Description:** Transmit an arbitrary string to the device and wait for a boolean response.

**Parameters:**
- `Command` (`str`) - The literal command string to be transmitted.
- `Raw` (`bool`) - If True, command is transmitted 'as-is'. If False, then protocol framing characters may be added prior to transmission.

**Returns:** `bool` - True/False response from the command

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Deprecated:** Use the more flexible `Action()` and `SupportedActions` mechanic instead.

---

### CommandString()

**Description:** Transmit an arbitrary string to the device and wait for a string response.

**Parameters:**
- `Command` (`str`) - The literal command string to be transmitted.
- `Raw` (`bool`) - If True, command is transmitted 'as-is'. If False, then protocol framing characters may be added prior to transmission.

**Returns:** `str` - String response from the command

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Deprecated:** Use the more flexible `Action()` and `SupportedActions` mechanic instead.

---

### Connect()

**Description:** Connect to the device asynchronously. Use this to connect to a device rather than setting `Connected` to True.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This is a non-blocking method. On return, `Connecting` must be True unless already connected. Connection has successfully completed when `Connecting` becomes (or is) False. New in Rotator V4.

---

### Disconnect()

**Description:** Disconnect from the device asynchronously. Use this to disconnect from a device rather than setting `Connected` to False.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This is a non-blocking method. On return, `Connecting` must be True unless already disconnected. Disconnect has successfully completed when `Connecting` becomes (or is) False. New in Rotator V4.

---

### Halt()

**Description:** Immediately stop any rotator motion due to a previous `Move()` or `MoveAbsolute()` call.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** Some Rotators may not support this function, in which case `MethodNotImplementedException` must be raised. Must be short-lived synchronous. The client may still check `IsMoving` to see when it actually stops if this takes some time.

---

### Move()

**Description:** Starts rotation relative to the current position (degrees).

**Parameters:**
- `Position` (`float`) - Relative position to move in degrees from current `Position`.

**Returns:** Nothing

**Exceptions:**
- `InvalidValueException` - If `Position` is invalid
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This is an asynchronous method. Must return immediately with `IsMoving` = True if the operation has successfully been started (unless it is already at the requested position). After the requested angle is successfully reached and motion stops, the `IsMoving` property must become False. Calling `Move()` must cause the `TargetPosition` property to change to the sum of the current angular position and the value of the `Position` parameter (modulo 360 degrees).

---

### MoveAbsolute()

**Description:** Starts rotation to the given absolute `Position` (degrees).

**Parameters:**
- `Position` (`float`) - New position in degrees.

**Returns:** Nothing

**Exceptions:**
- `InvalidValueException` - If `Position` is invalid
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This is an asynchronous method. Must return immediately with `IsMoving` = True if the operation has successfully been started (unless it is already at the requested position). After the requested angle is successfully reached and motion stops, the `IsMoving` property becomes False. Calling `MoveAbsolute()` must cause the `TargetPosition` property to change to the `Position` parameter then starts rotation to `TargetPosition`.

---

### MoveMechanical()

**Description:** Starts rotation to the given mechanical `Position` (degrees).

**Parameters:**
- `Position` (`float`) - New mechanical position in degrees.

**Returns:** Nothing

**Exceptions:**
- `InvalidValueException` - If `Position` is invalid
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This is an asynchronous method. Must return immediately with `IsMoving` = True if the operation has successfully been started (unless it is already at the requested position). After the requested angle is successfully reached and motion stops, the `IsMoving` property becomes False. This method is to address requirements that need a physical rotation angle such as taking sky flats. Added in version 3.

---

### Sync()

**Description:** Syncs the rotator to the specified position angle without moving it.

**Parameters:**
- `Position` (`float`) - Synchronised rotator position angle.

**Returns:** Nothing

**Exceptions:**
- `InvalidValueException` - If `Position` is invalid
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** Must be short-lived and synchronous. Once this method has been called and the sync offset determined, both the `MoveAbsolute()` method and the `Position` property must function in synced coordinates rather than mechanical coordinates. The sync offset must persist across driver starts and device reboots. Added in version 3.

---

### SetupDialog()

**Description:** Launches a configuration dialogue box for the driver. The call will not return until the user clicks OK or cancels manually.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This method is only valid for COM drivers. Alpaca devices should provide configuration through the Alpaca HTML endpoints and should not implement a SetupDialog endpoint. This is a blocking call.

---

## Properties

### CanReverse

**Type:** `bool` (Read-Only)

**Description:** Returns True if the direction of rotation can be set via the `Reverse` property.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** Must be implemented, must always return True.

---

### Connected

**Type:** `bool` (Read/Write)

**Description:** Retrieve or set the connected state of the device. Set True to connect to the device hardware. Set False to disconnect from the device hardware. You can also read the property to check whether it is connected.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Deprecated (write):** Writing is deprecated as of Rotator V4. Use the newer `Connect()` and `Disconnect()` methods, and the newer `Connecting` property.

---

### Connecting

**Type:** `bool` (Read-Only)

**Description:** Returns True while the device is undertaking an asynchronous connect or disconnect operation.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This is the correct property for determining when the non-blocking methods `Connect()` or `Disconnect()` have completed. Completion is when `Connecting` becomes False after calling either of these methods. New in Rotator V4.

---

### Description

**Type:** `str` (Read-Only)

**Description:** Description of the device such as manufacturer and model number. Any ASCII characters may be used.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This describes the device, not the driver. See the `DriverInfo` property for information on the ASCOM driver. The description length must be a maximum of 64 characters so that it can be used in FITS image headers.

---

### DeviceState

**Type:** `List[StateValue]` (Read-Only)

**Description:** Returns a list of `StateValue` objects representing the operational properties of this device.

This device must return the following operational properties if they are known:
- `IsMoving`
- `MechanicalPosition`
- `Position`
- `TimeStamp`

> **Note:** Available only for the Rotator Interface Version 4 and later.

---

### DriverInfo

**Type:** `str` (Read-Only)

**Description:** Descriptive and version information about the ASCOM driver.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This string may contain line endings and may be hundreds to thousands of characters long. It is intended to display detailed information on the ASCOM driver, including version and copyright data. See the `Description` property for information on the device itself.

---

### DriverVersion

**Type:** `str` (Read-Only)

**Description:** String containing only the major and minor version of the driver.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This must be in the form "n.n". It should not be confused with the `InterfaceVersion` property, which is the version of this specification supported by the driver.

---

### InterfaceVersion

**Type:** `int` (Read-Only)

**Description:** ASCOM Device interface definition version that this device supports. Should return 4 for this interface version.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This is a single "short" integer indicating the version of this specific ASCOM universal interface definition. For example, for IRotatorV4, this will be 4. Clients can detect legacy V1 drivers by trying to read this property. If the driver raises an error, it is a V1 driver.

---

### IsMoving

**Type:** `bool` (Read-Only)

**Description:** Returns True if the rotator is currently moving to a new position.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This is the correct property to use to determine successful completion of a (non-blocking) `Move()`, `MoveAbsolute()`, or `MoveMechanical()` request. `IsMoving` must be True immediately upon returning from any of these three movement calls (unless already at the requested position), and must remain True until successful completion, at which time `IsMoving` must become False.

---

### MechanicalPosition

**Type:** `float` (Read-Only)

**Description:** The raw mechanical position of the rotator in degrees, relative to the optics.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** Applications must not use this as a way to determine if a (non-blocking) `MoveMechanical()` has completed. The `MechanicalPosition` may transit through the requested position before finally settling. Use the `IsMoving` property. Added in version 3.

---

### Name

**Type:** `str` (Read-Only)

**Description:** The short name of the driver, for display purposes.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** The `Description` property is used to return info about the device rather than the driver.

---

### Position

**Type:** `float` (Read-Only)

**Description:** Current instantaneous Rotator position, allowing for any sync offset, in degrees.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** Applications must not use this as a way to determine if a (non-blocking) `Move()` or `MoveAbsolute()` has completed. The `Position` may transit through the requested position before finally settling. Use the `IsMoving` property. The `Sync()` method may be used to make `Position` indicate equatorial position angle. If `Sync()` has never been called, `Position` must be equal to `MechanicalPosition`. Once called, however, the offset must remain across driver starts and device reboots.

---

### Reverse

**Type:** `bool` (Read/Write)

**Description:** Set or indicate rotation direction reversal.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** Rotation is normally in degrees counterclockwise as viewed from behind the rotator, looking toward the sky. This corresponds to the direction of equatorial position angle. Set this property True to cause rotation opposite to equatorial PositionAngle, i.e. clockwise.

---

### StepSize

**Type:** `float` (Read-Only)

**Description:** The minimum rotation step size (degrees).

**Exceptions:**
- `PropertyNotImplementedException` - If the rotator does not know its step size
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

---

### SupportedActions

**Type:** `List[str]` (Read-Only)

**Description:** Returns the list of custom action names supported by this driver, to be used with `Action()`.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

> **Note:** This method, combined with `Action()`, is the supported mechanic for adding non-standard functionality. SupportedActions is a "discovery" mechanism that enables clients to know which Actions a device supports without having to exercise the Actions themselves.

---

### TargetPosition

**Type:** `float` (Read-Only)

**Description:** The destination position angle for `Move()` and `MoveAbsolute()`.

> **Note:** This will contain the new Position, including any `Sync()` offset, immediately upon return from a call to `Move()` or `MoveAbsolute()`.
