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

from typing import Any

from agents.classifier import ClassifierAgent
from agents.comparator import ComparatorAgent
from agents.extractor import ExtractorAgent
from agents.validator import ValidatorAgent
from utils.scraper import Scraper
from utils.state import SharedState

try:
    from langgraph.graph import END, START, StateGraph
except ImportError:
    END = "END"
    START = "START"

    class StateGraph:
        def __init__(self, state_type: type[SharedState]) -> None:
            self.state_type = state_type
            self.nodes: dict[str, Any] = {}
            self.edges: list[tuple[str, str]] = []
            self.conditional_edges: list[tuple[str, Any, dict[str, str]]] = []

        def add_node(self, name: str, action: Any) -> None:
            self.nodes[name] = action

        def add_edge(self, source: str, target: str) -> None:
            self.edges.append((source, target))

        def add_conditional_edges(self, source: str, condition: Any, mapping: dict[str, str]) -> None:
            self.conditional_edges.append((source, condition, mapping))

        def compile(self) -> "CompiledGraph":
            return CompiledGraph(self)

    class CompiledGraph:
        def __init__(self, graph: StateGraph) -> None:
            self.graph = graph

        def invoke(self, state: SharedState) -> SharedState:
            current = "scraper"
            while True:
                if current in self.graph.nodes:
                    state = self.graph.nodes[current](state)
                if current == "validator":
                    for source, condition, mapping in self.graph.conditional_edges:
                        if source == current:
                            decision = condition(state)
                            target = mapping.get(decision, END)
                            if target == END:
                                return state
                            current = target
                            break
                    else:
                        return state
                else:
                    next_node = next((target for source, target in self.graph.edges if source == current), None)
                    if next_node is None:
                        return state
                    current = next_node


class BankingAnalysisWorkflow:
    def __init__(self) -> None:
        self.scraper = Scraper()
        self.classifier = ClassifierAgent()
        self.extractor = ExtractorAgent()
        self.validator = ValidatorAgent()
        self.comparator = ComparatorAgent()

    def _scraper_node(self, state: SharedState) -> SharedState:
        if not state.raw_text:
            state.raw_text = self.scraper.fetch(state.source_url)
        return state

    def _classifier_node(self, state: SharedState) -> SharedState:
        state.campaign_type = self.classifier.classify(state.raw_text, state=state)
        return state

    def _extractor_node(self, state: SharedState) -> SharedState:
        state.extracted_products = self.extractor.extract(state.raw_text, campaign_type=state.campaign_type, state=state)
        return state

    def _validator_node(self, state: SharedState) -> SharedState:
        state.validated_products = self.validator.validate(state.extracted_products, state=state)
        return state

    def _comparator_node(self, state: SharedState) -> SharedState:
        state.comparison = self.comparator.compare(state.validated_products, state=state)
        return state

    def _route_after_validator(self, state: SharedState) -> str:
        if state.validation_rejected or any(log.get("TaskStatus") == "rejected" for log in state.logs):
            return "end"
        return "continue"

    def run(self, source_url: str, raw_text: str | None = None) -> dict[str, Any]:
        state = SharedState(source_url=source_url)
        if raw_text is not None:
            state.raw_text = raw_text
        graph = self.build_graph()
        result_state = graph.invoke(state)
        return {
            "source_url": source_url,
            "campaign_type": result_state.campaign_type,
            "extracted_products": result_state.validated_products,
            "comparison": result_state.comparison,
            "logs": result_state.logs,
            "validation_rejected": result_state.validation_rejected,
            "rejection_reason": result_state.rejection_reason,
        }

    def build_graph(self) -> Any:
        workflow = StateGraph(SharedState)
        workflow.add_node("scraper", self._scraper_node)
        workflow.add_node("classifier", self._classifier_node)
        workflow.add_node("extractor", self._extractor_node)
        workflow.add_node("validator", self._validator_node)
        workflow.add_node("comparator", self._comparator_node)
        workflow.add_edge(START, "scraper")
        workflow.add_edge("scraper", "classifier")
        workflow.add_edge("classifier", "extractor")
        workflow.add_edge("extractor", "validator")
        workflow.add_conditional_edges("validator", self._route_after_validator, {"end": END, "continue": "comparator"})
        workflow.add_edge("comparator", END)
        return workflow.compile()


if __name__ == "__main__":
    workflow = BankingAnalysisWorkflow()
    result = workflow.run("https://example.com/banking-offer")
    print(result)

