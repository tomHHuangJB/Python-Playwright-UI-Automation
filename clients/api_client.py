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

    def request(
        self,
        method: str,
        path: str,
        *,
        raise_for_status: bool = True,
        **kwargs: Any,
    ) -> requests.Response:
        url = f"{self.base_api_url}{path}"
        response = self.session.request(
            method=method,
            url=url,
            timeout=self.timeout_seconds,
            **kwargs,
        )
        if raise_for_status:
            response.raise_for_status()
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(
        self,
        path: str,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self.request("POST", path, json=payload or {}, **kwargs)

    def put(
        self,
        path: str,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self.request("PUT", path, json=payload or {}, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def get_json(self, path: str, **kwargs: Any) -> Any:
        return self.get(path, **kwargs).json()

    def post_json(self, path: str, payload: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        return self.post(path, payload=payload, **kwargs).json()

    def put_json(self, path: str, payload: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        return self.put(path, payload=payload, **kwargs).json()

    def delete_json(self, path: str, **kwargs: Any) -> Any:
        return self.delete(path, **kwargs).json()

    def health(self) -> dict[str, Any]:
        return self.get_json("/health")

    def reset(self) -> dict[str, Any]:
        return self.post_json("/api/reset")

    def seed(self, seed: int = 42) -> dict[str, Any]:
        return self.post_json("/api/seed", {"seed": seed})
