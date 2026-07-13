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
from pathlib import Path

from main import BankingAnalysisWorkflow


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    data_dir = Path(__file__).resolve().parent / "data"
    workflow = BankingAnalysisWorkflow()

    valid_payload = load_json(data_dir / "valid_campaign.json")
    valid_result = workflow.run(valid_payload["source_url"], raw_text=valid_payload["text"])
    print("VALID CASE")
    print(json.dumps(valid_result, ensure_ascii=False, indent=2))

    invalid_payload = load_json(data_dir / "invalid_campaign.json")
    invalid_result = workflow.run(invalid_payload["source_url"], raw_text=invalid_payload["text"])
    print("\nINVALID CASE")
    print(json.dumps(invalid_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

