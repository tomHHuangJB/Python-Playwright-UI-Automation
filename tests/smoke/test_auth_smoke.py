import pytest

from flows.auth_flow import AuthFlow
from pages.auth_page import AuthPage


@pytest.mark.smoke
def test_auth_login_smoke(page) -> None:
    auth_page = AuthPage(page)
    auth_flow = AuthFlow(auth_page)

    auth_page.open()
    auth_page.expect_page_ready()
    auth_flow.sign_in_with_demo_user(remember_me=True)
    auth_page.expect_session_controls()
