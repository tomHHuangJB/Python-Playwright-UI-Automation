from __future__ import annotations

import pytest

from assertions.api_assertions import (
    assert_boolean,
    assert_error_response,
    assert_integer,
    assert_mapping,
    assert_non_empty_string,
    assert_required_keys,
    assert_response_header,
    assert_sequence,
)


@pytest.mark.api
def test_data_crud_endpoints_and_validation_errors(api_client) -> None:
    list_response = api_client.get("/api/data")
    assert list_response.status_code == 200
    assert_response_header(list_response, "X-Correlation-ID")

    list_payload = list_response.json()
    assert_required_keys(list_payload, ("data", "delay"))
    assert_sequence(list_payload["data"], "data")
    assert list_payload["delay"] == 0
    for index, item in enumerate(list_payload["data"]):
        assert_mapping(item, f"data[{index}]")
        assert_required_keys(item, ("id", "name"))
        assert_integer(item["id"], f"data[{index}].id")
        assert_non_empty_string(item["name"], f"data[{index}].name")

    invalid_create_response = api_client.post("/api/data", payload={}, raise_for_status=False)
    assert invalid_create_response.status_code == 400
    assert_error_response(
        invalid_create_response.json(),
        code="VALIDATION",
        message_contains="Name required",
    )

    create_payload = api_client.post_json("/api/data", {"name": "Gamma", "status": "draft"})
    assert_required_keys(create_payload, ("id", "name", "status"))
    assert_integer(create_payload["id"], "id")
    assert create_payload["name"] == "Gamma"
    assert create_payload["status"] == "draft"

    update_payload = api_client.put_json("/api/data/7", {"name": "Gamma Updated"})
    assert_required_keys(update_payload, ("id", "name", "updated"))
    assert update_payload["id"] == "7"
    assert update_payload["name"] == "Gamma Updated"
    assert_boolean(update_payload["updated"], "updated")

    delete_payload = api_client.delete_json("/api/data/7")
    assert_required_keys(delete_payload, ("deleted",))
    assert_boolean(delete_payload["deleted"], "deleted")


@pytest.mark.api
def test_reset_seed_and_deterministic_failure_hooks_are_available(api_client) -> None:
    reset_payload = api_client.post_json("/api/reset")
    assert reset_payload == {"status": "reset"}

    seed_payload = api_client.post_json("/api/seed", {"seed": 12345})
    assert seed_payload == {"seed": 12345}

    failure_response = api_client.get(
        "/api/data",
        params={"seed": 7, "failProbability": 1},
        raise_for_status=False,
    )
    assert failure_response.status_code == 500
    assert_error_response(failure_response.json(), code="DETERMINISTIC_FAILURE")
