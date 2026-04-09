from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

import requests


def assert_required_keys(payload: Mapping[str, Any], required_keys: Sequence[str]) -> None:
    missing = [key for key in required_keys if key not in payload]
    assert not missing, f"Missing required key(s): {', '.join(missing)} in payload {payload!r}"


def assert_non_empty_string(value: Any, field_name: str) -> None:
    assert isinstance(value, str), f"{field_name} must be a string, got {type(value).__name__}"
    assert value.strip(), f"{field_name} must not be empty"


def assert_boolean(value: Any, field_name: str) -> None:
    assert isinstance(value, bool), f"{field_name} must be a boolean, got {type(value).__name__}"


def assert_integer(value: Any, field_name: str) -> None:
    assert isinstance(value, int), f"{field_name} must be an integer, got {type(value).__name__}"


def assert_mapping(value: Any, field_name: str) -> None:
    assert isinstance(value, Mapping), f"{field_name} must be a mapping, got {type(value).__name__}"


def assert_sequence(value: Any, field_name: str) -> None:
    assert isinstance(value, Sequence) and not isinstance(
        value, (str, bytes)
    ), f"{field_name} must be a sequence"


def assert_iso_datetime(value: Any, field_name: str) -> None:
    assert_non_empty_string(value, field_name)
    datetime.fromisoformat(value.replace("Z", "+00:00"))


def assert_error_response(
    payload: Mapping[str, Any],
    *,
    code: str | None = None,
    message_contains: str | None = None,
) -> None:
    assert_required_keys(payload, ("error",))
    error = payload["error"]
    assert_mapping(error, "error")
    assert_required_keys(error, ("code", "message"))
    assert_non_empty_string(error["code"], "error.code")
    assert_non_empty_string(error["message"], "error.message")
    if code is not None:
        assert error["code"] == code
    if message_contains is not None:
        assert message_contains in str(error["message"])


def assert_response_header(
    response: requests.Response, header_name: str, expected_value: str | None = None
) -> str:
    value = response.headers.get(header_name)
    assert value is not None, f"Expected response header {header_name!r} to be present"
    if expected_value is not None:
        assert value == expected_value
    return value
