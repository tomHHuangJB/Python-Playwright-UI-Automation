from __future__ import annotations

from dataclasses import dataclass

from playwright.sync_api import Page


@dataclass(frozen=True)
class NavigationTiming:
    dom_content_loaded_ms: float
    load_event_ms: float
    duration_ms: float
    response_start_ms: float


def read_navigation_timing(page: Page) -> NavigationTiming:
    timing = page.evaluate(
        """
        () => {
          const [entry] = performance.getEntriesByType("navigation");
          if (!entry) {
            return null;
          }

          return {
            domContentLoadedMs: entry.domContentLoadedEventEnd,
            loadEventMs: entry.loadEventEnd,
            durationMs: entry.duration,
            responseStartMs: entry.responseStart
          };
        }
        """
    )
    if timing is None:
        raise AssertionError("Navigation timing entry was not available")

    return NavigationTiming(
        dom_content_loaded_ms=float(timing["domContentLoadedMs"]),
        load_event_ms=float(timing["loadEventMs"]),
        duration_ms=float(timing["durationMs"]),
        response_start_ms=float(timing["responseStartMs"]),
    )
