from __future__ import annotations

from playwright.sync_api import Page, expect


class Header:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def dashboard_nav(self):
        return self.page.get_by_test_id("nav-dashboard")

    @property
    def auth_nav(self):
        return self.page.get_by_test_id("nav-auth")

    @property
    def forms_nav(self):
        return self.page.get_by_test_id("nav-forms")

    @property
    def tables_nav(self):
        return self.page.get_by_test_id("nav-tables")

    @property
    def dynamic_nav(self):
        return self.page.get_by_test_id("nav-dynamic")

    @property
    def mobile_menu_button(self):
        return self.page.get_by_test_id("mobile-menu-button")

    @property
    def mega_menu(self):
        return self.page.get_by_test_id("mega-menu")

    @property
    def skip_link(self):
        return self.page.get_by_test_id("skip-link")

    def expect_loaded(self) -> None:
        if self.mobile_menu_button.is_visible():
            expect(self.mobile_menu_button).to_be_visible()
            return

        expect(self.dashboard_nav).to_be_visible()
        expect(self.auth_nav).to_be_visible()
        expect(self.mega_menu).to_be_visible()

    def go_to_auth(self) -> None:
        self.auth_nav.click()

    def go_to_forms(self) -> None:
        self.forms_nav.click()

    def go_to_tables(self) -> None:
        self.tables_nav.click()

    def go_to_dynamic(self) -> None:
        self.dynamic_nav.click()
