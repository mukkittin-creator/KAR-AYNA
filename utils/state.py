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

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SharedState:
    """Central state object for LangGraph-style agent orchestration."""

    source_url: str = ""
    raw_text: str = ""
    campaign_type: str = "general_banking_offer"
    extracted_products: list[dict[str, Any]] = field(default_factory=list)
    validated_products: list[dict[str, Any]] = field(default_factory=list)
    comparison: dict[str, Any] | None = None
    errors: list[str] = field(default_factory=list)
    logs: list[dict[str, Any]] = field(default_factory=list)
    validation_rejected: bool = False
    rejection_reason: str | None = None

    def add_log(self, record: dict[str, Any]) -> None:
        self.logs.append(record)

