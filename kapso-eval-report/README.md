# KAPSO SynthesisEvalReport — worked example (1 Oct 2026)

Standalone prototype answering [Leeroo-AI/kapso#92](https://github.com/Leeroo-AI/kapso/issues/92):
after synthesis, how do we know a program is *actually* better than baseline — not just better on the search set?

## What this is

A stdlib-only `SynthesisEvalReport` plus scoring helpers:

| Signal | What it catches |
|--------|-----------------|
| `grounding_score` | Citations that were never retrieved / hallucinated |
| `generalization_score` | Held-out vs in-search collapse (search overfit) |
| `composition_validity` | Incompatible technique pairs |
| `compute_ratio` | Accuracy bought with 10x FLOPs |
| `flagged_issues` | Machine-readable reject reasons |
| `trust_to_deploy()` | Conservative gate before shipping a candidate |

## Run

```bash
python3 synthesis_eval_report.py
```

Prints self-check, then a GOOD vs FRAGILE campaign side-by-side.

## Why this shape

Issue #92 proposed the dataclass. This file makes it executable with a tiny
tabular-churn style worked example (MLE-Bench flavoured), so a reviewer can
see deploy-vs-reject without wiring the full Kapso campaign loop.

Intended next step on a writable fork: drop `SynthesisEvalReport` next to
campaign outputs and emit one JSON report per leaf. This gist/prototype is
the proof packet while fork/`gh` write path for `Leeroo-AI/kapso` is still blocked.

## Author

Rahul Yadav — github.com/rahulyyadav — for Leeroo / Kapso follow-up after
Alireza pointed at github.com/Leeroo-AI/kapso.
