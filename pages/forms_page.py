from __future__ import annotations

from playwright.sync_api import FrameLocator, expect

from components.header import Header
from pages.base_page import BasePage


class FormsPage(BasePage):
    PATH = "/forms"
    ROUTE_NAME = "forms"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def toggle_extra_checkbox(self):
        return self.by_test_id("toggle-extra")

    @property
    def conditional_input(self):
        return self.by_test_id("conditional-input")

    @property
    def wizard_step_label(self):
        return self.by_test_id("wizard-step")

    @property
    def wizard_next_button(self):
        return self.by_test_id("wizard-next")

    @property
    def wizard_prev_button(self):
        return self.by_test_id("wizard-prev")

    @property
    def array_add_button(self):
        return self.by_test_id("array-add")

    @property
    def rich_text_iframe(self) -> FrameLocator:
        return self.page.frame_locator("[data-testid='rich-text-iframe']")

    @property
    def drag_drop_zone(self):
        return self.by_test_id("drag-drop-zone")

    @property
    def upload_progress(self):
        return self.by_test_id("upload-progress")

    @property
    def color_picker(self):
        return self.by_test_id("color-picker")

    @property
    def range_min(self):
        return self.by_test_id("range-min")

    @property
    def range_max(self):
        return self.by_test_id("range-max")

    @property
    def datetime_picker(self):
        return self.by_test_id("datetime-picker")

    @property
    def shadow_host(self):
        return self.by_test_id("shadow-host")

    def array_item(self, index: int):
        return self.by_test_id(f"array-item-{index}")

    def array_remove_button(self, index: int):
        return self.by_test_id(f"array-remove-{index}")

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.toggle_extra_checkbox).to_be_visible()
        expect(self.wizard_step_label).to_be_visible()
        expect(self.array_add_button).to_be_visible()
        expect(self.shadow_host).to_be_visible()

    def show_conditional_field(self) -> None:
        if not self.toggle_extra_checkbox.is_checked():
            self.toggle_extra_checkbox.click()

    def hide_conditional_field(self) -> None:
        if self.toggle_extra_checkbox.is_checked():
            self.toggle_extra_checkbox.click()

    def expect_conditional_field_visible(self) -> None:
        expect(self.conditional_input).to_be_visible()

    def expect_conditional_field_hidden(self) -> None:
        expect(self.conditional_input).to_have_count(0)

    def advance_wizard_to_step(self, step: int) -> None:
        for _ in range(3):
            if self.wizard_step_label.text_content() == f"Step {step} of 3":
                return
            self.wizard_next_button.click()
        expect(self.wizard_step_label).to_contain_text(f"Step {step} of 3")

    def return_wizard_to_step(self, step: int) -> None:
        for _ in range(3):
            if self.wizard_step_label.text_content() == f"Step {step} of 3":
                return
            self.wizard_prev_button.click()
        expect(self.wizard_step_label).to_contain_text(f"Step {step} of 3")

    def add_array_item(self) -> None:
        self.array_add_button.click()

    def remove_array_item(self, index: int) -> None:
        self.array_remove_button(index).click()

    def set_array_item_value(self, index: int, value: str) -> None:
        self.array_item(index).fill(value)

    def expect_array_item_value(self, index: int, value: str) -> None:
        expect(self.array_item(index)).to_have_value(value)

    def set_color(self, value: str) -> None:
        self.color_picker.fill(value)

    def set_range_values(self, minimum: str, maximum: str) -> None:
        self.range_min.fill(minimum)
        self.range_max.fill(maximum)

    def set_datetime(self, value: str) -> None:
        self.datetime_picker.fill(value)

    def fill_rich_text(self, value: str) -> None:
        editor = self.rich_text_iframe.locator("body")
        editor.click()
        editor.fill(value)

    def expect_rich_text(self, value: str) -> None:
        editor = self.rich_text_iframe.locator("body")
        expect(editor).to_contain_text(value)

    def expect_shadow_input_visible(self) -> None:
        shadow_input = self.shadow_host.locator("css=input[data-testid='shadow-input']")
        expect(shadow_input).to_be_visible()
