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


def write_campaigns(data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    campaigns = {
        "perfect_kar_payi_campaign.json": {
            "name": "perfect_kar_payi_campaign",
            "source_url": "https://demo.local/kar-payi",
            "text": "KatÄ±lÄ±m bankasÄ± Ã¼rÃ¼nÃ¼nde %2,05 kÃ¢r payÄ± sunulmaktadÄ±r. Vade 12 ay, komisyon oranÄ± 0,50 TL olarak belirtilmiÅŸtir.",
        },
        "faiz_trap_campaign.json": {
            "name": "faiz_trap_campaign",
            "source_url": "https://demo.local/faiz-trap",
            "text": "Bu kampanya faiz ve kredi tabanlÄ± bir teklif olarak hazÄ±rlanmÄ±ÅŸtÄ±r; mevzuata uygun olmayan iÃ§erik barÄ±ndÄ±rmaktadÄ±r.",
        },
        "empty_invalid_campaign.json": {
            "name": "empty_invalid_campaign",
            "source_url": "https://demo.local/empty",
            "text": "",
        },
    }
    for filename, payload in campaigns.items():
        with (data_dir / filename).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)


def run_suite() -> None:
    data_dir = Path(__file__).resolve().parent / "data"
    write_campaigns(data_dir)
    workflow = BankingAnalysisWorkflow()
    for filename in ["perfect_kar_payi_campaign.json", "faiz_trap_campaign.json", "empty_invalid_campaign.json"]:
        payload = json.loads((data_dir / filename).read_text(encoding="utf-8"))
        result = workflow.run(payload["source_url"], raw_text=payload["text"])
        print(f"=== {payload['name']} ===")
        print(json.dumps({
            "name": payload["name"],
            "validation_rejected": result.get("validation_rejected"),
            "rejection_reason": result.get("rejection_reason"),
            "campaign_type": result.get("campaign_type"),
            "extracted_products": result.get("extracted_products"),
            "comparison": result.get("comparison"),
        }, ensure_ascii=False, indent=2))
        print()


if __name__ == "__main__":
    run_suite()

