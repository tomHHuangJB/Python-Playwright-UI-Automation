from __future__ import annotations

import pytest

from assertions.api_assertions import (
    assert_integer,
    assert_mapping,
    assert_non_empty_string,
    assert_required_keys,
    assert_sequence,
)


@pytest.mark.data_validation
def test_table_filter_and_sort_invariants_hold_for_active_rows(api_client) -> None:
    payload = api_client.get_json(
        "/api/table",
        params={"status": "Active", "sort": "id", "order": "desc"},
    )

    assert_required_keys(payload, ("items", "total"))
    assert_sequence(payload["items"], "items")
    assert payload["total"] == 6
    assert len(payload["items"]) == 6

    ids: list[int] = []
    for index, item in enumerate(payload["items"]):
        assert_mapping(item, f"items[{index}]")
        assert_required_keys(item, ("id", "name", "status"))
        assert_integer(item["id"], f"items[{index}].id")
        assert_non_empty_string(item["name"], f"items[{index}].name")
        assert item["status"] == "Active"
        ids.append(item["id"])

    assert ids == sorted(ids, reverse=True)


@pytest.mark.data_validation
def test_roles_permissions_and_consistency_payloads_are_well_formed(api_client) -> None:
    roles_payload = api_client.get_json("/api/roles")
    assert_required_keys(roles_payload, ("roles", "permissions"))
    assert_sequence(roles_payload["roles"], "roles")
    assert roles_payload["roles"] == ["viewer", "editor", "admin"]
    assert_mapping(roles_payload["permissions"], "permissions")
    assert roles_payload["permissions"]["admin"] == ["all"]
    assert roles_payload["permissions"]["viewer"] == ["read"]

    permissions_payload = api_client.get_json("/api/permissions")
    assert_required_keys(permissions_payload, ("geo", "notifications", "clipboard"))
    assert permissions_payload["geo"] in {"prompt", "granted", "denied"}
    assert permissions_payload["notifications"] in {"prompt", "granted", "denied"}
    assert permissions_payload["clipboard"] in {"prompt", "granted", "denied"}

    consistency_payload = api_client.get_json("/api/consistency")
    assert_required_keys(consistency_payload, ("status", "visibleAfterMs"))
    assert consistency_payload["status"] == "eventual"
    assert_integer(consistency_payload["visibleAfterMs"], "visibleAfterMs")
    assert consistency_payload["visibleAfterMs"] > 0
