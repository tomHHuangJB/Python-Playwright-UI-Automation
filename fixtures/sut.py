from __future__ import annotations

from clients.api_client import ApiClient


class SutController:
    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    def ensure_healthy(self) -> dict:
        return self.api_client.health()

    def reset_state(self) -> dict:
        return self.api_client.reset()

    def seed_state(self, seed: int = 42) -> dict:
        return self.api_client.seed(seed)
