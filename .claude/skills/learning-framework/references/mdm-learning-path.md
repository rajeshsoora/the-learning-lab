# MDM / Spark / Entity Resolution — Learning Path

> Living reference for Rajesh's curriculum, broken into ordered modules across 4 phases.
> The live, canonical progress tracker is **roadmap.html** on the site. This file mirrors it for version control.
> Frame (locked): Why=build · Anchor=MDM/PySpark ER pipeline · Angle=mechanistic+table-driven · Depth=use · Budget≈45min/session.

## Status legend
- ✅ done · 🟡 partial (tail parked) · 🔜 up next · ⬜ locked

---

## Progress snapshot (as of 2026-06-19) — 5 / 10 complete (50%)

### Phase 1 — Spark Foundations ✅
- ✅ **00** Entity Resolution Overview — `entity-resolution-walkthrough.html`
- ✅ **01** Complex Types & Nested Data — `nested-types-decision-card.html`
- ✅ **02** String Processing & Normalization — `string-processing-normalization.html`
- ✅ **03** Window Functions — `window-functions.html`

### Phase 2 — The ER Algorithms
- ✅ **04** Match Scoring & Classification — `match-scoring-classification.html` *(built 2026-06-19)*
- 🔜 **05** Score Aggregation & Confidence — up next

### Phase 3 — ER at Scale
- ⬜ **06** LSH & MinHash
- ⬜ **07** Graph Theory & Clustering

### Phase 4 — Pipeline Mastery (Capstone)
- ⬜ **08** Spark Performance (Remaining Levers)
- ⬜ **09** Pipeline Design (Capstone)

---

## Module 04 — what was covered (built 2026-06-19)
9-stage flow-module-builder treatment, matching the Module 03 style.
- **Stage 01** Why a flat average breaks — two distinct pairs (same-household vs moved-person) that average identically; the corruption argument.
- **Stage 02** Field weighting — courtroom/DNA analogy; the **"raw score is a red herring; discriminating power decides"** contrast (Rajesh's signature fix); shippable weight table; weights as YAML config.
- **Stage 03** Composite score — Σ(sim×weight); worked contribution table + accumulating debug trace; weighted-sum = weighted-average when weights sum to 1.
- **Stage 04** Null handling (the climax) — disagreement (0.0, stays in denominator) vs absence (null, drops from both); the **"they look the same in the numerator; the denominator decides"** red-herring contrast; verdict-flips-on-renormalization worked example; wrong vs right scorer with output.
- **Stage 05** Thresholds — three bands (match/review/no-match); classify ladder; precision↔recall lever (forward-link to Mod 05).
- **Stage 06** Full PySpark ScoringPlugin pattern — `F.when(present, ...)` as the column-wise null guard; num/den accumulators; config-vs-logic separation.
- **Stage 07** Interactive Score Builder — live sliders + absent toggles, renormalizing math readout, 4 presets (household trap, moved person, absent SSN, reset).
- **Stage 08** Self-test — 8 scenario-recognition questions (the format that re-energizes Rajesh).

## Parked / for later
- Nothing parked from Module 04.
- Module 05 should open by reusing the Stage 05 precision/recall lever and turning the two thresholds into something tuned against labeled data + review-queue size.

## Calibration notes that held this session
- Table-driven teaching throughout (every mechanism has a worked table).
- "X is a red herring; Y decides" + side-by-side contrast used twice (weighting, null handling) — the core misconception-repair device.
- Every code block shows its output; wrong→right pairs always show both outputs.
- Depth = use: all examples point at his real ScoringPlugin / YAML config shape.
