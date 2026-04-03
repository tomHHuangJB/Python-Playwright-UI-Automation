from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Generator
from pathlib import Path

import allure
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

LAYER_LABELS = ("smoke", "bdd", "ui", "regression", "perf")
SEVERITY_BY_LAYER = {
    "smoke": allure.severity_level.CRITICAL,
    "bdd": allure.severity_level.CRITICAL,
    "ui": allure.severity_level.NORMAL,
    "regression": allure.severity_level.NORMAL,
    "perf": allure.severity_level.MINOR,
}
FEATURE_NAME_OVERRIDES = {
    "a11y": "Accessibility",
    "auth": "Authentication",
    "components": "Components",
    "debug_panel": "Debug Panel",
    "errors": "Errors",
    "experiments": "Experiments",
    "files": "Files",
    "forms": "Forms",
    "grpc": "gRPC",
    "home": "Home",
    "i18n": "Internationalization",
    "integrations": "Integrations",
    "mobile": "Mobile",
    "navigation": "Navigation",
    "performance": "Performance",
    "selectors": "Selectors",
    "system": "System",
    "tables": "Tables",
}
OWNER_BY_FEATURE = {
    "Accessibility": "quality-engineering",
    "Authentication": "identity-platform",
    "Components": "frontend-platform",
    "Debug Panel": "quality-engineering",
    "Errors": "platform-reliability",
    "Experiments": "growth-platform",
    "Files": "content-platform",
    "Forms": "frontend-platform",
    "gRPC": "backend-platform",
    "Home": "frontend-platform",
    "Internationalization": "frontend-platform",
    "Integrations": "integrations-platform",
    "Mobile": "mobile-experience",
    "Navigation": "frontend-platform",
    "Performance": "platform-reliability",
    "Selectors": "quality-engineering",
    "System": "platform-reliability",
    "Tables": "frontend-platform",
    "General": "quality-engineering",
}
RISK_BY_LAYER = {
    "smoke": "critical-path",
    "bdd": "business-critical",
    "ui": "workflow",
    "regression": "broad-regression",
    "perf": "performance-guardrail",
}
STATEFUL_LAYERS = frozenset(LAYER_LABELS)


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "smoke: fast smoke coverage for critical routes")
    config.addinivalue_line("markers", "regression: broader feature coverage")
    config.addinivalue_line("markers", "ui: focused cross-page workflows")
    config.addinivalue_line(
        "markers",
        "quarantined(reason): known-flaky or temporarily blocked test excluded "
        "from normal runs unless INCLUDE_QUARANTINED=1",
    )
    config.addinivalue_line(
        "markers",
        "preserve_state: skip automatic API reset/seed baseline for "
        "a test that must manage state itself",
    )


def _layer_for_item(item: pytest.Item) -> str:
    path_parts = Path(str(item.path)).parts
    for layer in LAYER_LABELS:
        if layer in path_parts:
            return layer

    item_markers = {marker.name for marker in item.iter_markers()}
    for layer in LAYER_LABELS:
        if layer in item_markers:
            return layer
    return "ui"


def _declared_layers(item: pytest.Item) -> set[str]:
    return {marker.name for marker in item.iter_markers() if marker.name in LAYER_LABELS}


def _feature_for_item(item: pytest.Item) -> str:
    nodeid = item.nodeid.lower()
    for key, label in FEATURE_NAME_OVERRIDES.items():
        if key in nodeid:
            return label

    stem = Path(str(item.path)).stem.replace("test_", "").replace("_", " ").title()
    return stem or "General"


def _seed_value_from_settings(settings: Settings) -> int:
    try:
        return int(settings.data_seed)
    except ValueError:
        digest = hashlib.sha256(settings.data_seed.encode("utf-8")).hexdigest()
        return int(digest[:8], 16)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    quarantined_marker = item.get_closest_marker("quarantined")
    if quarantined_marker is not None and os.getenv("INCLUDE_QUARANTINED", "0") != "1":
        reason = quarantined_marker.args[0] if quarantined_marker.args else "No reason recorded"
        pytest.skip(f"Quarantined test skipped by default: {reason}")

    layer = _layer_for_item(item)
    feature = _feature_for_item(item)
    owner = OWNER_BY_FEATURE.get(feature, "quality-engineering")
    risk = RISK_BY_LAYER[layer]
    severity = SEVERITY_BY_LAYER[layer]

    allure.dynamic.parent_suite("UI Automation")
    allure.dynamic.suite(layer.upper())
    allure.dynamic.sub_suite(feature)
    allure.dynamic.feature(feature)
    allure.dynamic.tag(layer, feature.lower().replace(" ", "-"), risk, owner)
    allure.dynamic.label("owner", owner)
    allure.dynamic.parameter("owner", owner)
    allure.dynamic.parameter("risk", risk)
    allure.dynamic.severity(severity)
    if quarantined_marker is not None:
        reason = quarantined_marker.args[0] if quarantined_marker.args else "No reason recorded"
        allure.dynamic.tag("quarantined")
        allure.dynamic.parameter("quarantine_reason", reason)

    if layer == "bdd":
        allure.dynamic.epic("Business Workflows")
        allure.dynamic.story(feature)
    elif layer == "smoke":
        allure.dynamic.epic("Critical Path")
    elif layer == "perf":
        allure.dynamic.epic("Performance Guardrails")
    else:
        allure.dynamic.epic("UI Coverage")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    for item in items:
        expected_layer = _layer_for_item(item)
        declared_layers = _declared_layers(item)

        if expected_layer not in declared_layers:
            item.add_marker(getattr(pytest.mark, expected_layer))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Generator[Browser, None, None]:
    browser_launcher = getattr(playwright_instance, settings.browser_name)
    browser = browser_launcher.launch(headless=settings.headless, slow_mo=settings.slow_mo_ms)
    yield browser
    browser.close()


@pytest.fixture
def context(
    browser: Browser, settings: Settings, request: pytest.FixtureRequest
) -> Generator[BrowserContext, None, None]:
    test_artifact_dir = artifact_dir(settings.artifacts_dir, request.node.nodeid)
    video_dir = test_artifact_dir / "video"

    context = browser.new_context(
        base_url=settings.base_ui_url,
        viewport={"width": settings.viewport_width, "height": settings.viewport_height},
        ignore_https_errors=True,
        record_video_dir=str(video_dir) if settings.video != "off" else None,
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context

    failed = bool(getattr(request.node, "rep_call", None) and request.node.rep_call.failed)
    trace_target = test_artifact_dir / "trace.zip"
    stop_trace(context, failed, settings.trace, trace_target)
    context.close()
    if failed and trace_target.exists():
        allure.attach.file(
            str(trace_target),
            name="playwright-trace",
            attachment_type="application/zip",
        )
    if failed and video_dir.exists():
        for video_file in sorted(video_dir.glob("*.webm")):
            allure.attach.file(
                str(video_file),
                name=f"video-{video_file.stem}",
                attachment_type="video/webm",
            )


@pytest.fixture
def page(
    context: BrowserContext, settings: Settings, request: pytest.FixtureRequest
) -> Generator[Page, None, None]:
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
            allure.attach.file(
                str(screenshot_target),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
    if failed:
        baseline_state = getattr(request.node, "sut_baseline", None)
        if baseline_state is not None:
            write_json_artifact(test_artifact_dir / "baseline-state.json", baseline_state)
            allure.attach(
                json.dumps(baseline_state, indent=2, sort_keys=True),
                name="baseline-state",
                attachment_type=allure.attachment_type.JSON,
            )
        write_json_artifact(test_artifact_dir / "console-events.json", console_events)
        write_json_artifact(test_artifact_dir / "request-failures.json", request_failures)
        write_text_artifact(test_artifact_dir / "page-errors.txt", "\n".join(page_errors))
        allure.attach(
            json.dumps(console_events, indent=2, sort_keys=True),
            name="console-events",
            attachment_type=allure.attachment_type.JSON,
        )
        allure.attach(
            json.dumps(request_failures, indent=2, sort_keys=True),
            name="request-failures",
            attachment_type=allure.attachment_type.JSON,
        )
        allure.attach(
            "\n".join(page_errors) or "No page errors captured.",
            name="page-errors",
            attachment_type=allure.attachment_type.TEXT,
        )
    page.close()


@pytest.fixture(scope="session")
def api_client(settings: Settings) -> Generator[ApiClient, None, None]:
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


@pytest.fixture(autouse=True)
def isolated_sut_state(
    request: pytest.FixtureRequest, settings: Settings, sut: SutController
) -> dict[str, object] | None:
    layer = _layer_for_item(request.node)
    if layer not in STATEFUL_LAYERS:
        return None

    if request.node.get_closest_marker("preserve_state"):
        return None

    health = sut.ensure_healthy()
    reset_result = sut.reset_state()
    seed_value = _seed_value_from_settings(settings)
    seed_result = sut.seed_state(seed_value)

    baseline_state = {
        "layer": layer,
        "seed": seed_value,
        "health": health,
        "reset": reset_result,
        "seed_result": seed_result,
    }
    allure.dynamic.parameter("sut_seed", seed_value)
    allure.dynamic.parameter("sut_layer", layer)
    request.node.sut_baseline = baseline_state
    return baseline_state


@pytest.fixture
def sut(api_client: ApiClient) -> SutController:
    return SutController(api_client)
