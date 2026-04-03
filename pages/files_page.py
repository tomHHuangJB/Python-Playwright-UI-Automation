from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class FilesPage(BasePage):
    PATH = "/files"
    ROUTE_NAME = "files"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def file_input(self):
        return self.by_test_id("file-input")

    @property
    def upload_progress(self):
        return self.by_test_id("upload-progress")

    @property
    def upload_advance_button(self):
        return self.by_test_id("upload-advance")

    @property
    def upload_status(self):
        return self.by_test_id("upload-status")

    @property
    def download_csv_button(self):
        return self.by_test_id("download-csv")

    @property
    def download_pdf_button(self):
        return self.by_test_id("download-pdf")

    @property
    def download_retry_button(self):
        return self.by_test_id("download-retry")

    @property
    def download_resume_button(self):
        return self.by_test_id("download-resume")

    @property
    def download_status(self):
        return self.by_test_id("download-status")

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.file_input).to_be_visible()
        expect(self.upload_advance_button).to_be_visible()
        expect(self.download_csv_button).to_be_visible()

    def advance_upload_chunk(self) -> None:
        self.upload_advance_button.click()

    def expect_upload_complete(self) -> None:
        expect(self.upload_status).to_contain_text("complete")

    def trigger_bad_download(self) -> None:
        self.download_retry_button.click()

    def trigger_good_download(self) -> None:
        self.download_resume_button.click()
