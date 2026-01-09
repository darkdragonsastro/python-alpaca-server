# ASCOM Exceptions

> This documentation is sourced from the official [ASCOM Exceptions](https://ascom-standards.org/newdocs/exceptions.html) documentation.

The ASCOM interfaces share a set of standard exception classes. These exceptions provide a consistent way for drivers to communicate errors to client applications.

**Note:** The exception codes shown here are generic values used by Alpaca or any other environment. For classic ASCOM COM in the Windows environment, these 16-bit codes are logically OR'ed with `0x80040000` (Windows generic user exception). For example, the value `0x40B` would appear in the COM context as `0x8004040B`.

## ActionNotImplementedException

**Numeric Value:** `0x040C` (1036)

**Description:** Exception thrown by a driver when it receives an unknown command through the `Action` method.

**When to throw:** Throw this exception when the driver's `Action` method receives a command name that it does not recognize or support.

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction.

## DriverException

**Numeric Value:** `0x500` - `0xFFF` (1280 - 4095, driver-defined)

**Description:** Generic driver exception that allows drivers to report custom errors with their own error codes.

**When to throw:** This is the generic driver exception. Drivers are permitted to directly throw these exceptions. This exception should **only** be thrown if there is no other more appropriate exception already defined. The specific exceptions listed here should be thrown where appropriate rather than using the more generic `DriverException`. Conform will not accept `DriverException` where more appropriate exceptions are already defined.

**Parameters:**
- `number` (int): The error number in the range `0x500`-`0xFFF`. The driver may choose this number for its own purposes.
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction.

## InvalidOperationException

**Numeric Value:** `0x40B` (1035)

**Description:** This exception should be thrown by the driver to reject a command from the client.

**When to throw:** Throw this exception when a client attempts an operation that is not valid given the current state of the device or driver. For example, attempting to set a tracking rate offset when the tracking rate is not sidereal.

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction.

## InvalidValueException

**Numeric Value:** `0x401` (1025)

**Description:** Exception to report an invalid value supplied to a driver.

**When to throw:** Throw this exception when a client provides a value that is outside the acceptable range or otherwise invalid for a property or method parameter.

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction such as the legal range for the value.

## MethodNotImplementedException

**Numeric Value:** `0x400` (1024)

**Description:** All methods defined by the relevant ASCOM standard interface must exist in each driver. However, those methods do not all have to be *implemented*. The minimum requirement for each defined method is to throw `MethodNotImplementedException`.

**When to throw:** Throw this exception from any method that exists in the interface but is not implemented by the driver. The message should at minimum contain the method name.

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction. **At a minimum it must contain the method name.**

**Note:** For historical reasons, this exception shares the same numeric code as `PropertyNotImplementedException`.

## NotConnectedException

**Numeric Value:** `0x407` (1031)

**Description:** This exception should be thrown when an operation is attempted that requires communication with the device, but the device is disconnected.

**When to throw:** Throw this exception when the driver is not connected to the device and an operation requiring device communication is attempted. This refers to the driver not being connected to the device. It is **not** for network outages or bad URLs.

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction.

## OperationCancelledException

**Numeric Value:** `0x40E` (1038)

**Description:** This exception should be thrown to indicate that an (asynchronous) in-progress operation has been cancelled.

**When to throw:** Throw this exception when an asynchronous operation that was in progress has been cancelled, typically by the user or client application calling a cancel or abort method.

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction.

## ParkedException

**Numeric Value:** `0x408` (1032)

**Description:** This exception should be thrown to indicate that movement (or other invalid operation) was attempted while the device was in a parked state.

**When to throw:** Throw this exception when an operation that requires the device to be unparked is attempted while the device is parked (e.g., attempting to slew a telescope or rotate a dome while parked).

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction.

## PropertyNotImplementedException

**Numeric Value:** `0x400` (1024)

**Description:** All properties defined by the relevant ASCOM standard interface must exist in each driver. However, those properties do not all have to be *implemented*. The minimum requirement for each defined property is to throw `PropertyNotImplementedException`.

**When to throw:** Throw this exception from any property getter or setter that exists in the interface but is not implemented by the driver. The message should at minimum contain the property name.

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction. **At a minimum it must contain the property name.**

**Note:** For historical reasons, this exception shares the same numeric code as `MethodNotImplementedException`.

## SlavedException

**Numeric Value:** `0x409` (1033)

**Description:** This exception should be used to indicate that movement (or other invalid operation) was attempted while the device was in slaved mode. This applies primarily to Dome drivers.

**When to throw:** Throw this exception when an operation that is not allowed in slaved mode is attempted while the device is slaved to another device (e.g., attempting to manually slew a dome that is slaved to a telescope).

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction.

## ValueNotSetException

**Numeric Value:** `0x402` (1026)

**Description:** Exception to report that no value has yet been set for this property.

**When to throw:** Throw this exception when a property is read before a value has been assigned to it, and no sensible default exists.

**Parameters:**
- `message` (str): The textual error message, which should always be informative and useful to help identify and solve the problem. It may even contain suggestions for correction.
