from __future__ import annotations

import pytest
from playwright.sync_api import expect

from components.header import Header
from pages.forms_page import FormsPage
from pages.home_page import HomePage


@pytest.mark.ui
def test_navigate_to_forms_from_home(page) -> None:
    home_page = HomePage(page)
    header = Header(page)
    forms_page = FormsPage(page)

    home_page.open()
    home_page.expect_page_ready()

    header.go_to_forms()

    expect(page).to_have_url("http://localhost:5173/forms")
    forms_page.expect_page_ready()
    expect(forms_page.toggle_extra_checkbox).to_be_visible()
