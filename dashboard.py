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

import pandas as pd
import streamlit as st

from config import LANG_DICT
from main import BankingAnalysisWorkflow


def get_lang() -> str:
    if "language" not in st.session_state:
        st.session_state.language = "TR"
    return st.session_state.language


def t(key: str) -> str:
    lang = get_lang()
    return LANG_DICT.get(lang, LANG_DICT["TR"]).get(key, key)


def localize_reasoning_text(text: str, lang: str) -> str:
    if not isinstance(text, str):
        return text
    if lang == "TR":
        return (
            text.replace("Highest profit share selected from", "En yÃ¼ksek kÃ¢r payÄ± seÃ§ildi")
            .replace("Lowest fee selected from", "En dÃ¼ÅŸÃ¼k Ã¼cret seÃ§ildi")
            .replace("Longest maturity selected from", "En uzun vade seÃ§ildi")
            .replace("No comparable products were available", "KarÅŸÄ±laÅŸtÄ±rÄ±labilir Ã¼rÃ¼n yok")
            .replace("with profit share", "ile kÃ¢r payÄ±")
            .replace("with fees", "ile Ã¼cret")
            .replace("with maturity", "ile vade")
            .replace("candidate selected from", "adayÄ±ndan seÃ§ildi")
            .replace("at", "de")
            .replace("months", "ay")
        )
    return text


def localize_payload(payload, lang: str):
    if isinstance(payload, dict):
        localized = {}
        for key, value in payload.items():
            if key == "reasoning" and isinstance(value, str):
                localized[key] = localize_reasoning_text(value, lang)
            else:
                localized[key] = localize_payload(value, lang)
        return localized
    if isinstance(payload, list):
        return [localize_payload(item, lang) for item in payload]
    return payload


st.set_page_config(page_title=t("page_title"), page_icon="ğŸ’¼", layout="wide")

with st.sidebar:
    st.header(t("sidebar_title"))
    st.caption(t("sidebar_description"))
    st.selectbox(t("language_label"), ["TR", "EN"], key="language")

st.title(f"{t('page_title')} | {t('page_subtitle')}")
st.caption(t("page_caption"))

workflow = BankingAnalysisWorkflow()

tab1, tab2, tab3 = st.tabs([t("analysis_tab"), t("comparison_tab"), t("terminology_tab")])

with tab1:
    st.subheader(t("analysis_title"))
    campaign_text = st.text_area(t("analysis_text_label"), height=220, placeholder=t("analysis_text_placeholder"))
    if st.button(t("analysis_button"), use_container_width=True):
        if campaign_text.strip():
            result = workflow.run("https://example.com/demo", raw_text=campaign_text)
            localized_result = localize_payload(result, get_lang())
            st.success(t("analysis_complete"))
            st.json(localized_result)
            if localized_result.get("extracted_products"):
                df = pd.DataFrame(localized_result["extracted_products"])
                column_map = {
                    "product_name": t("column_product_name"),
                    "profit_share": t("column_profit_share"),
                    "maturity": t("column_maturity"),
                    "fees": t("column_fees"),
                }
                df = df.rename(columns={col: column_map.get(col, col) for col in df.columns})
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning(t("analysis_warning"))

with tab2:
    st.subheader(t("comparison_title"))
    left_text = st.text_area(t("comparison_left_label"), height=180, key="left_campaign")
    right_text = st.text_area(t("comparison_right_label"), height=180, key="right_campaign")
    if st.button(t("comparison_button"), use_container_width=True):
        if left_text.strip() and right_text.strip():
            left_result = workflow.run("https://example.com/demo/left", raw_text=left_text)
            right_result = workflow.run("https://example.com/demo/right", raw_text=right_text)
            localized_left = localize_payload(left_result, get_lang())
            localized_right = localize_payload(right_result, get_lang())
            comparison_payload = {
                t("comparison_first_campaign"): localized_left,
                t("comparison_second_campaign"): localized_right,
                t("comparison_reasoning_label"): (
                    f"{t('comparison_first_campaign')}: {localized_left.get('comparison', {}).get('reasoning', 'n/a')}\n"
                    f"{t('comparison_second_campaign')}: {localized_right.get('comparison', {}).get('reasoning', 'n/a')}"
                ),
            }
            st.success(t("comparison_complete"))
            st.json(comparison_payload)
        else:
            st.warning(t("comparison_warning"))

with tab3:
    st.subheader(t("terminology_title"))
    st.info(t("terminology_info"))
    control_text = st.text_area(t("terminology_text_label"), height=220, placeholder=t("terminology_text_placeholder"))
    if st.button(t("terminology_button"), use_container_width=True):
        if control_text.strip():
            preview_result = workflow.run("https://example.com/demo/control", raw_text=control_text)
            localized_result = localize_payload(preview_result, get_lang())
            if localized_result.get("validation_rejected"):
                st.error(t("status_violation"))
            else:
                st.success(t("status_valid"))
            st.json(localized_result)
        else:
            st.warning(t("terminology_warning"))

