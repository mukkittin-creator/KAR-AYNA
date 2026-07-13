# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# http://www.apache.org/licenses/LICENSE-2.0

"""
Copyright 2026

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import re
import time
from typing import Any

from pydantic import BaseModel, Field

from utils.logger import StructuredLogger
from utils.normalizer import normalize_financial_value
from utils.state import SharedState


class ExtractedProduct(BaseModel):
    """Structured output contract for extracted product details."""

    product_name: str = Field(default="")
    profit_share_rate: float | None = None
    maturity: int | None = None
    fees: str | None = None
    source_terms: list[str] = Field(default_factory=list)


class ExtractorAgent:
    """Extracts product data from unstructured banking copy with regex-first local parsing."""

    def __init__(self) -> None:
        self.logger = StructuredLogger()

    def extract(self, text: str, campaign_type: str | None = None, state: SharedState | None = None) -> list[dict[str, Any]]:
        start_time = time.perf_counter()
        if not text:
            self._log("extractor", "completed", state, start_time=start_time, result_count=0)
            return []
        result = [self._fallback_extract(text)]
        self._log("extractor", "completed", state, start_time=start_time, result_count=len(result))
        return result

    def validate(self, products: list[dict[str, Any]], state: SharedState | None = None) -> list[dict[str, Any]]:
        validated: list[dict[str, Any]] = []
        for item in products:
            model = ExtractedProduct.model_validate(item)
            validated.append(model.model_dump())
        self._log("extractor", "completed", state, start_time=time.perf_counter(), result_count=len(validated))
        return validated

    def _fallback_extract(self, text: str) -> dict[str, Any]:
        lowered = text.lower()
        profit_share_rate = None
        maturity = None
        fees = None
        profit_match = re.search(r"(\d+[.,]\d+|\d+)%?", text)
        if profit_match:
            profit_share_rate = normalize_financial_value(profit_match.group(1))
        maturity_match = re.search(r"(\d+)\s*(ay|month|months)", lowered)
        if maturity_match:
            maturity = int(maturity_match.group(1))
        fee_match = re.search(r"([\w\s]+(?:komisyon|masraf|fee|fees))", lowered)
        if fee_match:
            fees = fee_match.group(1).strip()
        return {
            "product_name": "banking_product",
            "profit_share_rate": profit_share_rate,
            "maturity": maturity,
            "fees": fees,
            "profit_share": profit_share_rate,
            "source_terms": [term for term in ["kÃ¢r payÄ±", "kar payi", "faiz", "vade", "komisyon"] if term in lowered],
        }

    def _log(self, agent_id: str, task_status: str, state: SharedState | None, **extra: Any) -> None:
        self.logger.log(agent_id, task_status, state, **extra)

