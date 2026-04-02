from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.files_page import FilesPage


@pytest.mark.regression
def test_files_upload_and_download_flows(page) -> None:
    files_page = FilesPage(page)

    files_page.open()
    files_page.expect_page_ready()

    for _ in range(5):
        files_page.advance_upload_chunk()

    files_page.expect_upload_complete()
    expect(files_page.upload_progress).to_have_attribute("style", "width: 100%;")

    files_page.trigger_bad_download()
    expect(files_page.download_status).to_contain_text("status:200")
    expect(files_page.download_status).to_contain_text("checksum:bad-hash")

    files_page.trigger_good_download()
    expect(files_page.download_status).to_contain_text("status:200")
    expect(files_page.download_status).to_contain_text("checksum:demo-hash")
