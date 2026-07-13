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

from utils.logger import StructuredLogger
from utils.state import SharedState


class ClassifierAgent:
    """Classifies campaign copy as Finansman or YatÄ±rÄ±m with lightweight heuristics."""

    def __init__(self) -> None:
        self.logger = StructuredLogger()

    def classify(self, text: str, state: SharedState | None = None) -> str:
        start_time = time.perf_counter()
        paragraph = (text or "").lower()
        if re.search(r"(yatÄ±rÄ±m|yatirim|depo|portfolio|portfÃ¶y|kar payÄ±|kÃ¢r payÄ±)", paragraph):
            category = "YatÄ±rÄ±m"
        else:
            category = "Finansman"
        self.logger.log("classifier", "completed", state, start_time=start_time, category=category)
        return category

