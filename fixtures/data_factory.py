from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class DemoCredentials:
    username: str
    password: str
    mfa_code: str


class DataFactory:
    def demo_credentials(self) -> DemoCredentials:
        return DemoCredentials(username="principal.engineer", password="demo", mfa_code="123456")

    def unique_upload_id(self, prefix: str = "upload") -> str:
        return f"{prefix}-{uuid4().hex[:12]}"

    def unique_order_id(self, prefix: str = "order") -> str:
        return f"{prefix}-{uuid4().hex[:12]}"
