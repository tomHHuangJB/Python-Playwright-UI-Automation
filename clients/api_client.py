from __future__ import annotations

from typing import Any

import requests


class ApiClient:
    def __init__(self, base_api_url: str, timeout_seconds: float = 10.0) -> None:
        self.base_api_url = base_api_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()

    def close(self) -> None:
        self.session.close()

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_api_url}{path}"
        response = self.session.request(
            method=method,
            url=url,
            timeout=self.timeout_seconds,
            **kwargs,
        )
        response.raise_for_status()
        return response

    def get_json(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs).json()

    def post_json(self, path: str, payload: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        return self.request("POST", path, json=payload or {}, **kwargs).json()

    def health(self) -> dict[str, Any]:
        return self.get_json("/health")

    def reset(self) -> dict[str, Any]:
        return self.post_json("/api/reset")

    def seed(self, seed: int = 42) -> dict[str, Any]:
        return self.post_json("/api/seed", {"seed": seed})
