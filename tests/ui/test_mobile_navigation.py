from __future__ import annotations

import pytest
from playwright.sync_api import expect

from components.header import Header


@pytest.mark.ui
def test_mobile_menu_navigation_routes_to_core_pages(page) -> None:
    page.set_viewport_size({"width": 430, "height": 932})
    page.goto("/")

    header = Header(page)

    header.expect_loaded()

    header.go_to_forms()
    expect(page).to_have_url("http://localhost:5173/forms")

    header.go_to_tables()
    expect(page).to_have_url("http://localhost:5173/tables")

    header.go_to_dynamic()
    expect(page).to_have_url("http://localhost:5173/dynamic")

    header.go_to_auth()
    expect(page).to_have_url("http://localhost:5173/auth")
