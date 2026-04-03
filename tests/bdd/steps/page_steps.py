from __future__ import annotations

from pytest_bdd import given, parsers, then

from pages.base_page import BasePage
from pages.page_registry import PAGE_REGISTRY


def _build_page(route_name: str, page) -> BasePage:
    try:
        page_class = PAGE_REGISTRY[route_name]
    except KeyError as exc:
        supported = ", ".join(sorted(PAGE_REGISTRY))
        raise AssertionError(
            f"Unsupported route '{route_name}'. Supported routes: {supported}"
        ) from exc
    return page_class(page)


@given(parsers.parse('the user opens the "{route_name}" page'), target_fixture="current_page")
def open_named_page(route_name: str, page) -> BasePage:
    current_page = _build_page(route_name, page)
    current_page.open()
    return current_page


@then(parsers.parse('the "{route_name}" page is ready'))
def page_is_ready(route_name: str, current_page: BasePage) -> None:
    assert current_page.route_name() == route_name
    current_page.expect_page_ready()
