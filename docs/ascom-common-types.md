# ASCOM Common Types

> This documentation is sourced from the official ASCOM documentation at
> [ascom-standards.org](https://ascom-standards.org/newdocs/).

## StateValue

**Description:** Each device type has a property `DeviceState` which returns a set of aggregated operational properties of the device. Each of these operational properties are returned as an object with `Name` and `Value` properties.

### Properties

#### Name

**Type:** `string`

**Description:** The name of an operational property. The name is case sensitive and must match the property name's spelling and casing in the relevant ASCOM interface specification.

#### Value

**Type:** `object`

**Description:** The corresponding value of the named operational property. The `StateValue.Value` property has the object type so that it can accept any type including the types commonly used in ASCOM interfaces such as int16, int32, double, string and enum. This approach avoids localisation complexities when transferring numeric and bool types.

**Important Notes:**

- **Integer** values should be transferred as little endian byte sequences.
- **Floating point** values should be transferred using the 32-bit single-precision and 64-bit double-precision IEC 60559 formats for Single and Double values respectively.
- **Boolean** values should be transferred using integer 0 for `FALSE` and a non-zero value to represent `TRUE`.
- **String** values should be UTF16 encoded without a null terminator.

These requirements are met by the Microsoft C++ and .NET languages. For other languages, please consult your language implementation documentation.

---

## Rate

**Description:** Describes a range of rates supported by the `Telescope.MoveAxis()` method (degrees per second). These are contained within the `Telescope.AxisRates` collection and serve to describe one or more supported ranges of rates of motion about a mechanical axis.

It is possible that the Maximum and Minimum properties will be equal. In this case, the `Rate` object expresses a single discrete rate. Both the `Minimum` and `Maximum` properties are always expressed in units of degrees per second.

### Properties

#### Minimum

**Type:** `float`

**Description:** The minimum rate (degrees per second).

**Exceptions:**

- `InvalidValueException` - If an invalid Axis is specified.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.

#### Maximum

**Type:** `float`

**Description:** The maximum rate (degrees per second).

**Exceptions:**

- `InvalidValueException` - If an invalid Axis is specified.
- `NotConnectedException` - If the device is not connected.
- `DriverException` - An error occurred that is not described by one of the more specific ASCOM exceptions.
