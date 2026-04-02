from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.i18n_page import I18nPage


@pytest.mark.regression
def test_i18n_locale_timezone_and_rtl(page) -> None:
    i18n_page = I18nPage(page)

    i18n_page.open()
    i18n_page.expect_page_ready()

    page_root = page.locator("main > div").first
    expect(page_root).to_have_attribute("dir", "ltr")
    expect(page.get_by_text("Missing translation: [cta.checkout]")).to_be_visible()

    i18n_page.set_locale("fr-FR")
    expect(page.get_by_text("Pluralization: 3 items")).to_be_visible()

    i18n_page.set_locale("ar")
    expect(page_root).to_have_attribute("dir", "rtl")
    expect(page.get_by_text("Pluralization: 3 items")).to_be_visible()

    i18n_page.set_timezone("Asia/Tokyo")
    expect(page.get_by_text("Selected TZ: Asia/Tokyo")).to_be_visible()
