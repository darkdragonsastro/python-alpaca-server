"""Tests for Platform 7 common endpoints (connect, disconnect, connecting, devicestate)."""

from typing import List

import pytest
from fastapi.testclient import TestClient

from python_alpaca_server.app import AlpacaServer
from python_alpaca_server.api.management import Description
from python_alpaca_server.device import StateValue
from python_alpaca_server.devices.safetymonitor import SafetyMonitor
from python_alpaca_server.request import CommonRequest


def _server_description() -> Description:
    """Create a test server description."""
    return Description(
        ServerName="Test Server",
        Manufacturer="Test",
        ManufacturerVersion="1.0.0",
        Location="Test Location",
    )


class MockSafetyMonitor(SafetyMonitor):
    """Minimal SafetyMonitor implementation for testing Platform 7 endpoints."""

    def __init__(self):
        super().__init__("test-safety-monitor")
        self._connected = False
        self._connecting = False

    def put_action(self, req):
        return ""

    def put_command_blind(self, req):
        pass

    def put_command_bool(self, req):
        return False

    def put_command_string(self, req):
        return ""

    def get_connected(self, req):
        return self._connected

    def put_connected(self, req):
        self._connected = req.Connected

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

    # Platform 7 methods
    def put_connect(self, req: CommonRequest) -> None:
        self._connecting = True
        self._connected = True
        self._connecting = False

    def put_disconnect(self, req: CommonRequest) -> None:
        self._connecting = True
        self._connected = False
        self._connecting = False

    def get_connecting(self, req: CommonRequest) -> bool:
        return self._connecting

    def get_devicestate(self, req: CommonRequest) -> List[StateValue]:
        return [
            StateValue(Name="IsSafe", Value=True),
            StateValue(Name="TimeStamp", Value="2024-01-01T00:00:00Z"),
        ]


class TestPlatform7Routes:
    """Tests for Platform 7 route registration."""

    def test_connect_route_registered(self):
        """PUT connect route is registered for all device types."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)

        routes = [route.path for route in app.routes]

        assert "/api/v1/{device_type}/{device_number}/connect" in routes

    def test_disconnect_route_registered(self):
        """PUT disconnect route is registered for all device types."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)

        routes = [route.path for route in app.routes]

        assert "/api/v1/{device_type}/{device_number}/disconnect" in routes

    def test_connecting_route_registered(self):
        """GET connecting route is registered for all device types."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)

        routes = [route.path for route in app.routes]

        assert "/api/v1/{device_type}/{device_number}/connecting" in routes

    def test_devicestate_route_registered(self):
        """GET devicestate route is registered for all device types."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)

        routes = [route.path for route in app.routes]

        assert "/api/v1/{device_type}/{device_number}/devicestate" in routes


class TestConnectEndpoint:
    """Tests for the PUT connect endpoint."""

    def test_connect_endpoint_accessible(self):
        """PUT connect endpoint is accessible and returns success."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.put("/api/v1/safetymonitor/0/connect", data={})

        assert response.status_code == 200
        data = response.json()
        # ErrorNumber should be excluded when None (no error)
        assert "ErrorNumber" not in data or data["ErrorNumber"] == 0

    def test_connect_initiates_connection(self):
        """PUT connect initiates device connection."""
        mock_device = MockSafetyMonitor()
        server = AlpacaServer(_server_description(), [mock_device])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        # Device should start disconnected
        assert mock_device._connected is False

        response = client.put("/api/v1/safetymonitor/0/connect", data={})

        assert response.status_code == 200
        # After connect, device should be connected
        assert mock_device._connected is True


class TestDisconnectEndpoint:
    """Tests for the PUT disconnect endpoint."""

    def test_disconnect_endpoint_accessible(self):
        """PUT disconnect endpoint is accessible and returns success."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.put("/api/v1/safetymonitor/0/disconnect", data={})

        assert response.status_code == 200
        data = response.json()
        assert "ErrorNumber" not in data or data["ErrorNumber"] == 0

    def test_disconnect_terminates_connection(self):
        """PUT disconnect terminates device connection."""
        mock_device = MockSafetyMonitor()
        mock_device._connected = True
        server = AlpacaServer(_server_description(), [mock_device])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        # Device should start connected
        assert mock_device._connected is True

        response = client.put("/api/v1/safetymonitor/0/disconnect", data={})

        assert response.status_code == 200
        # After disconnect, device should be disconnected
        assert mock_device._connected is False


class TestConnectingEndpoint:
    """Tests for the GET connecting endpoint."""

    def test_connecting_endpoint_accessible(self):
        """GET connecting endpoint is accessible and returns boolean."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/v1/safetymonitor/0/connecting")

        assert response.status_code == 200
        data = response.json()
        assert "Value" in data
        assert isinstance(data["Value"], bool)

    def test_connecting_returns_false_when_idle(self):
        """GET connecting returns False when no async operation is active."""
        mock_device = MockSafetyMonitor()
        server = AlpacaServer(_server_description(), [mock_device])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/v1/safetymonitor/0/connecting")

        assert response.status_code == 200
        data = response.json()
        assert data["Value"] is False


class TestDeviceStateEndpoint:
    """Tests for the GET devicestate endpoint."""

    def test_devicestate_endpoint_accessible(self):
        """GET devicestate endpoint is accessible and returns list."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/v1/safetymonitor/0/devicestate")

        assert response.status_code == 200
        data = response.json()
        assert "Value" in data
        assert isinstance(data["Value"], list)

    def test_devicestate_returns_state_values(self):
        """GET devicestate returns StateValue objects with Name and Value."""
        server = AlpacaServer(_server_description(), [MockSafetyMonitor()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/v1/safetymonitor/0/devicestate")

        assert response.status_code == 200
        data = response.json()
        state_values = data["Value"]
        assert len(state_values) == 2

        # Check that state values have correct structure
        names = [sv["Name"] for sv in state_values]
        assert "IsSafe" in names
        assert "TimeStamp" in names

        # Check IsSafe value
        is_safe = next(sv for sv in state_values if sv["Name"] == "IsSafe")
        assert is_safe["Value"] is True


class TestStateValueModel:
    """Tests for the StateValue model."""

    def test_statevalue_creation(self):
        """StateValue can be created with Name and Value."""
        sv = StateValue(Name="TestProp", Value=42)
        assert sv.Name == "TestProp"
        assert sv.Value == 42

    def test_statevalue_accepts_various_value_types(self):
        """StateValue accepts various types for Value field."""
        # String value
        sv_str = StateValue(Name="StringProp", Value="hello")
        assert sv_str.Value == "hello"

        # Boolean value
        sv_bool = StateValue(Name="BoolProp", Value=True)
        assert sv_bool.Value is True

        # Float value
        sv_float = StateValue(Name="FloatProp", Value=3.14)
        assert sv_float.Value == 3.14

        # List value
        sv_list = StateValue(Name="ListProp", Value=[1, 2, 3])
        assert sv_list.Value == [1, 2, 3]
