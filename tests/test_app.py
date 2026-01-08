"""Tests for conditional router registration in AlpacaServer."""

from typing import List

import pytest
from fastapi.testclient import TestClient

from python_alpaca_server.app import AlpacaServer
from python_alpaca_server.api.management import Description
from python_alpaca_server.device import DeviceType
from python_alpaca_server.devices.safetymonitor import SafetyMonitor
from python_alpaca_server.devices.observingconditions import ObservingConditions
from python_alpaca_server.devices.focuser import Focuser
from python_alpaca_server.devices.dome import Dome
from python_alpaca_server.devices.filterwheel import FilterWheel
from python_alpaca_server.devices.rotator import Rotator
from python_alpaca_server.devices.covercalibrator import CoverCalibrator
from python_alpaca_server.devices.switch import Switch
from python_alpaca_server.request import CommonRequest


def _server_description() -> Description:
    """Create a test server description."""
    return Description(
        ServerName="Test Server",
        Manufacturer="Test",
        ManufacturerVersion="1.0.0",
        Location="Test Location",
    )


# Minimal concrete implementations for testing


class MockSafetyMonitor(SafetyMonitor):
    """Minimal SafetyMonitor implementation for testing."""

    def __init__(self):
        super().__init__("test-safety-monitor")

    def put_action(self, req):
        return ""

    def put_command_blind(self, req):
        pass

    def put_command_bool(self, req):
        return False

    def put_command_string(self, req):
        return ""

    def get_connected(self, req):
        return True

    def put_connected(self, req):
        pass

    def get_description(self, req):
        return "Test SafetyMonitor"

    def get_driverinfo(self, req):
        return "Test Driver"

    def get_driverversion(self, req):
        return "1.0"

    def get_interfaceversion(self, req):
        return 1

    def get_name(self, req):
        return "Test SafetyMonitor"

    def get_supportedactions(self, req):
        return []

    def get_issafe(self, req):
        return True


class MockObservingConditions(ObservingConditions):
    """Minimal ObservingConditions implementation for testing."""

    def __init__(self):
        super().__init__("test-observing-conditions")

    def put_action(self, req):
        return ""

    def put_command_blind(self, req):
        pass

    def put_command_bool(self, req):
        return False

    def put_command_string(self, req):
        return ""

    def get_connected(self, req):
        return True

    def put_connected(self, req):
        pass

    def get_description(self, req):
        return "Test ObservingConditions"

    def get_driverinfo(self, req):
        return "Test Driver"

    def get_driverversion(self, req):
        return "1.0"

    def get_interfaceversion(self, req):
        return 1

    def get_name(self, req):
        return "Test ObservingConditions"

    def get_supportedactions(self, req):
        return []

    def get_averageperiod(self, req):
        return 0.0

    def put_averageperiod(self, req):
        pass

    def get_cloudcover(self, req):
        return 0.0

    def get_dewpoint(self, req):
        return 0.0

    def get_humidity(self, req):
        return 50.0

    def get_pressure(self, req):
        return 1013.25

    def get_rainrate(self, req):
        return 0.0

    def get_skybrightness(self, req):
        return 0.0

    def get_skyquality(self, req):
        return 0.0

    def get_skytemperature(self, req):
        return 0.0

    def get_starfwhm(self, req):
        return 0.0

    def get_temperature(self, req):
        return 20.0

    def get_winddirection(self, req):
        return 0.0

    def get_windgust(self, req):
        return 0.0

    def get_windspeed(self, req):
        return 0.0

    def put_refresh(self, req):
        pass

    def get_sensordescription(self, req):
        return "Test Sensor"

    def get_timesincelastupdate(self, req):
        return 0.0


class MockFocuser(Focuser):
    """Minimal Focuser implementation for testing."""

    def __init__(self):
        super().__init__("test-focuser")

    def put_action(self, req):
        return ""

    def put_command_blind(self, req):
        pass

    def put_command_bool(self, req):
        return False

    def put_command_string(self, req):
        return ""

    def get_connected(self, req):
        return True

    def put_connected(self, req):
        pass

    def get_description(self, req):
        return "Test Focuser"

    def get_driverinfo(self, req):
        return "Test Driver"

    def get_driverversion(self, req):
        return "1.0"

    def get_interfaceversion(self, req):
        return 1

    def get_name(self, req):
        return "Test Focuser"

    def get_supportedactions(self, req):
        return []

    def get_absolute(self, req):
        return True

    def get_ismoving(self, req):
        return False

    def get_maxincrement(self, req):
        return 10000

    def get_maxstep(self, req):
        return 50000

    def get_position(self, req):
        return 25000

    def get_stepsize(self, req):
        return 1

    def get_tempcomp(self, req):
        return False

    def put_tempcomp(self, req):
        pass

    def get_tempcompavailable(self, req):
        return False

    def get_temperature(self, req):
        return 20.0

    def put_halt(self, req):
        pass

    def put_move(self, req):
        pass


def _get_route_paths(app) -> List[str]:
    """Extract all route paths from a FastAPI app."""
    return [route.path for route in app.routes]


class TestConditionalRouterRegistration:
    """Tests for conditional router registration based on device types present."""

    def test_safetymonitor_routes_registered_when_device_present(self):
        """SafetyMonitor routes are registered when a SafetyMonitor device is present."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)

        routes = _get_route_paths(app)

        assert "/api/v1/safetymonitor/{device_number}/issafe" in routes

    def test_safetymonitor_routes_not_registered_when_device_absent(self):
        """SafetyMonitor routes are NOT registered when no SafetyMonitor device is present."""
        server = AlpacaServer(_server_description(), [MockObservingConditions()])
        app = server.create_app(5555)

        routes = _get_route_paths(app)

        assert "/api/v1/safetymonitor/{device_number}/issafe" not in routes

    def test_observingconditions_routes_registered_when_device_present(self):
        """ObservingConditions routes are registered when an ObservingConditions device is present."""
        server = AlpacaServer(_server_description(), [MockObservingConditions()])
        app = server.create_app(5555)

        routes = _get_route_paths(app)

        # Check for a few key ObservingConditions routes
        assert "/api/v1/observingconditions/{device_number}/temperature" in routes
        assert "/api/v1/observingconditions/{device_number}/humidity" in routes
        assert "/api/v1/observingconditions/{device_number}/pressure" in routes

    def test_observingconditions_routes_not_registered_when_device_absent(self):
        """ObservingConditions routes are NOT registered when no ObservingConditions device is present."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)

        routes = _get_route_paths(app)

        assert "/api/v1/observingconditions/{device_number}/temperature" not in routes
        assert "/api/v1/observingconditions/{device_number}/humidity" not in routes

    def test_focuser_routes_registered_when_device_present(self):
        """Focuser routes are registered when a Focuser device is present."""
        server = AlpacaServer(_server_description(), [MockFocuser()])
        app = server.create_app(5555)

        routes = _get_route_paths(app)

        assert "/api/v1/focuser/{device_number}/position" in routes
        assert "/api/v1/focuser/{device_number}/ismoving" in routes

    def test_focuser_routes_not_registered_when_device_absent(self):
        """Focuser routes are NOT registered when no Focuser device is present."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)

        routes = _get_route_paths(app)

        assert "/api/v1/focuser/{device_number}/position" not in routes
        assert "/api/v1/focuser/{device_number}/ismoving" not in routes

    def test_multiple_device_types_all_routes_registered(self):
        """Routes for multiple device types are all registered when devices are present."""
        server = AlpacaServer(
            _server_description(),
            [MockSafetyMonitor(), MockObservingConditions(), MockFocuser()],
        )
        app = server.create_app(5555)

        routes = _get_route_paths(app)

        # All three device types should have their routes
        assert "/api/v1/safetymonitor/{device_number}/issafe" in routes
        assert "/api/v1/observingconditions/{device_number}/temperature" in routes
        assert "/api/v1/focuser/{device_number}/position" in routes

    def test_common_routes_always_registered(self):
        """Common routes (like connected) are always registered regardless of device types."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)

        routes = _get_route_paths(app)

        # Common route that works for any device type
        assert "/api/v1/{device_type}/{device_number}/connected" in routes

    def test_management_routes_always_registered(self):
        """Management routes are always registered."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)

        routes = _get_route_paths(app)

        assert "/management/apiversions" in routes
        assert "/management/v1/description" in routes
        assert "/management/v1/configureddevices" in routes


class TestRouterRegistrationWithTestClient:
    """Integration tests using TestClient to verify routes work end-to-end."""

    def test_observingconditions_endpoint_accessible(self):
        """ObservingConditions endpoint is accessible via HTTP when device is present."""
        server = AlpacaServer(_server_description(), [MockObservingConditions()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/v1/observingconditions/0/temperature")

        assert response.status_code == 200
        data = response.json()
        assert "Value" in data
        assert data["Value"] == 20.0

    def test_observingconditions_endpoint_not_found_when_absent(self):
        """ObservingConditions endpoint returns 404 when no device is present."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/v1/observingconditions/0/temperature")

        # Route shouldn't exist at all, so 404
        assert response.status_code == 404

    def test_safetymonitor_endpoint_accessible(self):
        """SafetyMonitor endpoint is accessible via HTTP when device is present."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/v1/safetymonitor/0/issafe")

        assert response.status_code == 200
        data = response.json()
        assert "Value" in data
        assert data["Value"] is True
