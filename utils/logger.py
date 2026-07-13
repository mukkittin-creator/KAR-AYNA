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

import json
import time
from datetime import datetime, timezone
from typing import Any


class StructuredLogger:
    """Outputs structured JSON logs for agent execution."""

    def log(self, agent_id: str, task_status: str, state: Any | None = None, **extra: Any) -> dict[str, Any]:
        start_time = extra.pop("start_time", None)
        processing_time = None
        if start_time is not None:
            processing_time = round(time.perf_counter() - start_time, 4)

        record: dict[str, Any] = {
            "Timestamp": datetime.now(timezone.utc).isoformat(),
            "AgentID": agent_id,
            "TaskStatus": task_status,
            "ProcessingTime": processing_time if processing_time is not None else 0.0,
        }
        record.update(extra)

        if state is not None and hasattr(state, "add_log"):
            state.add_log(record)

        print(json.dumps(record, ensure_ascii=False))
        return record

