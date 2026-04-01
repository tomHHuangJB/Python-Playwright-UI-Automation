from __future__ import annotations

import pytest

from pages.tables_page import TablesPage


@pytest.mark.regression
def test_tables_grid_editing_and_server_controls(page) -> None:
    tables_page = TablesPage(page)

    tables_page.open()
    tables_page.expect_page_ready()

    tables_page.select_row(1)
    assert tables_page.row_checkbox(1).is_checked()

    tables_page.update_row_name(1, "Row 1 Updated")
    tables_page.expect_row_name(1, "Row 1 Updated")

    tables_page.update_row_status(1, "Archived")
    tables_page.expect_row_status(1, "Archived")

    tables_page.expect_visible(tables_page.cursor_prev_button)
    tables_page.expect_visible(tables_page.cursor_next_button)
    tables_page.expect_visible(tables_page.offset_next_button)
    tables_page.expect_visible(tables_page.bulk_export_button)
    tables_page.expect_visible(tables_page.bulk_archive_button)
    tables_page.expect_visible(tables_page.resize_column_button)
    tables_page.expect_visible(tables_page.reorder_column_button)
    tables_page.expect_visible(tables_page.pin_column_button)

    tables_page.apply_sort_ascending()
    tables_page.expect_table_status("rows:12")

    tables_page.apply_sort_descending()
    tables_page.expect_table_status("rows:12")

    tables_page.apply_filter_active()
    tables_page.expect_table_status("rows:6")
    # The row-1 controls were intentionally mutated earlier in this test, and the
    # grid uses uncontrolled inputs/selects. For filter verification, assert on
    # unaffected rows plus row-count/absence signals instead of recycled row-1 DOM state.
    assert tables_page.visible_row_count() == 6
    tables_page.expect_row_name(3, "Row 3")
    tables_page.expect_row_status(3, "Active")
    assert tables_page.row_name_input(2).count() == 0
    assert tables_page.row_status_select(2).count() == 0
