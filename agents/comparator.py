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

import time
from typing import Any

from utils.logger import StructuredLogger
from utils.normalizer import normalize_financial_value
from utils.state import SharedState


class ComparatorAgent:
    """Compares extracted product candidates and returns an explainable advantage analysis."""

    def __init__(self) -> None:
        self.logger = StructuredLogger()

    def compare(self, products: list[dict[str, Any]], state: SharedState | None = None) -> dict[str, Any]:
        start_time = time.perf_counter()
        normalized = []
        for product in products:
            normalized.append({
                "product_name": product.get("product_name", "unknown"),
                "profit_share_rate": normalize_financial_value(product.get("profit_share_rate") or product.get("profit_share")),
                "maturity": product.get("maturity"),
                "fees": product.get("fees"),
            })
        ranked = sorted(normalized, key=lambda item: (-(item["profit_share_rate"] or 0), str(item["fees"] or ""), -(item["maturity"] or 0)))
        best = ranked[0] if ranked else None
        lowest_fee = min(normalized, key=lambda item: (item["fees"] is None, str(item["fees"] or ""))) if normalized else None
        longest_maturity = max(normalized, key=lambda item: item["maturity"] or 0) if normalized else None
        result = {
            "best_profit_share": best,
            "lowest_fee": lowest_fee,
            "longest_maturity": longest_maturity,
            "ranked_products": ranked,
            "reasoning": self._build_reasoning(best, lowest_fee, longest_maturity),
        }
        self.logger.log("comparator", "completed", state, start_time=start_time, product_count=len(normalized))
        return result

    def compare_outputs(self, left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
        left_score = left.get("profit_share_rate") or left.get("profit_share") or 0
        right_score = right.get("profit_share_rate") or right.get("profit_share") or 0
        if left_score > right_score:
            winner = "left"
            reasoning = f"Left output has the stronger profit share rate at {left_score}%."
        elif right_score > left_score:
            winner = "right"
            reasoning = f"Right output has the stronger profit share rate at {right_score}%."
        else:
            winner = "tie"
            reasoning = "Both outputs present comparable profit share rates."
        return {"winner": winner, "reasoning": reasoning}

    def _build_reasoning(self, best: dict[str, Any] | None, lowest_fee: dict[str, Any] | None, longest_maturity: dict[str, Any] | None) -> str:
        fragments: list[str] = []
        if best:
            fragments.append(f"Highest profit-share candidate selected from '{best.get('product_name', 'unknown')}' at {best.get('profit_share_rate')}.")
        if lowest_fee:
            fragments.append(f"Lowest fee candidate selected from '{lowest_fee.get('product_name', 'unknown')}' with fees '{lowest_fee.get('fees')}'.")
        if longest_maturity:
            fragments.append(f"Longest maturity selected from '{longest_maturity.get('product_name', 'unknown')}' at {longest_maturity.get('maturity')} months.")
        if not fragments:
            fragments.append("No comparable products were available.")
        return " | ".join(fragments)

