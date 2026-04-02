from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.grpc_page import GrpcPage


@pytest.mark.regression
def test_grpc_command_generator_updates_for_scenario_auth_and_port(page) -> None:
    grpc_page = GrpcPage(page)

    grpc_page.open()
    grpc_page.expect_page_ready()

    expect(grpc_page.command).to_contain_text("grpcurl")
    expect(grpc_page.selected_auth).to_contain_text("public")

    grpc_page.select_scenario("admin-snapshot")
    expect(grpc_page.scenario_title).to_contain_text(
        "automation.admin.v1.AdminService/GetSystemSnapshot"
    )
    expect(grpc_page.required_auth).to_contain_text("admin")
    expect(grpc_page.selected_auth).to_contain_text("admin")
    expect(grpc_page.command).to_contain_text("x-api-key: test-admin-key")
    expect(grpc_page.expected_result).to_contain_text("Returns counts")

    grpc_page.set_grpc_port("51051")
    expect(grpc_page.command).to_contain_text("localhost:51051")
    expect(grpc_page.reflection_tip).to_contain_text("localhost:51051")

    grpc_page.select_auth_profile("service")
    expect(grpc_page.selected_auth).to_contain_text("service")
    expect(grpc_page.command).to_contain_text("x-user-role: service")
    expect(grpc_page.auth_table).to_contain_text("test-service-key")
