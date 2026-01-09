# ASCOM Switch Interface

> This documentation is sourced from the official [ASCOM Switch Interface](https://ascom-standards.org/newdocs/switch.html) documentation.

**See Also:** [ASCOM Exceptions](ascom-exceptions.md) | [Common Types](ascom-common-types.md)

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

**Notes:**
- Must be implemented but may throw `MethodNotImplementedException` if no custom actions are supported
- This method, combined with `SupportedActions`, is the supported mechanic for adding non-standard functionality
- Action names must be case insensitive

---

### CanAsync()

**Description:** Flag indicating whether the specified switch can operate asynchronously.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `bool` - True if the specified switch device can operate asynchronously.

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3
- This is a mandatory method and must not throw a `MethodNotImplementedException`
- See `SetAsync()` for details of asynchronous switch operations

---

### CancelAsync()

**Description:** Cancels an in-progress asynchronous state change operation.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** Nothing

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3
- This is a mandatory method and must not throw a `MethodNotImplementedException`
- On return, calls to `StateChangeComplete()` for this switch will raise an `OperationCancelledException`
- See `SetAsync()` for details of asynchronous switch operations

---

### CanWrite()

**Description:** Indicates whether the specified switch can be written to.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `bool` - True if the specified switch can be written to.

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 2
- Examples of switches that cannot be written to include a limit switch or a sensor

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

**Notes:**
- **Deprecated** since version 3. Use the more flexible `Action()` and `SupportedActions` mechanic instead.

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

**Notes:**
- **Deprecated** since version 3. Use the more flexible `Action()` and `SupportedActions` mechanic instead.

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

**Notes:**
- **Deprecated** since version 3. Use the more flexible `Action()` and `SupportedActions` mechanic instead.

---

### Connect()

**Description:** Connect to the device asynchronously.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3 as the preferred asynchronous connection mechanic
- Use this to connect to a device rather than setting `Connected` to True
- On return, `Connecting` must be True unless already connected
- Connection has successfully completed when `Connecting` becomes (or is) False

---

### Disconnect()

**Description:** Disconnect from the device asynchronously.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3 as the preferred asynchronous disconnection mechanic
- Use this to disconnect from a device rather than setting `Connected` to False
- On return, `Connecting` must be True unless already disconnected
- Disconnect has successfully completed when `Connecting` becomes (or is) False

---

### GetSwitch()

**Description:** Return the state of the specified switch as a boolean.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `bool` - The state of the switch.

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `InvalidOperationException` - If there is a temporary condition that prevents the switch's value being returned, including after power-up if the switch's state is unknown
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- This is a mandatory method and must not throw a `MethodNotImplementedException`
- Do not use this to determine if a `SetAsync()` has completed; use `StateChangeComplete()` instead
- For a variable output device, `GetSwitch()` must return False if at its minimum value, else True
- Some switches do not support reading their state although they do allow state to be set

---

### GetSwitchDescription()

**Description:** Gets the description of the specified switch.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `str` - String giving the switch description.

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 2
- This is to allow a fuller description of the switch to be returned, for example for a tool tip

---

### GetSwitchName()

**Description:** Gets the "short" name of the specified switch.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `str` - String giving the switch name.

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

---

### GetSwitchValue()

**Description:** Return the value of the specified switch as a float.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `float` - The value of the switch. Expected to be between `MinSwitchValue()` and `MaxSwitchValue()` in steps of `SwitchStep()`.

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `InvalidOperationException` - If there is a temporary condition that prevents the device value being returned, including after power-up if the switch's state is unknown
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 2
- This is a mandatory method and must not throw a `MethodNotImplementedException`
- Do not use this to determine if a `SetAsyncValue()` has completed; use `StateChangeComplete()` instead
- For a boolean on/off switch, `GetSwitchValue()` must return `MinSwitchValue` if off, and `MaxSwitchValue` if on

---

### MaxSwitchValue()

**Description:** Returns the maximum value for the specified switch.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `float` - The maximum value to which this switch can be set or which a read-only sensor will return.

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 2
- This is a mandatory method and must not throw a `MethodNotImplementedException`
- This must be greater than `MinSwitchValue()` for the switch
- For an on/off switch, `MaxSwitchValue` must return the value 1.0

---

### MinSwitchValue()

**Description:** Returns the minimum value for the specified switch.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `float` - The minimum value to which this switch can be set or which a read-only sensor will return.

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 2
- This is a mandatory method and must not throw a `MethodNotImplementedException`
- This must be less than `MaxSwitchValue()` for the switch
- For an on/off switch, `MinSwitchValue` must return the value 0.0

---

### SetAsync()

**Description:** Asynchronously set a switch to the specified boolean on/off state.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)
- `State` (`bool`) - The required control state (on or off)

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If `CanAsync()` is False for the switch
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3
- Non-blocking: Returns immediately after successfully starting the state change with `StateChangeComplete()` for the given switch = False
- After the state change has completed, `StateChangeComplete()` becomes True
- Switch devices are numbered from 0 to `MaxSwitch` - 1
- `GetSwitchValue()` must return `MaxSwitchValue()` if state is True, and `MinSwitchValue()` if state is False

---

### SetAsyncValue()

**Description:** Asynchronously set a switch to the specified float value.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)
- `Value` (`float`) - The value to be set, between `MinSwitchValue()` and `MaxSwitchValue()` for the switch

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If either `CanWrite()` or `CanAsync()` is False for the switch
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1), or if `Value` is not between `MinSwitchValue()` and `MaxSwitchValue()`
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3

---

### SetSwitch()

**Description:** Set a switch to the specified boolean on/off state.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)
- `State` (`bool`) - The required control state (on or off)

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If `CanWrite()` is False for the switch
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- `GetSwitchValue()` must return `MaxSwitchValue()` if state is True, and `MinSwitchValue()` if state is False

---

### SetSwitchName()

**Description:** Set a switch's name to the specified value.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)
- `Name` (`str`) - The name of the switch

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If the switch name cannot be set by the client
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 2

---

### SetSwitchValue()

**Description:** Set a switch's value to the specified float value.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)
- `Value` (`float`) - The value to be set, between `MinSwitchValue()` and `MaxSwitchValue()` for the switch

**Returns:** Nothing

**Exceptions:**
- `MethodNotImplementedException` - If `CanWrite()` is False for the switch
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1), or if `Value` is not between `MinSwitchValue()` and `MaxSwitchValue()`
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 2

---

### SetupDialog()

**Description:** Launch a configuration dialog box for the driver.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- The call will not return until the user clicks OK or Cancel manually
- Must be implemented and must not throw a `MethodNotImplementedException`
- This method is only valid for COM drivers; Alpaca devices should provide configuration through HTML endpoints

---

### StateChangeComplete()

**Description:** Indicates whether an asynchronous state change operation has completed.

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `bool` - True if the last `SetAsync()` or `SetAsyncValue()` has completed and the switch is in the requested state.

**Exceptions:**
- `MethodNotImplementedException` - If `CanAsync()` is False for the switch
- `OperationCancelledException` - If an in-progress state change is cancelled by a call to `CancelAsync()`
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3

---

### SwitchStep()

**Description:** The step size that the specified switch supports (the difference between successive values of the switch).

**Parameters:**
- `Id` (`int`) - The specified switch number (0 to `MaxSwitch` - 1)

**Returns:** `float` - The step size for this switch.

**Exceptions:**
- `InvalidValueException` - If `Id` is out of range (0 to `MaxSwitch` - 1)
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 2
- Must be implemented and must not throw a `MethodNotImplementedException`
- `SwitchStep` must be greater than zero
- The number of steps can be calculated as: `((MaxSwitchValue - MinSwitchValue) / SwitchStep) + 1`

---

## Properties

### Connected

**Type:** `bool` (Read/Write)

**Description:** Retrieve or set the connected state of the device.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Setting this property to True will attempt to connect to the device
- Setting this property to False will disconnect from the device
- In version 3+, prefer using `Connect()` and `Disconnect()` methods instead
- Do not use a `NotConnectedException` here; that exception is for use in other methods that require a connection

---

### Connecting

**Type:** `bool` (Read-Only)

**Description:** Returns True while the device is undertaking an asynchronous connect or disconnect operation.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3
- Must be implemented and must not throw a `PropertyNotImplementedException`
- Use this to monitor the progress of `Connect()` and `Disconnect()` operations
- Completion is when `Connecting` becomes False after calling either method

---

### Description

**Type:** `str` (Read-Only)

**Description:** A description of the device, such as manufacturer and model number.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Any ASCII characters may be used
- The description length must be a maximum of 64 characters (for compatibility with FITS headers)
- This describes the device, not the driver; see `DriverInfo` for driver information

---

### DeviceState

**Type:** `List[StateValue]` (Read-Only)

**Description:** Returns the device's operational state in a single call.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3
- Returns a list of `StateValue` objects containing name/value pairs for operational states
- For Switch devices with multiple controllable switches, property names include the switch number (e.g., `GetSwitch0`, `GetSwitch1`, etc.)
- DeviceState property names include:
  - `GetSwitch0` through `GetSwitch(MaxSwitch-1)`
  - `GetSwitchValue0` through `GetSwitchValue(MaxSwitch-1)`
  - `StateChangeComplete0` through `StateChangeComplete(MaxSwitch-1)`
  - `TimeStamp`

---

### DriverInfo

**Type:** `str` (Read-Only)

**Description:** Descriptive and version information about the ASCOM driver.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- This string may contain line endings and may be hundreds to thousands of characters long
- It is intended to display detailed information about the driver including version numbers
- See `Description` for information about the device itself
- To get the driver version in a parseable string, use `DriverVersion`

---

### DriverVersion

**Type:** `str` (Read-Only)

**Description:** A string containing only the major and minor version of the driver formatted as 'n.n'.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- This must be in the form "n.n"
- Should not be confused with `InterfaceVersion`, which is the version of the specification supported by the driver
- On systems with a comma as the decimal point, you may need to make accommodations to parse the value

---

### InterfaceVersion

**Type:** `int` (Read-Only)

**Description:** The ASCOM device interface definition version that this device supports.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Should return 3 for devices implementing ISwitchV3
- Must be implemented and must not throw a `PropertyNotImplementedException`
- This is a single integer indicating the version of the interface definition
- Should not be confused with `DriverVersion`, which is the major.minor version of the driver

---

### MaxSwitch

**Type:** `int` (Read-Only)

**Description:** Count of switches managed by this driver.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Switches are numbered from 0 to `MaxSwitch` - 1

---

### Name

**Type:** `str` (Read-Only)

**Description:** The short name of the driver, for display purposes.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Must be implemented and must not throw a `PropertyNotImplementedException`
- The `Description` property is used to return info about the device rather than the driver

---

### SupportedActions

**Type:** `List[str]` (Read-Only)

**Description:** Returns the list of custom action names supported by this driver.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Must be implemented but may return an empty list if no custom actions are supported
- Must not throw a `PropertyNotImplementedException`
- Action names are case insensitive
- Use `Action()` method to invoke these custom actions
- SupportedActions is a "discovery" mechanism that enables clients to know which Actions a device supports
