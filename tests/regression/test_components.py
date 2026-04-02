from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.components_page import ComponentsPage


@pytest.mark.regression
def test_components_visual_and_interaction_coverage(page) -> None:
    components_page = ComponentsPage(page)

    components_page.open()
    components_page.expect_page_ready()

    before = components_page.infinite_items_count()
    components_page.load_more_items()
    page.wait_for_function(
        """
        ([selector, count]) => document.querySelectorAll(selector).length > count
        """,
        arg=["[data-testid='infinite-scroll'] div.rounded", before],
    )

    components_page.select_bar_b()
    expect(components_page.active_bar_label).to_contain_text("B")

    page.once("dialog", lambda dialog: dialog.accept())
    components_page.open_context_menu()

    components_page.trigger_toast()
    # The toast is transient, so wait for its business signal to exist in the DOM
    # instead of checking once.
    page.wait_for_function(
        """
        () => document.querySelectorAll('[data-testid="toast-item"]').length > 0
        """
    )

    components_page.tooltip_trigger.hover()
    expect(components_page.tooltip_content).to_be_visible()
