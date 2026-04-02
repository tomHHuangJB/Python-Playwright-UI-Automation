from __future__ import annotations

from components.debug_panel import DebugPanel
from components.header import Header


class NavigationFlow:
    def __init__(self, header: Header, debug_panel: DebugPanel) -> None:
        self.header = header
        self.debug_panel = debug_panel

    def traverse_primary_routes(self) -> None:
        self.header.go_to_auth()
        self.header.go_to_forms()
        self.header.go_to_tables()
        self.header.go_to_dynamic()
        self.header.dashboard_nav.click()

    def open_debug_panel(self) -> None:
        self.debug_panel.open()
        self.debug_panel.expect_open()
