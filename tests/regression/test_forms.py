from __future__ import annotations

import json
from pathlib import Path

import pytest

from pages.forms_page import FormsPage


def load_forms_case() -> dict:
    data_path = Path(__file__).resolve().parents[2] / "test_data" / "ui" / "forms_cases.json"
    return json.loads(data_path.read_text())


@pytest.mark.regression
def test_forms_core_interactions(page) -> None:
    forms_case = load_forms_case()
    forms_page = FormsPage(page)

    forms_page.open()
    forms_page.expect_page_ready()

    forms_page.expect_conditional_field_hidden()
    forms_page.show_conditional_field()
    forms_page.expect_conditional_field_visible()
    forms_page.hide_conditional_field()
    forms_page.expect_conditional_field_hidden()

    forms_page.advance_wizard_to_step(forms_case["wizard_target_step"])
    forms_page.return_wizard_to_step(1)

    forms_page.add_array_item()
    forms_page.set_array_item_value(1, forms_case["array_new_value"])
    forms_page.expect_array_item_value(1, forms_case["array_new_value"])
    forms_page.remove_array_item(1)

    forms_page.fill_rich_text(forms_case["rich_text_value"])
    forms_page.expect_rich_text(forms_case["rich_text_value"])

    forms_page.set_color(forms_case["color_value"])
    forms_page.set_range_values(forms_case["range_min"], forms_case["range_max"])
    forms_page.set_datetime(forms_case["datetime_value"])

    assert forms_page.color_picker.input_value() == forms_case["color_value"]
    assert forms_page.range_min.input_value() == forms_case["range_min"]
    assert forms_page.range_max.input_value() == forms_case["range_max"]
    assert forms_page.datetime_picker.input_value() == forms_case["datetime_value"]

    forms_page.expect_shadow_input_visible()
    forms_page.expect_visible(forms_page.drag_drop_zone)
    forms_page.expect_visible(forms_page.upload_progress)
