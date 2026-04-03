from __future__ import annotations

import pytest
from playwright.sync_api import expect

from flows.auth_flow import AuthFlow
from pages.auth_page import AuthPage
from pages.home_page import HomePage


@pytest.mark.ui
def test_login_then_dashboard_shows_authenticated_session(page) -> None:
    auth_page = AuthPage(page)
    auth_flow = AuthFlow(auth_page)
    home_page = HomePage(page)

    auth_page.open()
    auth_page.expect_page_ready()
    auth_flow.sign_in_with_demo_user(remember_me=True)

    home_page.open()
    home_page.expect_page_ready()
    home_page.expect_authenticated_session()
    expect(home_page.session_state_card).to_be_visible()
