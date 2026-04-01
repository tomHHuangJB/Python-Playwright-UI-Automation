from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class TablesPage(BasePage):
    PATH = "/tables"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def data_grid(self):
        return self.by_test_id("data-grid")

    @property
    def bulk_export_button(self):
        return self.by_test_id("bulk-export")

    @property
    def bulk_archive_button(self):
        return self.by_test_id("bulk-archive")

    @property
    def cursor_prev_button(self):
        return self.by_test_id("cursor-prev")

    @property
    def cursor_next_button(self):
        return self.by_test_id("cursor-next")

    @property
    def offset_next_button(self):
        return self.by_test_id("offset-next")

    @property
    def resize_column_button(self):
        return self.by_test_id("col-resize")

    @property
    def reorder_column_button(self):
        return self.by_test_id("col-reorder")

    @property
    def pin_column_button(self):
        return self.by_test_id("col-pin")

    @property
    def sort_asc_button(self):
        return self.by_test_id("sort-asc")

    @property
    def sort_desc_button(self):
        return self.by_test_id("sort-desc")

    @property
    def filter_active_button(self):
        return self.by_test_id("filter-active")

    @property
    def table_status(self):
        return self.by_test_id("table-status")

    def row_checkbox(self, row_id: int):
        return self.by_test_id(f"row-select-{row_id}")

    def row_name_input(self, row_id: int):
        return self.by_test_id(f"row-name-{row_id}")

    def row_status_select(self, row_id: int):
        return self.by_test_id(f"row-status-{row_id}")

    def open(self) -> None:
        self.goto(self.PATH)

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.data_grid).to_be_visible()
        expect(self.bulk_export_button).to_be_visible()
        expect(self.sort_asc_button).to_be_visible()

    def select_row(self, row_id: int) -> None:
        self.row_checkbox(row_id).check()

    def update_row_name(self, row_id: int, value: str) -> None:
        row_input = self.row_name_input(row_id)
        row_input.fill(value)
        row_input.blur()

    def update_row_status(self, row_id: int, value: str) -> None:
        self.row_status_select(row_id).select_option(value)

    def expect_row_name(self, row_id: int, value: str) -> None:
        expect(self.row_name_input(row_id)).to_have_value(value)

    def expect_row_status(self, row_id: int, value: str) -> None:
        expect(self.row_status_select(row_id)).to_have_value(value)

    def visible_row_count(self) -> int:
        return self.page.locator("[data-testid^='row-name-']").count()

    def apply_sort_ascending(self) -> None:
        self.sort_asc_button.click()

    def apply_sort_descending(self) -> None:
        self.sort_desc_button.click()

    def apply_filter_active(self) -> None:
        self.filter_active_button.click()

    def expect_table_status(self, value: str) -> None:
        expect(self.table_status).to_contain_text(value)
