"""KAPSO-oriented SynthesisEvalReport (worked example for Leeroo-AI/kapso#92).

Standalone stdlib-only prototype. Drop-in shape for synthesis outputs so a
campaign can trust (or reject) a candidate beyond black-box task score.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable, Mapping, Sequence
import json
import math


@dataclass
class SynthesisEvalReport:
    task_id: str
    baseline_score: float
    synthesized_score: float
    improvement_delta: float

    grounding_score: float  # 0-1
    generalization_score: float  # held-out / in-search ratio, clipped 0-1
    composition_validity: bool
    compute_ratio: float  # synthesized_flops / baseline_flops

    flagged_issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def trust_to_deploy(self, *, min_delta: float = 0.0, min_grounding: float = 0.55) -> bool:
        """Conservative gate: improve, stay grounded, don't silently explode compute."""
        if self.improvement_delta < min_delta:
            return False
        if self.grounding_score < min_grounding:
            return False
        if not self.composition_validity:
            return False
        if "efficiency_regression" in self.flagged_issues and self.compute_ratio > 5.0:
            return False
        if "grounding_gap" in self.flagged_issues:
            return False
        return True


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def grounding_from_citations(
    retrieved_ids: Sequence[str],
    cited_ids: Sequence[str],
    *,
    hallucinated_ids: Sequence[str] = (),
) -> float:
    """Fraction of cited knowledge that was actually retrieved, minus hallucinations."""
    if not cited_ids:
        return 0.0
    retrieved = set(retrieved_ids)
    cited = list(cited_ids)
    grounded = sum(1 for c in cited if c in retrieved)
    base = grounded / len(cited)
    penalty = len(hallucinated_ids) / max(1, len(cited))
    return _clamp01(base - penalty)


def generalization_from_scores(in_search: float, held_out: float) -> float:
    """Held-out relative to in-search. 1.0 = no overfitting; <1 = search-set overfit."""
    if in_search <= 0:
        return 0.0
    return _clamp01(held_out / in_search)


def composition_ok(
    technique_ids: Sequence[str],
    incompatibilities: Mapping[str, Iterable[str]],
) -> bool:
    """False if any selected technique pair is marked incompatible."""
    selected = set(technique_ids)
    for a in selected:
        banned = set(incompatibilities.get(a, ()))
        if selected & banned:
            return False
    return True


def build_report(
    *,
    task_id: str,
    baseline_score: float,
    synthesized_score: float,
    retrieved_ids: Sequence[str],
    cited_ids: Sequence[str],
    hallucinated_ids: Sequence[str],
    in_search_score: float,
    held_out_score: float,
    technique_ids: Sequence[str],
    incompatibilities: Mapping[str, Iterable[str]],
    baseline_flops: float,
    synthesized_flops: float,
) -> SynthesisEvalReport:
    delta = synthesized_score - baseline_score
    g = grounding_from_citations(retrieved_ids, cited_ids, hallucinated_ids=hallucinated_ids)
    gen = generalization_from_scores(in_search_score, held_out_score)
    ok = composition_ok(technique_ids, incompatibilities)
    compute_ratio = (
        math.inf if baseline_flops <= 0 else synthesized_flops / baseline_flops
    )

    flags: list[str] = []
    if g < 0.55:
        flags.append("grounding_gap")
    if gen < 0.85:
        flags.append("search_overfit")
    if not ok:
        flags.append("composition_invalid")
    if compute_ratio > 3.0 and delta < 0.05:
        flags.append("efficiency_regression")
    if delta <= 0:
        flags.append("no_improvement")

    return SynthesisEvalReport(
        task_id=task_id,
        baseline_score=baseline_score,
        synthesized_score=synthesized_score,
        improvement_delta=delta,
        grounding_score=round(g, 4),
        generalization_score=round(gen, 4),
        composition_validity=ok,
        compute_ratio=round(compute_ratio, 4) if compute_ratio != math.inf else float("inf"),
        flagged_issues=flags,
    )


def demo() -> None:
    """Two campaigns: one deployable, one fragile (overfit + compute blow-up)."""
    incompat = {
        "label_smoothing": ("hard_label_mixup",),
        "hard_label_mixup": ("label_smoothing",),
    }

    good = build_report(
        task_id="mle-bench/tabular-churn-v1",
        baseline_score=0.742,
        synthesized_score=0.781,
        retrieved_ids=["wiki:catboost-defaults", "wiki:target-encoding", "paper:ariosky2021"],
        cited_ids=["wiki:catboost-defaults", "wiki:target-encoding"],
        hallucinated_ids=[],
        in_search_score=0.788,
        held_out_score=0.781,
        technique_ids=["catboost", "target_encoding"],
        incompatibilities=incompat,
        baseline_flops=1.2e9,
        synthesized_flops=1.5e9,
    )

    bad = build_report(
        task_id="mle-bench/tabular-churn-v1",
        baseline_score=0.742,
        synthesized_score=0.790,
        retrieved_ids=["wiki:catboost-defaults"],
        cited_ids=["wiki:catboost-defaults", "paper:fake-ensemble-2024", "wiki:never-retrieved"],
        hallucinated_ids=["paper:fake-ensemble-2024"],
        in_search_score=0.910,
        held_out_score=0.690,
        technique_ids=["label_smoothing", "hard_label_mixup"],
        incompatibilities=incompat,
        baseline_flops=1.2e9,
        synthesized_flops=18.0e9,
    )

    print("=== GOOD candidate (should trust_to_deploy=True) ===")
    print(json.dumps(good.to_dict(), indent=2))
    print("trust_to_deploy:", good.trust_to_deploy())
    print()
    print("=== FRAGILE candidate (should trust_to_deploy=False) ===")
    print(json.dumps(bad.to_dict(), indent=2))
    print("trust_to_deploy:", bad.trust_to_deploy())


def _self_check() -> None:
    incompat = {"a": ("b",), "b": ("a",)}
    r = build_report(
        task_id="t",
        baseline_score=0.5,
        synthesized_score=0.6,
        retrieved_ids=["k1", "k2"],
        cited_ids=["k1", "k2"],
        hallucinated_ids=[],
        in_search_score=0.62,
        held_out_score=0.60,
        technique_ids=["a"],
        incompatibilities=incompat,
        baseline_flops=10.0,
        synthesized_flops=12.0,
    )
    assert r.trust_to_deploy(), r
    assert r.grounding_score == 1.0
    assert "grounding_gap" not in r.flagged_issues
    bad = build_report(
        task_id="t",
        baseline_score=0.5,
        synthesized_score=0.55,
        retrieved_ids=["k1"],
        cited_ids=["k1", "halluc"],
        hallucinated_ids=["halluc"],
        in_search_score=0.9,
        held_out_score=0.5,
        technique_ids=["a", "b"],
        incompatibilities=incompat,
        baseline_flops=10.0,
        synthesized_flops=100.0,
    )
    assert not bad.trust_to_deploy(), bad
    assert "grounding_gap" in bad.flagged_issues
    assert "composition_invalid" in bad.flagged_issues
    print("self_check: OK")


if __name__ == "__main__":
    _self_check()
    demo()
