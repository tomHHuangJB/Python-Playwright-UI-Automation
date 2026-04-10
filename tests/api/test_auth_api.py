from __future__ import annotations

import pytest

from assertions.api_assertions import (
    assert_boolean,
    assert_error_response,
    assert_mapping,
    assert_non_empty_string,
    assert_required_keys,
    assert_response_header,
    assert_sequence,
)


@pytest.mark.api
def test_auth_endpoints_expose_expected_contracts(api_client) -> None:
    login_response = api_client.post(
        "/api/auth/login",
        payload={"username": "principal.engineer", "password": "demo"},
    )
    assert login_response.status_code == 200
    assert_response_header(login_response, "X-Correlation-ID")

    login_payload = login_response.json()
    assert_required_keys(login_payload, ("token", "refreshToken", "user"))
    assert_non_empty_string(login_payload["token"], "token")
    assert_non_empty_string(login_payload["refreshToken"], "refreshToken")
    assert login_payload["user"] == "principal.engineer"

    refresh_payload = api_client.post_json("/api/auth/refresh")
    assert_required_keys(refresh_payload, ("token", "refreshToken"))
    assert_non_empty_string(refresh_payload["token"], "token")
    assert_non_empty_string(refresh_payload["refreshToken"], "refreshToken")

    sessions_payload = api_client.get_json("/api/auth/sessions")
    assert_required_keys(sessions_payload, ("sessions",))
    assert_sequence(sessions_payload["sessions"], "sessions")
    first_session = sessions_payload["sessions"][0]
    assert_mapping(first_session, "sessions[0]")
    assert_required_keys(first_session, ("id", "user", "active"))
    assert_non_empty_string(first_session["id"], "sessions[0].id")
    assert_non_empty_string(first_session["user"], "sessions[0].user")
    assert_boolean(first_session["active"], "sessions[0].active")

    lockout_response = api_client.post("/api/auth/lockout", raise_for_status=False)
    assert lockout_response.status_code == 423
    assert_error_response(lockout_response.json(), code="LOCKED", message_contains="locked")
