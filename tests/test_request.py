"""Tests for request validators in python_alpaca_server.request."""

import pytest
from fastapi import HTTPException

from python_alpaca_server.request import (
    _lenient_int_validator,
    _strict_bool_validator,
    _strict_float_validator,
    _strict_int_validator,
)


class TestLenientIntValidator:
    """Tests for _lenient_int_validator."""

    def test_valid_int(self):
        """Valid integers are returned as-is."""
        assert _lenient_int_validator(42) == 42
        assert _lenient_int_validator(-10) == -10
        assert _lenient_int_validator(0) == 0

    def test_string_int(self):
        """Strings that represent integers are converted."""
        assert _lenient_int_validator("42") == 42
        assert _lenient_int_validator("-10") == -10
        assert _lenient_int_validator("0") == 0

    def test_none_returns_zero(self):
        """None returns 0."""
        assert _lenient_int_validator(None) == 0

    def test_invalid_string_returns_zero(self):
        """Invalid strings return 0 instead of raising."""
        assert _lenient_int_validator("not a number") == 0
        assert _lenient_int_validator("") == 0
        assert _lenient_int_validator("12.5") == 0

    def test_float_truncated(self):
        """Floats are truncated to int."""
        assert _lenient_int_validator(12.9) == 12
        assert _lenient_int_validator(-3.7) == -3


class TestStrictIntValidator:
    """Tests for _strict_int_validator."""

    def test_valid_int(self):
        """Valid integers are returned as-is."""
        assert _strict_int_validator(42) == 42
        assert _strict_int_validator(-10) == -10
        assert _strict_int_validator(0) == 0

    def test_string_int(self):
        """Strings that represent integers are converted."""
        assert _strict_int_validator("42") == 42
        assert _strict_int_validator("-10") == -10
        assert _strict_int_validator("0") == 0

    def test_none_raises_http_exception(self):
        """None raises HTTPException with 400 status."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_int_validator(None)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid integer value"

    def test_invalid_string_raises_http_exception(self):
        """Invalid strings raise HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_int_validator("not a number")
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid integer value"

    def test_empty_string_raises_http_exception(self):
        """Empty string raises HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_int_validator("")
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid integer value"

    def test_float_string_raises_http_exception(self):
        """Float strings raise HTTPException (can't convert to int)."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_int_validator("12.5")
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid integer value"

    def test_float_truncated(self):
        """Float values are truncated to int."""
        assert _strict_int_validator(12.9) == 12
        assert _strict_int_validator(-3.7) == -3


class TestStrictBoolValidator:
    """Tests for _strict_bool_validator."""

    def test_true_string_lowercase(self):
        """String 'true' returns True."""
        assert _strict_bool_validator("true") is True

    def test_true_string_uppercase(self):
        """String 'TRUE' returns True (case insensitive)."""
        assert _strict_bool_validator("TRUE") is True

    def test_true_string_mixed_case(self):
        """String 'True' returns True (case insensitive)."""
        assert _strict_bool_validator("True") is True
        assert _strict_bool_validator("TrUe") is True

    def test_false_string_lowercase(self):
        """String 'false' returns False."""
        assert _strict_bool_validator("false") is False

    def test_false_string_uppercase(self):
        """String 'FALSE' returns False (case insensitive)."""
        assert _strict_bool_validator("FALSE") is False

    def test_false_string_mixed_case(self):
        """String 'False' returns False (case insensitive)."""
        assert _strict_bool_validator("False") is False
        assert _strict_bool_validator("FaLsE") is False

    def test_string_one(self):
        """String '1' returns True."""
        assert _strict_bool_validator("1") is True

    def test_string_zero(self):
        """String '0' returns False."""
        assert _strict_bool_validator("0") is False

    def test_int_one(self):
        """Integer 1 returns True."""
        assert _strict_bool_validator(1) is True

    def test_int_zero(self):
        """Integer 0 returns False."""
        assert _strict_bool_validator(0) is False

    def test_bool_true(self):
        """Boolean True returns True."""
        assert _strict_bool_validator(True) is True

    def test_bool_false(self):
        """Boolean False returns False."""
        assert _strict_bool_validator(False) is False

    def test_none_raises_http_exception(self):
        """None raises HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_bool_validator(None)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid boolean value"

    def test_invalid_string_raises_http_exception(self):
        """Invalid strings raise HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_bool_validator("yes")
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid boolean value"

    def test_other_int_raises_http_exception(self):
        """Integers other than 0 and 1 raise HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_bool_validator(2)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid boolean value"

        with pytest.raises(HTTPException) as exc_info:
            _strict_bool_validator(-1)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid boolean value"


class TestStrictFloatValidator:
    """Tests for _strict_float_validator."""

    def test_valid_float(self):
        """Valid floats are returned as-is."""
        assert _strict_float_validator(3.14) == 3.14
        assert _strict_float_validator(-2.5) == -2.5
        assert _strict_float_validator(0.0) == 0.0

    def test_valid_int(self):
        """Integers are converted to float."""
        assert _strict_float_validator(42) == 42.0
        assert _strict_float_validator(-10) == -10.0
        assert _strict_float_validator(0) == 0.0

    def test_string_float(self):
        """Strings that represent floats are converted."""
        assert _strict_float_validator("3.14") == 3.14
        assert _strict_float_validator("-2.5") == -2.5
        assert _strict_float_validator("0.0") == 0.0

    def test_string_int(self):
        """Strings that represent integers are converted to float."""
        assert _strict_float_validator("42") == 42.0
        assert _strict_float_validator("-10") == -10.0

    def test_none_raises_http_exception(self):
        """None raises HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_float_validator(None)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid float value"

    def test_invalid_string_raises_http_exception(self):
        """Invalid strings raise HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_float_validator("not a number")
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid float value"

    def test_empty_string_raises_http_exception(self):
        """Empty string raises HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            _strict_float_validator("")
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid float value"

    def test_scientific_notation(self):
        """Scientific notation strings are converted."""
        assert _strict_float_validator("1e10") == 1e10
        assert _strict_float_validator("1.5e-3") == 1.5e-3
