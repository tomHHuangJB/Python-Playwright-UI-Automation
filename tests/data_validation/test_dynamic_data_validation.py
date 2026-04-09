from __future__ import annotations

import pytest

from assertions.api_assertions import (
    assert_boolean,
    assert_integer,
    assert_iso_datetime,
    assert_mapping,
    assert_required_keys,
    assert_response_header,
    assert_sequence,
)


@pytest.mark.data_validation
def test_dedup_responses_preserve_payload_identity_for_a_reused_key(api_client) -> None:
    first_payload = api_client.get_json("/api/dedup", params={"key": "shared-key"})
    second_payload = api_client.get_json("/api/dedup", params={"key": "shared-key"})

    for payload in (first_payload, second_payload):
        assert_required_keys(payload, ("key", "deduped", "payload"))
        assert payload["key"] == "shared-key"
        assert_boolean(payload["deduped"], "deduped")
        assert_mapping(payload["payload"], "payload")
        assert_required_keys(payload["payload"], ("id", "message"))
        assert_integer(payload["payload"]["id"], "payload.id")

    assert first_payload["deduped"] is False
    assert second_payload["deduped"] is True
    assert_integer(second_payload["cachedAt"], "cachedAt")
    assert first_payload["payload"] == second_payload["payload"]


@pytest.mark.data_validation
def test_race_and_partial_payloads_match_expected_data_shapes(api_client) -> None:
    race_payload = api_client.get_json("/api/race", params={"label": "fast", "delay": 0})
    assert_required_keys(race_payload, ("label", "delay", "serverTime"))
    assert race_payload["label"] == "fast"
    assert race_payload["delay"] == 0
    assert_iso_datetime(race_payload["serverTime"], "serverTime")

    partial_response = api_client.get("/api/partial")
    assert partial_response.status_code == 206
    assert_response_header(partial_response, "Content-Range", "items 0-1/5")
    partial_payload = partial_response.json()
    assert_required_keys(partial_payload, ("items", "total"))
    assert_sequence(partial_payload["items"], "items")
    assert len(partial_payload["items"]) == 2
    assert partial_payload["total"] == 5
    for index, item in enumerate(partial_payload["items"]):
        assert_mapping(item, f"items[{index}]")
        assert_required_keys(item, ("id",))
        assert_integer(item["id"], f"items[{index}].id")
