from __future__ import annotations

import sys
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import Settings, load_settings


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
    test_artifact_dir = settings.artifacts_dir / request.node.name
    test_artifact_dir.mkdir(parents=True, exist_ok=True)

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
    if failed or settings.trace == "on":
        context.tracing.stop(path=str(trace_target))
    else:
        context.tracing.stop()
    context.close()


@pytest.fixture
def page(context: BrowserContext, settings: Settings, request: pytest.FixtureRequest) -> Page:
    page = context.new_page()
    yield page

    failed = bool(getattr(request.node, "rep_call", None) and request.node.rep_call.failed)
    if failed or settings.screenshot == "on":
        screenshot_dir = settings.artifacts_dir / request.node.name
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshot_dir / "failure.png"), full_page=True)
    page.close()
