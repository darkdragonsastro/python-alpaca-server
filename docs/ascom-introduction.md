# Introduction to ASCOM Master Interfaces

This is the master generic document for the ASCOM interfaces. The interface specifications are written using language and OS independent syntax. For more information see the [ASCOM Initiative web site](https://ascom-standards.org/index.htm) and the [ASCOM Implementation Neutral Interface Definitions](https://ascom-standards.org/Help/Platform/html/N_ASCOM_DeviceInterface.htm).

## Status of This Document (1.0.17 as of 06-Jan-2026)

This is an update to the first production release of this document. Camera image array shaping and encoding has been clarified. Rotator operation was clarified with diagrams. A requirement for internal wrap management has been added as a result of new rotators without this appearing and causing confusion and limitations. **No interface changes were made**. The clarifying FAQ articles represent the ASCOM Platform 7 specifications. A new FAQ "What do we mean by the terms Mandatory, Optional and Deprecated?" has been added. Datatype specifics have been included. Consider this a living document. Inevitably, corrections and requests for clarifications will be applied during its lifetime. Significant corrections will be logged here in the future.

## Data Types Used in This Document

Throughout the interface definitions, parameter and other numeric values are assigned generic datatypes `integer`, `float`, `list`, and `array`. Please see [ASCOM Implementation Neutral Interface Definitions](https://ascom-standards.org/Help/Platform/html/N_ASCOM_DeviceInterface.htm) for COM and [Alpaca API Reference](https://ascom-standards.org/api/) for Alpaca implementation specific detail.

In this document the scalar types `integer` and `float` are considered signed and do not imply restrictions on their permitted values. If there are value restrictions, they are either commonly understood (e.g., range of angles) or specifically mentioned in the value's documentation. The specifics of an interface in a particular language may differentiate between similar scalar type in that language such as 16-, 32-, or 64-bit signed or unsigned integers.

A `list` is a single string of comma-separated substrings. An `array` is an indexable and enumerable set of values. Array syntax and usage is language specific.

## Common Misconceptions and Confusions

Throughout the evolution of ASCOM, and particularly recently with Alpaca, the goal has been to provide a strong framework for reliability and integrity. There are a few subject areas within which misconceptions and confusion are common. Before starting a development project you may benefit from reviewing the following design principles that are *foundational*:

- [The General Principles](https://ascom-standards.org/AlpacaDeveloper/Principles.htm)
- [Asynchronous APIs](https://ascom-standards.org/AlpacaDeveloper/Async.htm)
- [Exceptions in ASCOM](https://ascom-standards.org/AlpacaDeveloper/Exceptions.htm)

---

*Source: [ASCOM Master Interfaces Documentation](https://ascom-standards.org/newdocs/introduction.html)*

*© ASCOM Initiative, MIT License*
