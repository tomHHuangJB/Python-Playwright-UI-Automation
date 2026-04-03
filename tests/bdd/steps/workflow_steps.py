from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import expect
from pytest_bdd import given, parsers, then, when

from flows.auth_flow import AuthFlow
from pages.auth_page import AuthPage
from pages.dynamic_page import DynamicPage
from pages.files_page import FilesPage
from pages.forms_page import FormsPage
from pages.tables_page import TablesPage


def _load_forms_case() -> dict:
    data_path = Path(__file__).resolve().parents[3] / "test_data" / "ui" / "forms_cases.json"
    return json.loads(data_path.read_text())


@given("deterministic browser hooks are installed for the dynamic page")
def install_dynamic_hooks(page) -> None:
    page.add_init_script(
        """
        Math.random = () => 0.9;
        Object.defineProperty(navigator, "serviceWorker", {
          configurable: true,
          value: {
            register: async () => ({ scope: "/sw.js" }),
            getRegistrations: async () => [{ unregister: async () => true }]
          }
        });
        """
    )


@when("the user signs in with the demo account")
def sign_in_demo_account(current_page) -> None:
    auth_page = AuthPage(current_page.page)
    auth_page.expect_page_ready()
    AuthFlow(auth_page).sign_in_with_demo_user(remember_me=True)


@when("the user signs in with the demo account without remember me")
def sign_in_demo_account_without_remember_me(current_page) -> None:
    auth_page = AuthPage(current_page.page)
    auth_page.expect_page_ready()
    AuthFlow(auth_page).sign_in_with_demo_user(remember_me=False)


@when("the user submits the demo MFA code")
def submit_demo_mfa_code(current_page) -> None:
    AuthFlow(AuthPage(current_page.page)).complete_mfa("123456")


@then("the auth page shows a signed-in token")
def auth_page_shows_signed_in_token(current_page) -> None:
    AuthPage(current_page.page).expect_signed_in()


@then("the auth page shows the session controls")
def auth_page_shows_session_controls(current_page) -> None:
    AuthPage(current_page.page).expect_session_controls()


@then("the auth page shows a rotated refresh token")
def auth_page_shows_rotated_refresh_token(current_page) -> None:
    AuthPage(current_page.page).expect_mfa_refreshed()


@when("the user toggles the conditional field on the forms page")
def show_forms_conditional_field(current_page) -> None:
    forms_page = FormsPage(current_page.page)
    forms_page.expect_page_ready()
    forms_page.expect_conditional_field_hidden()
    forms_page.show_conditional_field()


@when("the user completes the forms workflow using shared test data")
def complete_forms_workflow(current_page) -> None:
    forms_page = FormsPage(current_page.page)
    forms_case = _load_forms_case()

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


@then("the forms page shows the conditional field")
def forms_page_shows_conditional_field(current_page) -> None:
    FormsPage(current_page.page).expect_conditional_field_visible()


@then("the forms page keeps advanced widgets ready")
def forms_page_keeps_advanced_widgets_ready(current_page) -> None:
    forms_page = FormsPage(current_page.page)
    forms_page.expect_shadow_input_visible()
    expect(forms_page.drag_drop_zone).to_be_visible()
    expect(forms_page.upload_progress).to_be_visible()


@when("the user updates table row 1")
def update_table_row_1(current_page) -> None:
    tables_page = TablesPage(current_page.page)
    tables_page.expect_page_ready()
    tables_page.select_row(1)
    tables_page.update_row_name(1, "Row 1 Updated")
    tables_page.update_row_status(1, "Archived")
    tables_page.expect_row_name(1, "Row 1 Updated")
    tables_page.expect_row_status(1, "Archived")


@when("the user filters the table to active rows")
def filter_table_to_active_rows(current_page) -> None:
    tables_page = TablesPage(current_page.page)
    tables_page.apply_sort_ascending()
    tables_page.expect_table_status("rows:12")
    tables_page.apply_sort_descending()
    tables_page.expect_table_status("rows:12")
    tables_page.apply_filter_active()
    tables_page.expect_table_status("rows:6")


@then("the table shows six visible rows")
def table_shows_six_visible_rows(current_page) -> None:
    tables_page = TablesPage(current_page.page)
    assert tables_page.visible_row_count() == 6
    assert tables_page.row_name_input(2).count() == 0
    assert tables_page.row_status_select(2).count() == 0


@then("table row 3 remains active")
def table_row_3_remains_active(current_page) -> None:
    tables_page = TablesPage(current_page.page)
    tables_page.expect_row_name(3, "Row 3")
    tables_page.expect_row_status(3, "Active")


@when("the user exercises the dynamic async controls")
def exercise_dynamic_async_controls(current_page) -> None:
    dynamic_page = DynamicPage(current_page.page)
    dynamic_page.expect_page_ready()
    dynamic_page.trigger_optimistic_update()
    dynamic_page.trigger_race_requests()
    dynamic_page.trigger_dedup()
    dynamic_page.trigger_partial_fetch()
    dynamic_page.toggle_consistency()
    dynamic_page.register_service_worker()
    dynamic_page.unregister_service_worker()


@then("the dynamic page shows the expected async results")
def dynamic_page_shows_expected_async_results(current_page) -> None:
    dynamic_page = DynamicPage(current_page.page)
    dynamic_page.expect_optimistic_saved()
    expect(dynamic_page.dynamic_log).to_contain_text("Optimistic update confirmed")
    expect(dynamic_page.race_results).to_contain_text("fast:200ms")
    expect(dynamic_page.race_results).to_contain_text("slow:800ms")
    expect(dynamic_page.dedup_status).to_contain_text("fresh -> cached")
    expect(dynamic_page.partial_status).to_contain_text("status:206")
    expect(dynamic_page.consistency_status).to_contain_text("visibleAfter:2000ms")
    expect(dynamic_page.sw_status).to_contain_text("unregistered")
    expect(dynamic_page.partial_failure).to_contain_text("Partial failure")


@when("the user advances upload processing to completion")
def advance_upload_processing_to_completion(current_page) -> None:
    files_page = FilesPage(current_page.page)
    files_page.expect_page_ready()
    for _ in range(5):
        files_page.advance_upload_chunk()


@when("the user runs the file download status checks")
def run_file_download_status_checks(current_page) -> None:
    files_page = FilesPage(current_page.page)
    files_page.trigger_bad_download()
    expect(files_page.download_status).to_contain_text("checksum:bad-hash")
    files_page.trigger_good_download()


@then("the file upload reports complete")
def file_upload_reports_complete(current_page) -> None:
    files_page = FilesPage(current_page.page)
    files_page.expect_upload_complete()
    expect(files_page.upload_progress).to_have_attribute("style", "width: 100%;")


@then("the file download status includes the demo hash")
def file_download_status_includes_demo_hash(current_page) -> None:
    files_page = FilesPage(current_page.page)
    expect(files_page.download_status).to_contain_text("status:200")
    expect(files_page.download_status).to_contain_text("checksum:demo-hash")

