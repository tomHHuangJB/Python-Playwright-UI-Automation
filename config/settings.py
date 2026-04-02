from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    project_root: Path
    base_ui_url: str
    base_api_url: str
    browser_name: str
    headless: bool
    slow_mo_ms: int
    trace: str
    video: str
    screenshot: str
    artifacts_dir: Path
    viewport_width: int
    viewport_height: int
    perf_navigation_max_ms: float
    perf_dom_content_loaded_max_ms: float


def load_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[1]
    return Settings(
        project_root=project_root,
        base_ui_url=os.getenv("BASE_UI_URL", "http://localhost:5173"),
        base_api_url=os.getenv("BASE_API_URL", "http://localhost:3001"),
        browser_name=os.getenv("BROWSER", "chromium"),
        headless=_as_bool(os.getenv("HEADLESS"), True),
        slow_mo_ms=int(os.getenv("SLOW_MO_MS", "0")),
        trace=os.getenv("TRACE", "retain-on-failure"),
        video=os.getenv("VIDEO", "retain-on-failure"),
        screenshot=os.getenv("SCREENSHOT", "only-on-failure"),
        artifacts_dir=Path(os.getenv("ARTIFACTS_DIR", str(project_root / "artifacts"))),
        viewport_width=int(os.getenv("VIEWPORT_WIDTH", "1440")),
        viewport_height=int(os.getenv("VIEWPORT_HEIGHT", "900")),
        perf_navigation_max_ms=float(os.getenv("PERF_NAVIGATION_MAX_MS", "4000")),
        perf_dom_content_loaded_max_ms=float(os.getenv("PERF_DOM_CONTENT_LOADED_MAX_MS", "2500")),
    )
