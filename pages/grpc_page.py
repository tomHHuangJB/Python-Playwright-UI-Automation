from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class GrpcPage(BasePage):
    PATH = "/grpc"
    ROUTE_NAME = "grpc"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def scenario_select(self):
        return self.by_test_id("grpc-scenario-select")

    @property
    def auth_select(self):
        return self.by_test_id("grpc-auth-select")

    @property
    def port_input(self):
        return self.by_test_id("grpc-port-input")

    @property
    def scenario_card(self):
        return self.by_test_id("grpc-scenario-card")

    @property
    def scenario_title(self):
        return self.by_test_id("grpc-scenario-title")

    @property
    def scenario_description(self):
        return self.by_test_id("grpc-scenario-description")

    @property
    def required_auth(self):
        return self.by_test_id("grpc-required-auth")

    @property
    def selected_auth(self):
        return self.by_test_id("grpc-selected-auth")

    @property
    def command_panel(self):
        return self.by_test_id("grpc-command-panel")

    @property
    def command(self):
        return self.by_test_id("grpc-command")

    @property
    def expected_result(self):
        return self.by_test_id("grpc-expected-result")

    @property
    def reflection_tip(self):
        return self.by_test_id("grpc-reflection-tip")

    @property
    def auth_table(self):
        return self.by_test_id("grpc-auth-table")

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.scenario_select).to_be_visible()
        expect(self.auth_select).to_be_visible()
        expect(self.port_input).to_be_visible()
        expect(self.command_panel).to_be_visible()
        expect(self.auth_table).to_be_visible()

    def select_scenario(self, scenario_id: str) -> None:
        self.scenario_select.select_option(scenario_id)

    def select_auth_profile(self, profile: str) -> None:
        self.auth_select.select_option(profile)

    def set_grpc_port(self, port: str) -> None:
        self.port_input.fill(port)
