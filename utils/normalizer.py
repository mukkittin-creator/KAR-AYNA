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
from typing import Any

CURRENCY_ALIASES = {
    "Å": "TL",
    "â‚º": "TL",
    "TL": "TL",
    "tÃ¼rk lirasÄ±": "TL",
    "turk lirasÄ±": "TL",
    "tÃ¼rk lira": "TL",
    "turk lira": "TL",
}


def normalize_currency(value: str | None) -> str:
    """Normalize currency aliases to a standard TL token."""
    if not value:
        return "TL"
    text = value.strip().lower()
    for alias, normalized in CURRENCY_ALIASES.items():
        if alias.lower() in text:
            return normalized
    return "TL"


def normalize_financial_value(value: Any) -> float | None:
    """Normalize common financial text such as '%2,05', '2.05%', '2,05', 'Å2,05' to a float."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if hasattr(value, "group") and callable(value.group):
        value = value.group(0)
    if not isinstance(value, str):
        value = str(value)
    text = value.strip()
    if not text:
        return None
    text = text.replace("%", "")
    text = text.replace(" ", "")
    text = text.replace("â‚º", "TL")
    text = text.replace("Å", "TL")
    text = text.replace("TÃ¼rkLirasÄ±", "TL")
    text = text.replace("TÃ¼rkLira", "TL")
    text = text.replace("TÃ¼rk LirasÄ±", "TL")
    text = text.replace("Turk Lirasi", "TL")
    text = text.replace("Turk Lira", "TL")
    match = re.search(r"[-+]?(?:\d{1,3}(?:[.,]\d{3})+|\d+)(?:[.,]\d+)?", text)
    if not match:
        return None
    numeric = match.group(0)
    numeric = numeric.replace(".", "") if "," in numeric and "." in numeric else numeric
    if "," in numeric:
        numeric = numeric.replace(",", ".")
    try:
        return float(numeric)
    except ValueError:
        return None

