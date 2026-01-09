# ASCOM Telescope Interface

> This documentation is sourced from the official [ASCOM Telescope Interface](https://ascom-standards.org/newdocs/telescope.html) documentation.

**See Also:** [ASCOM Exceptions](ascom-exceptions.md) | [Common Types](ascom-common-types.md)

## Methods

### AbortSlew()

**Description:** Stops a slew in progress.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If no actions at all are supported.
- `ParkedException` - If the telescope is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Use the `Slewing` property to monitor stopping of the slew. When the mount has successfully stopped the slew, `Slewing` becomes False. Effective only after a call to either one of the slew methods or to `MoveAxis()`. Does nothing if no slew/motion is in progress. In the case of `MoveAxis()` or `SlewToAltAzAsync()`, `Tracking` must be returned to the state before the slew stopped.

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

> **Note:** Must be implemented but may throw `MethodNotImplementedException` if no custom actions are supported. Action names must be case insensitive.

---

### AxisRates()

**Description:** Determine the rates at which the telescope may be moved about the specified axis by the `MoveAxis()` method.

**Parameters:**
- `Axis` (`TelescopeAxes`) - The mechanical axis about which rate information is desired.

**Returns:** `List[Rate]` - A list or collection of `Rate` objects, each of which specifies a minimum and a maximum angular rate (degrees/second) at which the given axis of the mount may be moved.

**Exceptions:**
- `InvalidValueException` - If an invalid Axis is specified.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented. A mount may specify one or more ranges of rates on each of its axes. An empty list must be returned if `MoveAxis()` is not supported. Returned rates must always be positive.

---

### CanMoveAxis()

**Description:** Indicates whether the mount can be moved about the given mechanical axis.

**Parameters:**
- `Axis` (`TelescopeAxes`) - The axis about which this info is desired.

**Returns:** `bool` - Whether the mount may be moved about the requested axis.

**Exceptions:**
- `InvalidValueException` - If an invalid Axis is specified.
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

> **Note:** Non-blocking. On return, `Connecting` must be True unless already connected. Connection has successfully completed when `Connecting` becomes (or is) False. This is a mandatory method and must not throw a `MethodNotImplementedException`.

---

### DestinationSideOfPier()

**Description:** Returns the pointing state in which the mount will be if slewed to the given coordinates at this instant of time. Provided so apps can manage GEM flipping during an image sequence.

**Parameters:**
- `RightAscension` (`float`) - The destination right ascension (hours).
- `Declination` (`float`) - The destination declination (degrees, positive North).

**Returns:** `PierSide` - The pointing state indicating the side of pier in which the mount will be.

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented.
- `InvalidValueException` - If an invalid RightAscension or Declination is specified.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Disconnect()

**Description:** Disconnect from the device asynchronously. Use this to disconnect from a device rather than setting `Connected` to False.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Non-blocking. On return, `Connecting` must be True unless already disconnected. Disconnect has successfully completed when `Connecting` becomes (or is) False. This is a mandatory method and must not throw a `MethodNotImplementedException`.

---

### FindHome()

**Description:** Start moving the mount to the "home" position.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (and `CanFindHome` = False).
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Returns immediately with `Slewing` = True if the homing operation has successfully been started, or `Slewing` = False which means the mount is already at its home position. Use the `Slewing` property to monitor the operation. When the mount has successfully reached its home position, `Slewing` becomes False and `AtHome` becomes True.

---

### MoveAxis()

**Description:** Start motion of the mount about the given mechanical axis at the given non-zero angular rate or, for a zero angular rate, stop `MoveAxis()` movement about the axis and resume any configured tracking movement.

**Parameters:**
- `Axis` (`TelescopeAxes`) - The mechanical axis about which motion is desired.
- `Rate` (`float`) - The rate of rotation desired (degrees/second).

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented.
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `InvalidValueException` - If an invalid axis or rate value is given.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Clients must use the `Slewing` property to determine if the mount is moving, however you must explicitly call `MoveAxis()` with a zero rate to stop motion about the given axis. A call with `Rate` = 0 is required to stop motion and return to the previous tracking state of that axis. Do not use this method to effect guiding; use `PulseGuide()` instead.

---

### Park()

**Description:** Start slewing the mount to its park position.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (and `CanPark` = False).
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Returns immediately with `Slewing` = True if the parking operation has successfully been started. Use the `Slewing` property to monitor the operation. When the mount has successfully reached its park position, `Slewing` becomes False and `AtPark` becomes True. Parking should put the telescope into a state where its pointing accuracy must not be lost if it is power-cycled.

---

### PulseGuide()

**Description:** Moves the mount in the specified angular direction for the specified time (ms). The directions are in the Equatorial coordinate system only, regardless of the mount's `AlignmentMode`.

**Parameters:**
- `Direction` (`GuideDirections`) - Equatorial axis and direction of guide motion.
- `Duration` (`int`) - The duration of the guide-rate motion (milliseconds).

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanPulseGuide` is False).
- `InvalidValueException` - If an invalid `Direction` or `Duration` is given.
- `InvalidOperationException` - If the pulse guide cannot be effected (e.g., if the telescope is slewing or is not tracking).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous method. The method returns as soon the pulse-guiding operation has been successfully started, with `IsPulseGuiding` property True. However, you may find that `IsPulseGuiding` is False when you get around to checking it if the 'pulse' is short. If the device cannot have simultaneous `PulseGuide` operations in both RightAscension and Declination, it must throw `InvalidOperationException` when the overlapping operation is attempted.

---

### SetPark()

**Description:** Set the mount's park position to its current position.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSetPark` is False).
- `InvalidOperationException` - If the pulse guide cannot be effected (e.g., if the mount is slewing or is not tracking).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### SetupDialog()

**Description:** Launches a configuration dialogue box for the driver. The call will not return until the user clicks OK or cancels manually.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented. This is a blocking call. Please note that this method is only valid for COM drivers. Alpaca devices should provide configuration through the Alpaca HTML endpoints.

---

### SlewToAltAz()

**Description:** Move the mount synchronously to the given local horizontal coordinates, return only when slew is complete.

**Parameters:**
- `Azimuth` (`float`) - Destination azimuth coordinate (degrees, North-referenced, positive East/clockwise).
- `Altitude` (`float`) - Destination altitude coordinate (degrees, positive up).

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSlewAltAz` is False).
- `InvalidOperationException` - If `Tracking` = True, or if `AtPark` = True, or if the requested slew would fail due to hardware limit(s).
- `InvalidValueException` - If an invalid `Azimuth` or `Altitude` is given.
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Deprecated:** Use `SlewToAltAzAsync()` instead. Synchronous methods are deprecated in ITelescope V4.

---

### SlewToAltAzAsync()

**Description:** Start a slew to the given local horizontal coordinates.

**Parameters:**
- `Azimuth` (`float`) - Destination azimuth coordinate (degrees, North-referenced, positive East/clockwise).
- `Altitude` (`float`) - Destination altitude coordinate (degrees, positive up).

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSlewAltAzAsync` is False).
- `InvalidOperationException` - If `Tracking` = True, or if `AtPark` = True, or if the requested slew would fail due to hardware limit(s).
- `InvalidValueException` - If an invalid `Azimuth` or `Altitude` is given.
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Use the `Slewing` property to monitor the operation. When the requested coordinates have been successfully reached, `Slewing` becomes False. If the mount can slew to local horizontal coordinates, it must implement this method.

---

### SlewToCoordinates()

**Description:** Move the mount to the given equatorial coordinates per `EquatorialSystem`, return only when slew is complete.

**Parameters:**
- `RightAscension` (`float`) - Destination right ascension coordinate (hours, per `EquatorialSystem`). Copied to `TargetRightAscension`.
- `Declination` (`float`) - Destination declination coordinate (degrees, per `EquatorialSystem`). Copied to `TargetDeclination`.

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSlew` is False).
- `InvalidValueException` - If an invalid `RightAscension` or `Declination` is given.
- `InvalidOperationException` - If `Tracking` is False or if the requested slew would fail due to hardware limit(s).
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Deprecated:** Use `SlewToCoordinatesAsync()` instead. Synchronous methods are deprecated in ITelescope V4.

---

### SlewToCoordinatesAsync()

**Description:** Start a slew to the given equatorial coordinates per `EquatorialSystem`.

**Parameters:**
- `RightAscension` (`float`) - Destination right ascension coordinate (hours, per `EquatorialSystem`). Copied to `TargetRightAscension`.
- `Declination` (`float`) - Destination declination coordinate (degrees, per `EquatorialSystem`). Copied to `TargetDeclination`.

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSlewAsync` is False).
- `InvalidValueException` - If an invalid `RightAscension` or `Declination` is given.
- `InvalidOperationException` - If `Tracking` is False or if the requested slew would fail due to hardware limit(s).
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Use the `Slewing` property to monitor the operation. When the requested coordinates have been successfully reached, `Slewing` becomes False. If the mount can slew to equatorial coordinates, it must implement this method.

---

### SlewToTarget()

**Description:** Move the mount to the `TargetRightAscension` and `TargetDeclination` coordinates per `EquatorialSystem`, return only when slew is complete.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSlew` is False).
- `InvalidOperationException` - If `Tracking` is False or if the requested slew would fail due to hardware limit(s).
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Deprecated:** Use `SlewToTargetAsync()` instead. Synchronous methods are deprecated in ITelescope V4.

---

### SlewToTargetAsync()

**Description:** Start an asynchronous slew to the coordinates in `TargetRightAscension` and `TargetDeclination` per `EquatorialSystem`.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSlewAsync` is False).
- `InvalidOperationException` - If `Tracking` is False or if the requested slew would fail due to hardware limit(s).
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Use the `Slewing` property to monitor the operation. When the requested coordinates have been successfully reached, `Slewing` becomes False. If the mount can slew to equatorial coordinates, it must implement this method.

---

### SyncToAltAz()

**Description:** Match the mount's local horizontal coordinates to the given local horizontal coordinates.

**Parameters:**
- `Azimuth` (`float`) - Destination azimuth coordinate (degrees, North-referenced, positive East/clockwise).
- `Altitude` (`float`) - Destination altitude coordinate (degrees, positive up).

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSyncAltAz` is False).
- `InvalidValueException` - If an invalid `Azimuth` or `Altitude` is given.
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** May throw `DriverException` if `Tracking` is True.

---

### SyncToCoordinates()

**Description:** Match the mount's equatorial coordinates with the given equatorial coordinates.

**Parameters:**
- `RightAscension` (`float`) - Destination right ascension coordinate (hours, per `EquatorialSystem`). Copied to `TargetRightAscension`.
- `Declination` (`float`) - Destination declination coordinate (degrees, per `EquatorialSystem`). Copied to `TargetDeclination`.

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSync` is False).
- `InvalidValueException` - If an invalid `RightAscension` or `Declination` is given.
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** May throw `DriverException` if `Tracking` is False.

---

### SyncToTarget()

**Description:** Match the mount's equatorial coordinates with the coordinates in `TargetRightAscension` and `TargetDeclination`.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanSync` is False).
- `InvalidValueException` - If an invalid `RightAscension` or `Declination` is given.
- `ParkedException` - If the mount is parked (`AtPark` = True).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** May throw `DriverException` if `Tracking` is False.

---

### Unpark()

**Description:** Starts the process of taking the mount out of the Parked state.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the method is not implemented (`CanUnpark` is False).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This is an asynchronous (non-blocking) method. Unless already unparked (`AtPark` = False), this must return with `Slewing` = True until the unparking process completes, at which time both `Slewing` and `AtPark` must become False. Unparking a mount that is not parked is harmless and must always be successful.

---

## Properties

### AlignmentMode

**Type:** `AlignmentModes` (Read-Only)

**Description:** The mechanical construction of the mount (Alt/Az, Polar, German Polar), etc. This property reflects the design of the mount and cannot be changed at run-time. Regardless of their `AlignmentMode`, all mounts may operate in equatorial (RA/Dec) and/or local horizontal (Alt/Az) coordinate systems.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Altitude

**Type:** `float` (Read-Only)

**Description:** The altitude (degrees) above the horizon at which the mount is currently pointing (local horizontal coordinates).

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### ApertureArea

**Type:** `float` (Read-Only)

**Description:** The telescope's effective aperture area (square meters). The area takes into account any obstructions; it is the actual light-gathering area.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### ApertureDiameter

**Type:** `float` (Read-Only)

**Description:** The telescope's effective aperture diameter (meters).

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### AtHome

**Type:** `bool` (Read-Only)

**Description:** True if the mount is at the home position. Can be True only following a `FindHome()` operation. Must become False immediately upon any slewing operation. Must always be False if the mount does not support homing.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented. Use `Slewing` to determine successful completion of the `FindHome()` operation.

---

### AtPark

**Type:** `bool` (Read-Only)

**Description:** True if the mount is at the park position. Can be True only following successful completion of a `Park()` operation. When parked, the mount must be stationary or restricted to a small safe range of movement. `Tracking` must be False. Must always be False if the mount does not support parking.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented. Use `Slewing` to determine successful completion of the `Park()` operation.

---

### Azimuth

**Type:** `float` (Read-Only)

**Description:** The azimuth (degrees) at which the mount is currently pointing (local horizontal coordinates). Azimuth is per the usual alt/az coordinate convention: degrees North-referenced, positive East/clockwise.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanFindHome

**Type:** `bool` (Read-Only)

**Description:** True if the mount can find its home position. See `FindHome()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### CanPark

**Type:** `bool` (Read-Only)

**Description:** True if the mount can be parked. See `Park()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanPulseGuide

**Type:** `bool` (Read-Only)

**Description:** True if the mount can be pulse guided. See `PulseGuide()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanSetDeclinationRate

**Type:** `bool` (Read-Only)

**Description:** True if the Declination tracking rate may be offset. See `DeclinationRate`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### CanSetGuideRates

**Type:** `bool` (Read-Only)

**Description:** True if the guide rates can be adjusted. See `PulseGuide()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### CanSetPark

**Type:** `bool` (Read-Only)

**Description:** True if the mount's park position can be set. See `SetPark()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### CanSetPierSide

**Type:** `bool` (Read-Only)

**Description:** True if the mount can be force-flipped via setting `SideOfPier`. This applies to both German and simple/fork mounts.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### CanSetRightAscensionRate

**Type:** `bool` (Read-Only)

**Description:** True if the Right Ascension tracking rate may be offset. See `RightAscensionRate`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### CanSetTracking

**Type:** `bool` (Read-Only)

**Description:** True if the mount's sidereal tracking may be turned on and off. See `Tracking`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### CanSlew

**Type:** `bool` (Read-Only)

**Description:** True if the mount can synchronously slew to equatorial coordinates. See `SlewToCoordinates()`, `SlewToCoordinatesAsync()`, `SlewToTarget()`, and `SlewToTargetAsync()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented. Synchronous methods are deprecated in ITelescope V4; clients should not use them.

---

### CanSlewAltAz

**Type:** `bool` (Read-Only)

**Description:** True if the mount can synchronously slew to alt/az coordinates. See `SlewToAltAz()` and `SlewToAltAzAsync()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented. Synchronous methods are deprecated in ITelescope V4; clients should not use them.

---

### CanSlewAltAzAsync

**Type:** `bool` (Read-Only)

**Description:** True if the mount can asynchronously slew to alt/az coordinates. See `SlewToAltAzAsync()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented. Clients should always use asynchronous slewing if available. If the mount can slew, driver authors must implement asynchronous slewing.

---

### CanSlewAsync

**Type:** `bool` (Read-Only)

**Description:** True if the mount can asynchronously slew to equatorial coordinates. See `SlewToCoordinatesAsync()` and `SlewToTargetAsync()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented. Clients should always use asynchronous slewing if available. If the mount can slew, driver authors must implement asynchronous slewing.

---

### CanSync

**Type:** `bool` (Read-Only)

**Description:** True if the mount can be synchronized to equatorial coordinates. See `SyncToCoordinates()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### CanSyncAltAz

**Type:** `bool` (Read-Only)

**Description:** True if the mount can be synchronized to alt/az coordinates. See `SyncToAltAz()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### CanUnpark

**Type:** `bool` (Read-Only)

**Description:** True if the mount can be unparked. See `Unpark()` and `Park()`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### Connected

**Type:** `bool` (Read/Write)

**Description:** Retrieve or set the connected state of the device. Set True to connect to the device hardware; set False to disconnect.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented. Writing is deprecated; use the newer `Connect()` and `Disconnect()` methods with the `Connecting` property instead.

---

### Connecting

**Type:** `bool` (Read-Only)

**Description:** Returns True while the device is undertaking an asynchronous connect or disconnect operation. This is the correct property for determining when the non-blocking methods `Connect()` or `Disconnect()` have completed.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented.

---

### Declination

**Type:** `float` (Read-Only)

**Description:** The mount's current Declination (degrees) in the current `EquatorialSystem`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### DeclinationRate

**Type:** `float` (Read/Write)

**Description:** Read or set a secular rate of change to the mount's `Declination` in arc seconds per UTC (SI) second. This is an offset from 0 (no change in declination). Offset tracking is most commonly used to track a solar system object such as a minor planet or comet.

**Exceptions:**
- `PropertyNotImplementedException` - If `CanSetDeclinationRate` is False yet an attempt is made to write to this property.
- `InvalidOperationException` - If `TrackingRate` is not `driveSidereal`.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** `DeclinationRate` read must be implemented. Reading this property must return a value of zero if `TrackingRate` is not `driveSidereal`.

---

### Description

**Type:** `str` (Read-Only)

**Description:** Description of the device such as manufacturer and model number. Any ASCII characters may be used. The description length must be a maximum of 64 characters.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented. This describes the device, not the driver.

---

### DeviceState

**Type:** `List[StateValue]` (Read-Only)

**Description:** List of `StateValue` objects representing the operational properties of this device. This device must return the following operational properties if they are known: `Altitude`, `AtHome`, `AtPark`, `Azimuth`, `Declination`, `IsPulseGuiding`, `RightAscension`, `SideOfPier`, `SiderealTime`, `Slewing`, `Tracking`, `UTCDate`, and `TimeStamp`.

---

### DoesRefraction

**Type:** `bool` (Read/Write)

**Description:** True if the mount applies atmospheric refraction to corrections.

**Exceptions:**
- `PropertyNotImplementedException` - If this property is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** `DoesRefraction` read must be implemented.

---

### DriverInfo

**Type:** `str` (Read-Only)

**Description:** Descriptive and version information about the ASCOM driver. This string may contain line endings and may be hundreds to thousands of characters long.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented.

---

### DriverVersion

**Type:** `str` (Read-Only)

**Description:** String containing only the major and minor version of the driver (e.g., "n.n"). This should not to be confused with the `InterfaceVersion` property.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented.

---

### EquatorialSystem

**Type:** `EquatorialCoordinateType` (Read-Only)

**Description:** The current equatorial coordinate system used by the mount. Most mounts use topocentric coordinates. Some high-end research mounts use J2000 coordinates.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### FocalLength

**Type:** `float` (Read-Only)

**Description:** The telescope's focal length in meters.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### GuideRateDeclination

**Type:** `float` (Read/Write)

**Description:** The current rate of change of Declination (deg/sec) for guiding, typically via `PulseGuide`. This is the rate for both hardware/relay guiding and for `PulseGuide`. This value must be set to a default upon startup.

**Exceptions:**
- `InvalidValueException` - If an invalid guide rate is set.
- `PropertyNotImplementedException` - If the property is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### GuideRateRightAscension

**Type:** `float` (Read/Write)

**Description:** The current rate of change of Right Ascension (deg/sec) for guiding, typically via `PulseGuide`. This is the rate for both hardware/relay guiding and for `PulseGuide`. This value is in degrees per second, not in hours per second. This value must be set to a default upon startup.

**Exceptions:**
- `InvalidValueException` - If an invalid guide rate is set.
- `PropertyNotImplementedException` - If the property is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### InterfaceVersion

**Type:** `int` (Read-Only)

**Description:** ASCOM Device interface definition version that this device supports. Should return 4 for this interface version. This is a single integer indicating the version of this specific ASCOM universal interface definition.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented.

---

### IsPulseGuiding

**Type:** `bool` (Read-Only)

**Description:** True if the mount is currently executing a `PulseGuide()` command. Use this property to determine when a (non-blocking) pulse guide command has completed.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented (`CanPulseGuide` is False).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** A pulse guide command may be so short that you won't see this equal to True.

---

### Name

**Type:** `str` (Read-Only)

**Description:** The short name of the driver, for display purposes.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented. The `Description` property is used to return info about the device rather than the driver.

---

### RightAscension

**Type:** `float` (Read-Only)

**Description:** The mount's current right ascension (hours) in the current `EquatorialSystem`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### RightAscensionRate

**Type:** `float` (Read/Write)

**Description:** Read or set a secular rate of change to the mount's `RightAscension` (seconds of RA per sidereal second). This is an offset from sidereal tracking rate. Offset tracking is most commonly used to track a solar system object such as a minor planet or comet.

**Exceptions:**
- `PropertyNotImplementedException` - If `CanSetRightAscensionRate` is False yet an attempt is made to write to this property.
- `InvalidOperationException` - If `TrackingRate` is not `driveSidereal`.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** `RightAscensionRate` read must be implemented. To convert a given rate in units of sidereal seconds per UTC (clock) second, multiply the value by 0.9972695677. Reading this property must return a value of zero if `TrackingRate` is not `driveSidereal`.

---

### SideOfPier

**Type:** `PierSide` (Read/Write)

**Description:** Start a change of, or return, the mount's pointing state. Writing to change pointing state returns immediately with `Slewing` = True if the state change (e.g., GEM flip) operation has successfully been started.

**Exceptions:**
- `PropertyNotImplementedException` - If the mount does not report its pointing state, or if it doesn't support changing pointing state by writing to `SideOfPier` (`CanSetPierSide` = False).
- `InvalidValueException` - If an invalid `PierSide` value is set.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** "SideOfPier" is a misnomer; this method actually refers to the mount's pointing state. For German Equatorial mounts there is a complex relationship between pointing state and the physical side of the pier on which the mount resides.

---

### SiderealTime

**Type:** `float` (Read-Only)

**Description:** Local apparent sidereal time (hours). Local Apparent Sidereal Time is the sidereal time used for pointing mounts, and must be calculated from the Greenwich Mean Sidereal time, longitude, nutation in longitude and True ecliptic obliquity.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** This property must be implemented.

---

### SiteElevation

**Type:** `float` (Read/Write)

**Description:** The observing site's elevation (meters) above mean sea level.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented at all, or if writing to the property is not implemented.
- `InvalidValueException` - If the given value is outside the range -300 through 10000 meters.
- `InvalidOperationException` - When `SiteElevation` is read and the mount cannot provide this property itself and a value has not yet been established by writing to the property.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### SiteLatitude

**Type:** `float` (Read/Write)

**Description:** The latitude (degrees) of the observing site.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented at all, or if writing to the property is not implemented.
- `InvalidValueException` - If the given value is outside the range -90 through +90 degrees latitude.
- `InvalidOperationException` - When `SiteLatitude` is read and the mount cannot provide this property itself and a value has not yet been established by writing to the property.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### SiteLongitude

**Type:** `float` (Read/Write)

**Description:** The longitude (degrees, positive east) of the observing site. West longitude is negative.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented at all, or if writing to the property is not implemented.
- `InvalidValueException` - If the given value is outside the range -180 through +180 degrees longitude.
- `InvalidOperationException` - When `SiteLongitude` is read and the mount cannot provide this property itself and a value has not yet been established by writing to the property.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### SlewSettleTime

**Type:** `int` (Read/Write)

**Description:** The post-slew settling time (seconds). Artificially lengthens all slewing operations, delaying setting `Slewing` to False even though the slew actually completes. Useful for mounts or buildings that require additional mechanical settling time after a slew to stabilize.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented.
- `InvalidValueException` - If the given value is negative or preposterously high.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Slewing

**Type:** `bool` (Read-Only)

**Description:** True if the mount is in motion resulting from a slew, parking, find-home, or a move-axis operation. This is the correct property to use to determine successful completion of a (non-blocking) slew operation.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented (no slewing capabilities of the mount).
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** `Slewing` must be True immediately upon returning from any slew call, and must remain True until successful completion. `Slewing` must also be true during any `MoveAxis()` operations. `Slewing` must not be True during `PulseGuide()` operations or application of `RightAscensionRate` or `DeclinationRate` offsets.

---

### SupportedActions

**Type:** `List[str]` (Read-Only)

**Description:** Returns the list of custom action names supported by this driver, to be used with `Action()`.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Must be implemented. This method, combined with `Action()`, is the supported mechanic for adding non-standard functionality.

---

### TargetDeclination

**Type:** `float` (Read/Write)

**Description:** Set or return the declination (degrees, positive North) for the target of an equatorial slew or sync operation. This is a pre-set target coordinate for `SlewToTargetAsync()` and `SyncToTarget()`. This is set by a call to `SlewToCoordinatesAsync()` from the `Declination` parameter.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented.
- `InvalidValueException` - If the given value is outside the range -90 through 90 degrees.
- `InvalidOperationException` - If the value is read before being set for the first time.
- `ParkedException` - If the mount is parked.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### TargetRightAscension

**Type:** `float` (Read/Write)

**Description:** Set or return the right ascension (hours) for the target of an equatorial slew or sync operation. This is a pre-set target coordinate for `SlewToTargetAsync()` and `SyncToTarget()`. This is set by a call to `SlewToCoordinatesAsync()` from the `RightAscension` parameter.

**Exceptions:**
- `PropertyNotImplementedException` - If the property is not implemented.
- `InvalidValueException` - If the given value is outside the range 0 to 24 hours.
- `InvalidOperationException` - If the value is read before being set for the first time.
- `ParkedException` - If the mount is parked.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### Tracking

**Type:** `bool` (Read/Write)

**Description:** The on/off state of the mount's sidereal tracking drive. When tracking is turned on, the mount must use the last selected `TrackingRate`. While tracking at sidereal rate, a mount is holding its `RightAscension` and `Declination` constant.

**Exceptions:**
- `PropertyNotImplementedException` - If writing to the property (tracking control) is not implemented (if `CanSetTracking` is False).
- `NotConnectedException` - If the device is not connected.
- `ParkedException` - When Tracking is set True and the telescope is parked (`AtPark` is True).
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Reading must be implemented.

---

### TrackingRate

**Type:** `DriveRates` (Read/Write)

**Description:** The current (sidereal) tracking rate of the mount, from `DriveRates`.

**Exceptions:**
- `InvalidValueException` - If the value being written is not one of the `DriveRates` or if the requested rate is not supported by the mount.
- `PropertyNotImplementedException` - If writing to the property (changing tracking rate) is not implemented at all.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Reading the tracking rate must be supported.

---

### TrackingRates

**Type:** `List[DriveRates]` (Read-Only)

**Description:** Return a list of supported `DriveRates` values. At a minimum, this list must contain an item for `driveSidereal`.

**Exceptions:**
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

---

### UTCDate

**Type:** `datetime` (Read/Write)

**Description:** The UTC date/time of the mount's time source.

**Exceptions:**
- `InvalidValueException` - If an illegal datetime value is written to the property.
- `InvalidOperationException` - When UTCDate is read and the mount cannot provide this property itself and a value has not yet been established by writing to the property.
- `PropertyNotImplementedException` - If writing to the property (changing the mount's UTC date-time) is not implemented.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

> **Note:** Reading this property must be implemented.

---

## Enumerated Constants

### AlignmentModes

The alignment mode (geometry) of the mount. See `AlignmentMode`.

| Symbol | Value | Description |
|--------|-------|-------------|
| `algAltAz` | 0 | Altitude-Azimuth type mount |
| `algPolar` | 1 | Polar (equatorial) mount other than German equatorial |
| `algGermanPolar` | 2 | German equatorial type mount |

---

### DriveRates

Well-known mount tracking rates. See `TrackingRate`.

| Symbol | Value | Description |
|--------|-------|-------------|
| `driveSidereal` | 0 | Sidereal tracking rate (15.041 arcseconds per second) |
| `driveLunar` | 1 | Lunar tracking rate (14.685 arcseconds per second) |
| `driveSolar` | 2 | Solar tracking rate (15.0 arcseconds per second) |
| `driveKing` | 3 | King tracking rate (15.0369 arcseconds per second) |

---

### EquatorialCoordinateType

Equatorial coordinate systems used by mounts.

| Symbol | Value | Description |
|--------|-------|-------------|
| `equOther` | 0 | Custom or unknown equinox and/or reference frame |
| `equTopocentric` | 1 | Topocentric coordinates |
| `equJ2000` | 2 | J2000 equator/equinox |
| `equJ2050` | 3 | J2050 equator/equinox |
| `equB1950` | 4 | B1950 equinox, FK4 reference frame |

---

### GuideDirections

The direction in which a `PulseGuide()` guide-rate motion is to be made. These are not mechanical axes; these are directions in the equatorial coordinate system. The North/South directions are references to equatorial coordinates and must be independent of the pointing state (flip state) of the mount.

| Symbol | Value | Description |
|--------|-------|-------------|
| `guideNorth` | 0 | North (+ declination) |
| `guideSouth` | 1 | South (- declination) |
| `guideEast` | 2 | East (+ right ascension) |
| `guideWest` | 3 | West (- right ascension) |

---

### PierSide

The pointing states of mounts.

| Symbol | Value | Description |
|--------|-------|-------------|
| `pierEast` | 0 | Normal pointing state |
| `pierWest` | 1 | Through the pole pointing state |
| `pierUnknown` | -1 | Unknown or indeterminate |

> **Note:** The PierSide enum is named PointingState in the ASCOM Library.

---

### TelescopeAxes

These are the mechanical axes of the mount. See `MoveAxis()`. The direction of rotation (plus or minus) is left undefined and dependent on the mount's mechanical construction.

| Symbol | Value | Description |
|--------|-------|-------------|
| `axisPrimary` | 0 | Primary mechanical axis (typically RA or Azimuth) |
| `axisSecondary` | 1 | Secondary mechanical axis (typically Dec or Altitude) |
| `axisTertiary` | 2 | Tertiary mechanical axis (e.g., rotator or special axis) |

> **Note:** The meaning of primary, secondary, and tertiary axis varies with the mount mechanical geometry. These are not equatorial coordinate axes; they are mechanical axes.
