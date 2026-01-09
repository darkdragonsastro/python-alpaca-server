# ASCOM Platform 7 Release Notes

This document contains the official ASCOM Alpaca and COM application programming
interface (API) specifications as of the release of the ASCOM Platform 7 and the
corresponding Alpaca interfaces. Platform 7 represents a significant upgrade to
all of the interfaces, hence their `InterfaceVersion` properties have been
increased by 1.

## Non-Blocking (Asynchronous) Behavior - Documentation

Since Alpaca is a network protocol, it is important that methods be non-blocking
(asynchronous). Most of the Platform 6 interface methods are either explicitly
or implicitly asynchronous. In addition, these methods already have existing
properties which permit detecting their successful completion.

However the Platform 6 interface documentation did not make this explicitly
clear in many cases, and was simply incorrect in a few cases. This document
contains formalized and clarified documentation for those methods that are
already asynchronous including specifying the relevant completion properties.

## Non-Blocking (Asynchronous) Enhancement - Device Connections

A fundamental problem with all of the Platform 6 device interfaces is the use of
the synchronous `Connected` property to effect connection and disconnection.
Since a property cannot be made asynchronous, the upgraded interfaces now have
new `Connect()` and `Disconnect()` methods, which are asynchronous, and a new
`Connecting` property with which clients can detect completion of these
operations.

> **Attention:** These changes are non-breaking. However, writing to `Connected`
> to effect connection and disconnection is now explicitly deprecated for
> *clients* but must still be implemented by *drivers* to ensure backward
> compatibility with earlier software.

## Expanded Application - Camera.ReadoutMode

The description of `ReadoutMode` now includes a generalization that it is meant
to be used for any sort of mode the camera supports such as
manufacturer-recommended combinations of gain and offset, changes in sensor
size, etc. in addition to pixel data readout modes/speeds.

## Non-Blocking (Asynchronous) Enhancement - CoverCalibrator

The `CoverCalibrator V1` interface doesn't have separate properties to undertake
the state and status roles. Instead, it uses multi-purpose enum state/status
properties that combine these functions. Using this approach it is possible to
report an error state but it is not possible to return a message indicating the
nature of the issue.

To address this, pollable boolean completion properties have been added for
cover and calibrator operations that can return text error descriptions through
exceptions/errors when necessary:

- `CalibratorChanging` was added for `CalibratorOn()` and `CalibratorOff()`
- `CoverMoving` was added for `OpenCover()` and `CloseCover()`

## Non-Blocking (Asynchronous) Enhancement - Dome

`AbortSlew()` has been newly declared as asynchronous with `Slewing` as the
completion property.

## Non-Blocking (Asynchronous) Enhancement - Switch

Switch state changes are currently synchronous, which limits their application
to short duration activities. Two new asynchronous set methods have been added
to provide greater flexibility and enable switches to control long running
activities:

- `SetAsync()` - Asynchronous switch state change
- `SetAsyncValue()` - Asynchronous switch value change

These are optional, and clients may discover if the device has these
capabilities by testing the new `CanAsync` property. Completion detection is
provided by a new `StateChangeComplete` property. Finally an in-progress switch
state change may be cancelled via the new `CancelAsync()` method.

## Non-Blocking (Asynchronous) and Other Enhancements - Telescope

### Asynchronous Method Documentation

`FindHome()`, `Park()`, `MoveAxis()`, and `PulseGuide()` are specifically
documented as asynchronous correcting earlier errors and as a clarification.

### Slewing Requirements

If a mount can slew at all, it now must support both *synchronous* and
*asynchronous* slewing. This means:

- Both `CanSlew` and `CanSlewAsync` must have the same value
- Both `CanSlewAltAz` and `CanSlewAltAzAsync` must have the same value

> **Note:** Synchronous slewing has been deprecated for *clients* but must be
> implemented by *drivers* for backward compatibility.

### AbortSlew Enhancement

`AbortSlew()` has been newly declared as asynchronous with `Slewing` as the
completion property.

### Tracking Rate Validation

Attempts to set `RightAscensionRate` and/or `DeclinationRate` now require
raising `InvalidOperationException` if `TrackingRate` is not `driveSidereal`.

### New Exception Handling

- Several methods have been specified to throw a new `ParkedException` if they
  are not appropriate for a parked mount.
- Equatorial slewing methods must throw `InvalidOperationException` if
  `Tracking` is False or if the requested slew would fail due to exceeding a
  hardware limit of the mount.

## Enhancement - Aggregated Reading of Operational Properties

A new `DeviceState` property has been added to all device interfaces. This
property returns an aggregated collection of operational state values in a
single call, which is particularly useful for Alpaca network communications
where multiple individual property reads would result in significant latency.

The `DeviceState` property returns a list of `StateValue` objects, each
containing a name-value pair representing a device property. This allows clients
to efficiently retrieve multiple operational properties with a single network
round-trip.

---

*Source: [ASCOM Master Interfaces Documentation](https://ascom-standards.org/newdocs/relnotes.html)*

*Copyright 2023-2026, ASCOM Initiative, MIT License.*
