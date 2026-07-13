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

from dataclasses import dataclass


@dataclass
class Settings:
    enable_local_llm: bool = False
    local_llm_endpoint: str = "http://127.0.0.1:11434/v1"
    local_model: str = "phi3"
    local_llm_api_key: str = "local"


settings = Settings()

LANG_DICT = {
    "TR": {
        "page_title": "KÃ‚R-AYNA",
        "page_subtitle": "Kampanya Analiz Platformu",
        "page_caption": "On-premise, ÅŸeffaf ve kurallÄ± banka kampanya analizi",
        "sidebar_title": "Dil SeÃ§imi",
        "sidebar_description": "ArayÃ¼zÃ¼ TÃ¼rkÃ§e veya Ä°ngilizce gÃ¶rÃ¼ntÃ¼leyin.",
        "language_label": "Dil",
        "analysis_tab": "Metin Analiz",
        "comparison_tab": "KarÅŸÄ±laÅŸtÄ±rma",
        "terminology_tab": "Terminoloji Kontrol",
        "analysis_title": "Metin Analiz",
        "analysis_text_label": "Kampanya Metni",
        "analysis_text_placeholder": "Kampanya metnini buraya yapÄ±ÅŸtÄ±rÄ±n...",
        "analysis_button": "Analiz Et",
        "analysis_complete": "Analiz tamamlandÄ±",
        "analysis_warning": "LÃ¼tfen bir kampanya metni girin.",
        "comparison_title": "KarÅŸÄ±laÅŸtÄ±rma",
        "comparison_left_label": "Birinci Kampanya Metni",
        "comparison_right_label": "Ä°kinci Kampanya Metni",
        "comparison_button": "KarÅŸÄ±laÅŸtÄ±r",
        "comparison_complete": "KarÅŸÄ±laÅŸtÄ±rma tamamlandÄ±",
        "comparison_warning": "Her iki kampanya metnini de girin.",
        "terminology_title": "Terminoloji Kontrol",
        "terminology_info": "Bu panel, kampanya metinlerinin yasaklÄ± terim iÃ§eriÄŸini kontrol eder.",
        "terminology_text_label": "Kontrol Edilecek Metin",
        "terminology_text_placeholder": "Kontrol etmek iÃ§in metin girin...",
        "terminology_button": "Kontrol Et",
        "terminology_warning": "LÃ¼tfen bir metin girin.",
        "status_valid": "RegÃ¼lasyon Durumu: GeÃ§erli",
        "status_violation": "RegÃ¼lasyon Durumu: Terminology Violation",
        "comparison_reasoning_label": "AÃ§Ä±klama",
        "comparison_first_campaign": "Birinci Kampanya",
        "comparison_second_campaign": "Ä°kinci Kampanya",
        "column_product_name": "ÃœrÃ¼n AdÄ±",
        "column_profit_share": "KÃ¢r PayÄ±",
        "column_maturity": "Vade",
        "column_fees": "Ãœcretler",
    },
    "EN": {
        "page_title": "KÃ‚R-AYNA",
        "page_subtitle": "Campaign Analysis Platform",
        "page_caption": "On-premise, transparent, and rule-based banking campaign analysis",
        "sidebar_title": "Language",
        "sidebar_description": "Switch the interface between Turkish and English.",
        "language_label": "Language",
        "analysis_tab": "Text Analysis",
        "comparison_tab": "Comparison",
        "terminology_tab": "Terminology Control",
        "analysis_title": "Text Analysis",
        "analysis_text_label": "Campaign Text",
        "analysis_text_placeholder": "Paste a campaign text here...",
        "analysis_button": "Analyze",
        "analysis_complete": "Analysis completed",
        "analysis_warning": "Please enter a campaign text.",
        "comparison_title": "Comparison",
        "comparison_left_label": "First Campaign Text",
        "comparison_right_label": "Second Campaign Text",
        "comparison_button": "Compare",
        "comparison_complete": "Comparison completed",
        "comparison_warning": "Please enter both campaign texts.",
        "terminology_title": "Terminology Control",
        "terminology_info": "This panel checks campaign texts for forbidden terminology.",
        "terminology_text_label": "Text to Check",
        "terminology_text_placeholder": "Enter text to inspect...",
        "terminology_button": "Check",
        "terminology_warning": "Please enter text to inspect.",
        "status_valid": "Regulation Status: Valid",
        "status_violation": "Regulation Status: Terminology Violation",
        "comparison_reasoning_label": "Reasoning",
        "comparison_first_campaign": "First Campaign",
        "comparison_second_campaign": "Second Campaign",
        "column_product_name": "Product Name",
        "column_profit_share": "Profit Share",
        "column_maturity": "Maturity",
        "column_fees": "Fees",
    },
}

