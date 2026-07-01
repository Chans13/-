"""Configuration for the Youth Center MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_API_URL = "https://www.youthcenter.go.kr/opi/youthPlcyList.do"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_TRANSPORT = "streamable-http"
DEFAULT_TIMEOUT_SECONDS = 15.0


@dataclass(frozen=True)
class Settings:
    """Runtime settings read from environment variables."""

    youth_center_api_key: str
    youth_center_api_url: str
    host: str
    port: int
    transport: str
    timeout_seconds: float


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number") from exc


def get_settings() -> Settings:
    """Load settings from process environment."""

    return Settings(
        youth_center_api_key=os.getenv("YOUTH_CENTER_API_KEY", ""),
        youth_center_api_url=os.getenv("YOUTH_CENTER_API_URL", DEFAULT_API_URL),
        host=os.getenv("MCP_HOST", DEFAULT_HOST),
        port=_get_int("MCP_PORT", DEFAULT_PORT),
        transport=os.getenv("MCP_TRANSPORT", DEFAULT_TRANSPORT),
        timeout_seconds=_get_float("YOUTH_CENTER_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS),
    )

