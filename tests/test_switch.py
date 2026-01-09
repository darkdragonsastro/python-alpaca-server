"""Tests for Switch device switchstep property."""

import pytest
from fastapi.testclient import TestClient

from python_alpaca_server.app import AlpacaServer
from python_alpaca_server.api.management import Description
from python_alpaca_server.devices.switch import Switch
from python_alpaca_server.request import (
    CommonRequest,
    IdRequest,
    PutIdNameRequest,
    PutIdStateRequest,
    PutIdValueRequest,
)


def _server_description() -> Description:
    """Create a test server description."""
    return Description(
        ServerName="Test Server",
        Manufacturer="Test",
        ManufacturerVersion="1.0.0",
        Location="Test Location",
    )


class MockSwitch(Switch):
    """Minimal Switch implementation for testing."""

    def __init__(self):
        super().__init__("test-switch")
        self._step_size = 0.1

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
        return "Test Switch"

    def get_driverinfo(self, req):
        return "Test Driver"

    def get_driverversion(self, req):
        return "1.0"

    def get_interfaceversion(self, req):
        return 1

    def get_name(self, req):
        return "Test Switch"

    def get_supportedactions(self, req):
        return []

    def get_maxswitch(self, req: CommonRequest) -> int:
        return 4

    def get_canwrite(self, req: IdRequest) -> bool:
        return True

    def get_getswitch(self, req: IdRequest) -> bool:
        return False

    def get_getswitchdescription(self, req: IdRequest) -> str:
        return f"Switch {req.Id}"

    def get_getswitchname(self, req: IdRequest) -> str:
        return f"Switch {req.Id}"

    def get_getswitchvalue(self, req: IdRequest) -> float:
        return 0.5

    def get_minswitchvalue(self, req: IdRequest) -> float:
        return 0.0

    def get_maxswitchvalue(self, req: IdRequest) -> float:
        return 1.0

    def get_switchstep(self, req: IdRequest) -> float:
        return self._step_size

    def put_setswitch(self, req: PutIdStateRequest) -> None:
        pass

    def put_setswitchname(self, req: PutIdNameRequest) -> None:
        pass

    def put_setswitchvalue(self, req: PutIdValueRequest) -> None:
        pass


class TestSwitchStepProperty:
    """Tests for the switchstep property on Switch devices."""

    def test_switchstep_route_registered(self):
        """The switchstep route is registered when a Switch device is present."""
        server = AlpacaServer(_server_description(), [MockSwitch()])
        app = server.create_app(5555)

        routes = [route.path for route in app.routes]

        assert "/api/v1/switch/{device_number}/switchstep" in routes

    def test_switchstep_endpoint_returns_value(self):
        """The switchstep endpoint returns the correct step value."""
        server = AlpacaServer(_server_description(), [MockSwitch()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/v1/switch/0/switchstep?Id=0")

        assert response.status_code == 200
        data = response.json()
        assert "Value" in data
        assert data["Value"] == 0.1

    def test_switchstep_endpoint_requires_id_parameter(self):
        """The switchstep endpoint requires an Id parameter."""
        server = AlpacaServer(_server_description(), [MockSwitch()])
        app = server.create_app(5555)
        client = TestClient(app, raise_server_exceptions=False)

        response = client.get("/api/v1/switch/0/switchstep")

        # Without Id, should get a validation error
        assert response.status_code == 422
