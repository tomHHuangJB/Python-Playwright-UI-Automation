from __future__ import annotations

from pathlib import Path

from playwright.sync_api import BrowserContext, Page


def artifact_dir(root: Path, test_name: str) -> Path:
    path = root / test_name
    path.mkdir(parents=True, exist_ok=True)
    return path


def stop_trace(context: BrowserContext, failed: bool, trace_mode: str, trace_path: Path) -> None:
    if failed or trace_mode == "on":
        context.tracing.stop(path=str(trace_path))
    else:
        context.tracing.stop()


def capture_screenshot(page: Page, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(target), full_page=True)
