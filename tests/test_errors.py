"""Tests for error classes in python_alpaca_server.errors."""

import pytest

from python_alpaca_server.errors import (
    ActionNotImplemented,
    AlpacaError,
    InvalidOperationError,
    InvalidValueError,
    InvalidWhileParkedError,
    InvalidWhileSlavedError,
    NotConnectedError,
    NotImplementedError,
    ValueNotSetError,
)
from python_alpaca_server.request import CommonRequest


@pytest.fixture
def mock_request():
    """Create a mock request with known transaction IDs."""
    return CommonRequest(
        ClientTransactionID=123,
        ClientID=456,
    )


class TestAlpacaError:
    """Tests for the base AlpacaError class."""

    def test_error_attributes(self, mock_request):
        """AlpacaError stores all attributes correctly."""
        error = AlpacaError(
            error_number=0x500,
            error_message="test error",
            client_transaction_id=mock_request.ClientTransactionID,
            client_id=mock_request.ClientID,
            server_transaction_id=mock_request.ServerTransactionID,
        )

        assert error.error_number == 0x500
        assert error.error_message == "test error"
        assert error.client_transaction_id == 123
        assert error.client_id == 456
        assert error.server_transaction_id == mock_request.ServerTransactionID

    def test_exception_message(self, mock_request):
        """AlpacaError formats exception message correctly."""
        error = AlpacaError(
            error_number=0x500,
            error_message="test error",
            client_transaction_id=mock_request.ClientTransactionID,
            client_id=mock_request.ClientID,
            server_transaction_id=mock_request.ServerTransactionID,
        )

        assert str(error) == "1280 - test error"  # 0x500 = 1280

    def test_is_exception(self, mock_request):
        """AlpacaError is a proper exception."""
        error = AlpacaError(
            error_number=0x500,
            error_message="test error",
            client_transaction_id=mock_request.ClientTransactionID,
            client_id=mock_request.ClientID,
            server_transaction_id=mock_request.ServerTransactionID,
        )

        with pytest.raises(AlpacaError):
            raise error


class TestNotImplementedError:
    """Tests for NotImplementedError."""

    def test_error_number(self, mock_request):
        """NotImplementedError has error number 0x400."""
        error = NotImplementedError(mock_request)
        assert error.error_number == 0x400

    def test_error_message(self, mock_request):
        """NotImplementedError has correct message."""
        error = NotImplementedError(mock_request)
        assert error.error_message == "not implemented"

    def test_transaction_ids_propagated(self, mock_request):
        """Transaction IDs are propagated from request."""
        error = NotImplementedError(mock_request)
        assert error.client_transaction_id == 123
        assert error.client_id == 456
        assert error.server_transaction_id == mock_request.ServerTransactionID


class TestInvalidValueError:
    """Tests for InvalidValueError."""

    def test_error_number(self, mock_request):
        """InvalidValueError has error number 0x401."""
        error = InvalidValueError(mock_request)
        assert error.error_number == 0x401

    def test_error_message(self, mock_request):
        """InvalidValueError has correct message."""
        error = InvalidValueError(mock_request)
        # Note: there's a typo in the source - "invlaid" instead of "invalid"
        assert error.error_message == "invlaid value"

    def test_transaction_ids_propagated(self, mock_request):
        """Transaction IDs are propagated from request."""
        error = InvalidValueError(mock_request)
        assert error.client_transaction_id == 123
        assert error.client_id == 456
        assert error.server_transaction_id == mock_request.ServerTransactionID


class TestValueNotSetError:
    """Tests for ValueNotSetError."""

    def test_error_number(self, mock_request):
        """ValueNotSetError has error number 0x402."""
        error = ValueNotSetError(mock_request)
        assert error.error_number == 0x402

    def test_error_message(self, mock_request):
        """ValueNotSetError has correct message."""
        error = ValueNotSetError(mock_request)
        assert error.error_message == "value not set"

    def test_transaction_ids_propagated(self, mock_request):
        """Transaction IDs are propagated from request."""
        error = ValueNotSetError(mock_request)
        assert error.client_transaction_id == 123
        assert error.client_id == 456
        assert error.server_transaction_id == mock_request.ServerTransactionID


class TestNotConnectedError:
    """Tests for NotConnectedError."""

    def test_error_number(self, mock_request):
        """NotConnectedError has error number 0x407."""
        error = NotConnectedError(mock_request)
        assert error.error_number == 0x407

    def test_error_message(self, mock_request):
        """NotConnectedError has correct message."""
        error = NotConnectedError(mock_request)
        assert error.error_message == "not connected"

    def test_transaction_ids_propagated(self, mock_request):
        """Transaction IDs are propagated from request."""
        error = NotConnectedError(mock_request)
        assert error.client_transaction_id == 123
        assert error.client_id == 456
        assert error.server_transaction_id == mock_request.ServerTransactionID


class TestInvalidWhileParkedError:
    """Tests for InvalidWhileParkedError."""

    def test_error_number(self, mock_request):
        """InvalidWhileParkedError has error number 0x408."""
        error = InvalidWhileParkedError(mock_request)
        assert error.error_number == 0x408

    def test_error_message(self, mock_request):
        """InvalidWhileParkedError has correct message."""
        error = InvalidWhileParkedError(mock_request)
        assert error.error_message == "invalid while parked"

    def test_transaction_ids_propagated(self, mock_request):
        """Transaction IDs are propagated from request."""
        error = InvalidWhileParkedError(mock_request)
        assert error.client_transaction_id == 123
        assert error.client_id == 456
        assert error.server_transaction_id == mock_request.ServerTransactionID


class TestInvalidWhileSlavedError:
    """Tests for InvalidWhileSlavedError."""

    def test_error_number(self, mock_request):
        """InvalidWhileSlavedError has error number 0x409."""
        error = InvalidWhileSlavedError(mock_request)
        assert error.error_number == 0x409

    def test_error_message(self, mock_request):
        """InvalidWhileSlavedError has correct message."""
        error = InvalidWhileSlavedError(mock_request)
        assert error.error_message == "invalid while slaved"

    def test_transaction_ids_propagated(self, mock_request):
        """Transaction IDs are propagated from request."""
        error = InvalidWhileSlavedError(mock_request)
        assert error.client_transaction_id == 123
        assert error.client_id == 456
        assert error.server_transaction_id == mock_request.ServerTransactionID


class TestInvalidOperationError:
    """Tests for InvalidOperationError."""

    def test_error_number(self, mock_request):
        """InvalidOperationError has error number 0x40B."""
        error = InvalidOperationError(mock_request)
        assert error.error_number == 0x40B

    def test_error_message(self, mock_request):
        """InvalidOperationError has correct message."""
        error = InvalidOperationError(mock_request)
        assert error.error_message == "invalid operation"

    def test_transaction_ids_propagated(self, mock_request):
        """Transaction IDs are propagated from request."""
        error = InvalidOperationError(mock_request)
        assert error.client_transaction_id == 123
        assert error.client_id == 456
        assert error.server_transaction_id == mock_request.ServerTransactionID


class TestActionNotImplemented:
    """Tests for ActionNotImplemented."""

    def test_error_number(self, mock_request):
        """ActionNotImplemented has error number 0x40C."""
        error = ActionNotImplemented(mock_request)
        assert error.error_number == 0x40C

    def test_error_message(self, mock_request):
        """ActionNotImplemented has correct message."""
        error = ActionNotImplemented(mock_request)
        assert error.error_message == "action not implemented"

    def test_transaction_ids_propagated(self, mock_request):
        """Transaction IDs are propagated from request."""
        error = ActionNotImplemented(mock_request)
        assert error.client_transaction_id == 123
        assert error.client_id == 456
        assert error.server_transaction_id == mock_request.ServerTransactionID


class TestErrorNumbersAreCorrect:
    """Verify all error numbers match the ASCOM Alpaca specification."""

    def test_all_error_numbers(self, mock_request):
        """All errors have the correct error numbers per spec."""
        error_map = {
            NotImplementedError: 0x400,
            InvalidValueError: 0x401,
            ValueNotSetError: 0x402,
            NotConnectedError: 0x407,
            InvalidWhileParkedError: 0x408,
            InvalidWhileSlavedError: 0x409,
            InvalidOperationError: 0x40B,
            ActionNotImplemented: 0x40C,
        }

        for error_class, expected_number in error_map.items():
            error = error_class(mock_request)
            assert error.error_number == expected_number, (
                f"{error_class.__name__} has error number {error.error_number}, "
                f"expected {expected_number}"
            )
