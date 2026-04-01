import pytest

from pages.home_page import HomePage


@pytest.mark.smoke
def test_home_dashboard_smoke(page) -> None:
    home_page = HomePage(page)

    home_page.open()
    home_page.expect_page_ready()
    home_page.expect_authenticated_session()
    home_page.expect_websocket_state("connected")
