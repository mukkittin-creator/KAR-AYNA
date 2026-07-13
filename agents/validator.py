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
from utils.state import SharedState


class ValidationResult(BaseModel):
    """Minimal validation model for extracted banking offers."""

    product_name: str = Field(default="")
    profit_share_rate: float | None = None
    maturity: int | None = None
    fees: str | None = None
    source_terms: list[str] = Field(default_factory=list)


class ValidatorAgent:
    """Enforces Participatory Banking terminology and halts the workflow on policy violations."""

    def __init__(self) -> None:
        self.logger = StructuredLogger()

    def validate(self, products: list[dict[str, Any]], state: SharedState | None = None) -> list[dict[str, Any]]:
        start_time = time.perf_counter()
        if not products:
            self.logger.log("validator", "completed", state, start_time=start_time, result_count=0)
            return []
        source_text = (state.raw_text if state is not None else "")
        validated: list[dict[str, Any]] = []
        for product in products:
            combined_text = " ".join([source_text, str(product.get("text", "")), str(product.get("product_name", "")), str(product.get("fees", ""))])
            if self._contains_violating_terms(combined_text):
                if state is not None:
                    state.validation_rejected = True
                    state.rejection_reason = "Terminology Violation"
                    state.errors.append("Terminology Violation")
                self.logger.log("validator", "rejected", state, start_time=start_time, reason="Terminology Violation")
                return []
            model = ValidationResult.model_validate(product)
            validated.append(model.model_dump())
        self.logger.log("validator", "completed", state, start_time=start_time, result_count=len(validated))
        return validated

    def _contains_violating_terms(self, text: str) -> bool:
        lowered = (text or "").lower()
        return bool(re.search(r"\b(faiz|kredi)\b", lowered))

