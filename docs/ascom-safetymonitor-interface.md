# ASCOM SafetyMonitor Interface

> This documentation is sourced from the official [ASCOM SafetyMonitor Interface](https://ascom-standards.org/newdocs/safetymonitor.html) documentation.

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
- Use `Connecting` to monitor connection progress
- When `Connecting` becomes False, check `Connected` to confirm successful connection

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
- Use `Connecting` to monitor disconnection progress

---

### SetupDialog()

**Description:** Launch a configuration dialog box for the driver.

**Parameters:** None

**Returns:** Nothing

**Exceptions:**
- `NotConnectedException` - If the device is not connected and this method requires a connection to be established
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- The call will not return until the user clicks OK or Cancel manually
- Must be implemented but may throw `MethodNotImplementedException` if no setup dialog is available

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

---

### Connecting

**Type:** `bool` (Read-Only)

**Description:** Returns True while the device is undertaking an asynchronous connect or disconnect operation.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3
- Use this to monitor the progress of `Connect()` and `Disconnect()` operations

---

### Description

**Type:** `str` (Read-Only)

**Description:** A description of the device, such as manufacturer and model number.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Any ASCII characters may be used
- The string shall not exceed 68 characters (for compatibility with FITS headers)

---

### DeviceState

**Type:** `List[StateValue]` (Read-Only)

**Description:** Returns the device's operational state in a single call.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Added in version 3
- Returns a list of `StateValue` objects containing the name/value pairs for operational states
- For SafetyMonitor, this includes: `IsSafe`, `Connected`, and `TimeStamp`

---

### DriverInfo

**Type:** `str` (Read-Only)

**Description:** Descriptive and version information about the driver.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- This string may contain line endings and may be hundreds to thousands of characters long
- It is intended to display detailed information about the driver including version numbers

---

### DriverVersion

**Type:** `str` (Read-Only)

**Description:** A string containing only the major and minor version of the driver formatted as 'm.n'.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- This property is for compatibility with the ASCOM Driver Development Kit

---

### InterfaceVersion

**Type:** `int` (Read-Only)

**Description:** The interface version number that this device supports.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- This should return 3 for devices implementing ISafetyMonitorV3

---

### IsSafe

**Type:** `bool` (Read-Only)

**Description:** Indicates whether the monitored state is safe for use.

**Exceptions:**
- `NotConnectedException` - If the device is not connected
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Must be implemented and must not throw `PropertyNotImplementedException`
- Returns True if the state is safe, False if it is unsafe
- This is the primary property for SafetyMonitor devices
- Multiple SafetyMonitor devices can be used to monitor different aspects of observatory safety (e.g., weather, power, etc.)

---

### Name

**Type:** `str` (Read-Only)

**Description:** The short name of the driver, for display purposes.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- The string shall not exceed 68 characters (for compatibility with FITS headers)

---

### SupportedActions

**Type:** `List[str]` (Read-Only)

**Description:** Returns the list of custom action names supported by this driver.

**Exceptions:**
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions

**Notes:**
- Must be implemented but may return an empty list if no custom actions are supported
- Action names are case insensitive
- Use `Action()` method to invoke these custom actions
