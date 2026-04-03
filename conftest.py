from __future__ import annotations

import os

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from clients.api_client import ApiClient
from config.settings import Settings, load_settings
from fixtures.data_factory import DataFactory, TestRunContext
from fixtures.sut import SutController
from utils.artifact_utils import (
    artifact_dir,
    capture_screenshot,
    stop_trace,
    write_json_artifact,
    write_text_artifact,
)

pytest_plugins = [
    "tests.bdd.steps.page_steps",
    "tests.bdd.steps.workflow_steps",
]


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "smoke: fast smoke coverage for critical routes")
    config.addinivalue_line("markers", "regression: broader feature coverage")
    config.addinivalue_line("markers", "ui: focused cross-page workflows")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Browser:
    browser_launcher = getattr(playwright_instance, settings.browser_name)
    browser = browser_launcher.launch(headless=settings.headless, slow_mo=settings.slow_mo_ms)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser, settings: Settings, request: pytest.FixtureRequest) -> BrowserContext:
    test_artifact_dir = artifact_dir(settings.artifacts_dir, request.node.nodeid)

    context = browser.new_context(
        base_url=settings.base_ui_url,
        viewport={"width": settings.viewport_width, "height": settings.viewport_height},
        ignore_https_errors=True,
        record_video_dir=str(test_artifact_dir / "video") if settings.video != "off" else None,
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context

    failed = bool(getattr(request.node, "rep_call", None) and request.node.rep_call.failed)
    trace_target = test_artifact_dir / "trace.zip"
    stop_trace(context, failed, settings.trace, trace_target)
    context.close()


@pytest.fixture
def page(context: BrowserContext, settings: Settings, request: pytest.FixtureRequest) -> Page:
    test_artifact_dir = artifact_dir(settings.artifacts_dir, request.node.nodeid)
    page = context.new_page()

    console_events: list[dict[str, str]] = []
    page_errors: list[str] = []
    request_failures: list[dict[str, str]] = []

    def on_console(message) -> None:
        console_events.append(
            {
                "type": message.type,
                "text": message.text,
                "location": str(message.location),
            }
        )

    def on_page_error(error) -> None:
        page_errors.append(str(error))

    def on_request_failed(failed_request) -> None:
        failure = failed_request.failure or ""
        request_failures.append(
            {
                "url": failed_request.url,
                "method": failed_request.method,
                "resource_type": failed_request.resource_type,
                "error_text": str(failure),
            }
        )

    page.on("console", on_console)
    page.on("pageerror", on_page_error)
    page.on("requestfailed", on_request_failed)
    yield page

    failed = bool(getattr(request.node, "rep_call", None) and request.node.rep_call.failed)
    if failed or settings.screenshot == "on":
        screenshot_target = test_artifact_dir / "failure.png"
        capture_screenshot(page, screenshot_target)
    if failed:
        write_json_artifact(test_artifact_dir / "console-events.json", console_events)
        write_json_artifact(test_artifact_dir / "request-failures.json", request_failures)
        write_text_artifact(test_artifact_dir / "page-errors.txt", "\n".join(page_errors))
    page.close()


@pytest.fixture(scope="session")
def api_client(settings: Settings) -> ApiClient:
    client = ApiClient(settings.base_api_url)
    yield client
    client.close()


@pytest.fixture(scope="session")
def data_factory(settings: Settings) -> DataFactory:
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "local")
    run_context = TestRunContext(
        run_id=settings.test_run_id,
        worker_id=worker_id,
        seed=settings.data_seed,
    )
    return DataFactory(settings.project_root, run_context)


@pytest.fixture
def sut(api_client: ApiClient) -> SutController:
    return SutController(api_client)
