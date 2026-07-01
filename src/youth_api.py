"""HTTP client for the Ontong Youth Center Open API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

import httpx

from .config import Settings


class YouthCenterApiError(Exception):
    """Raised when the upstream Youth Center API cannot be queried."""


@dataclass(frozen=True)
class YouthPolicyClient:
    """Small synchronous HTTP client for the Youth Center policy API."""

    settings: Settings

    def request(self, params: Mapping[str, Any]) -> dict[str, Any]:
        if not self.settings.youth_center_api_key:
            raise YouthCenterApiError("YOUTH_CENTER_API_KEY is not set")

        query = {
            "apiKey": self.settings.youth_center_api_key,
            "rtnType": "json",
            **_without_empty_values(params),
        }

        try:
            with httpx.Client(timeout=self.settings.timeout_seconds) as client:
                response = client.get(self.settings.youth_center_api_url, params=query)
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPStatusError as exc:
            raise YouthCenterApiError(
                f"Youth Center API returned HTTP {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise YouthCenterApiError(f"Youth Center API request failed: {exc}") from exc
        except ValueError as exc:
            raise YouthCenterApiError("Youth Center API returned a non-JSON response") from exc

        if not isinstance(payload, dict):
            raise YouthCenterApiError("Youth Center API returned an unexpected JSON shape")
        return payload

    def search_policies(
        self,
        *,
        keyword: Optional[str] = None,
        policy_name: Optional[str] = None,
        description_keyword: Optional[str] = None,
        region_code: Optional[str] = None,
        category_major: Optional[str] = None,
        category_middle: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> dict[str, Any]:
        return self.request(
            {
                "pageType": 1,
                "plcyKywdNm": keyword,
                "plcyNm": policy_name,
                "plcyExplnCn": description_keyword,
                "zipCd": region_code,
                "lclsfNm": category_major,
                "mclsfNm": category_middle,
                "pageNum": max(page, 1),
                "pageSize": max(min(page_size, 100), 1),
            }
        )

    def get_policy_detail(self, policy_id: str) -> dict[str, Any]:
        return self.request({"pageType": 2, "plcyNo": policy_id})


def _without_empty_values(params: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value not in (None, "")}

