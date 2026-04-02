from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.experiments_page import ExperimentsPage


@pytest.mark.regression
def test_experiments_variant_and_role_gated_flag(page) -> None:
    experiments_page = ExperimentsPage(page)

    experiments_page.open()
    experiments_page.expect_page_ready()

    experiments_page.choose_variant_b()
    expect(experiments_page.active_variant_label).to_contain_text("B")

    experiments_page.apply_flag_override()
    experiments_page.select_role("admin")
    expect(experiments_page.flag_enabled_label).to_contain_text("true")
