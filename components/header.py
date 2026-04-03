from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class Header(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def dashboard_nav(self):
        return self.by_test_id("nav-dashboard")

    @property
    def auth_nav(self):
        return self.by_test_id("nav-auth")

    @property
    def forms_nav(self):
        return self.by_test_id("nav-forms")

    @property
    def tables_nav(self):
        return self.by_test_id("nav-tables")

    @property
    def dynamic_nav(self):
        return self.by_test_id("nav-dynamic")

    @property
    def mobile_auth_nav(self):
        return self.by_test_id("mobile-nav-auth")

    @property
    def mobile_forms_nav(self):
        return self.by_test_id("mobile-nav-forms")

    @property
    def mobile_tables_nav(self):
        return self.by_test_id("mobile-nav-tables")

    @property
    def mobile_dynamic_nav(self):
        return self.by_test_id("mobile-nav-dynamic")

    @property
    def mobile_menu_button(self):
        return self.by_test_id("mobile-menu-button")

    @property
    def mega_menu(self):
        return self.by_test_id("mega-menu")

    @property
    def skip_link(self):
        return self.by_test_id("skip-link")

    def expect_loaded(self) -> None:
        if self.mobile_menu_button.is_visible():
            expect(self.mobile_menu_button).to_be_visible()
            return

        expect(self.dashboard_nav).to_be_visible()
        expect(self.auth_nav).to_be_visible()
        expect(self.mega_menu).to_be_visible()

    def _open_mobile_menu_if_needed(self, target) -> None:
        if not target.is_visible():
            self.mobile_menu_button.click()

    def go_to_auth(self) -> None:
        if self.mobile_menu_button.is_visible():
            self._open_mobile_menu_if_needed(self.mobile_auth_nav)
            self.mobile_auth_nav.click()
            return
        self.auth_nav.click()

    def go_to_forms(self) -> None:
        if self.mobile_menu_button.is_visible():
            self._open_mobile_menu_if_needed(self.mobile_forms_nav)
            self.mobile_forms_nav.click()
            return
        self.forms_nav.click()

    def go_to_tables(self) -> None:
        if self.mobile_menu_button.is_visible():
            self._open_mobile_menu_if_needed(self.mobile_tables_nav)
            self.mobile_tables_nav.click()
            return
        self.tables_nav.click()

    def go_to_dynamic(self) -> None:
        if self.mobile_menu_button.is_visible():
            self._open_mobile_menu_if_needed(self.mobile_dynamic_nav)
            self.mobile_dynamic_nav.click()
            return
        self.dynamic_nav.click()
