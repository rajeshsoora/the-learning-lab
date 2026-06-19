# MDM / Spark / Entity Resolution — Learning Path

> Living reference for Rajesh's curriculum, broken into ordered modules across 4 phases.
> The live, canonical progress tracker is **roadmap.html** on the site. This file mirrors it for version control — kept in sync with roadmap.html's `PHASES` data.
> Frame (locked): Why=build · Anchor=MDM/PySpark ER pipeline · Angle=mechanistic+table-driven · Depth=use · Budget≈45min/session.

## Status legend
- ✅ done · 🔜 up next · ⬜ locked

---

## Progress snapshot (as of 2026-06-19) — 5 / 9 modules complete

### Phase 1 — Spark Foundations  (~2–2.5 sessions) ✅
- ✅ **00 — Entity Resolution Overview** — `entity-resolution-walkthrough.html`
  - Topics: blocking, shuffle, self-join, skew
  - Unlocks: the full pipeline traced end to end — standardize → block → shuffle → self-join → score → skew.
- ✅ **01 — Complex Types & Nested Data** — `nested-types-decision-card.html`
  - Topics: arrays, structs, maps, explode
  - Unlocks: read and write the nested entity structures the MDM pipeline actually stores.
- ✅ **02 — String Processing & Normalization** — `string-processing-normalization.html`
  - Topics: jaro-winkler, levenshtein, soundex, normalization
  - Unlocks: know what StandardizationPlugin should normalize and exactly why each rule exists.
- ✅ **03 — Window Functions** — `window-functions.html`
  - Topics: row_number, rank, lag, dedup
  - Unlocks: assign row numbers, pick latest record per entity, build golden record selection.

### Phase 2 — The ER Algorithms  (~2 sessions)
- ✅ **04 — Match Scoring & Classification** — `match-scoring-classification.html` *(built 2026-06-19)*
  - Topics: field weighting, composite scores, thresholds, null handling
  - Unlocks: combine per-field similarity scores into a single match/review/no-match verdict — the heart of the ScoringPlugin.
- 🔜 **05 — Score Aggregation & Confidence** — up next (~1 session)
  - Topics: weighted aggregation, confidence bands, review queues, precision vs recall
  - Unlocks: tune the thresholds that decide which pairs auto-merge, which go to human review, and which are rejected.

### Phase 3 — ER at Scale  (~2 sessions)
- ⬜ **06 — LSH & MinHash** (~1 session)
  - Topics: minhash, banding, jaccard, candidate generation
  - Unlocks: find candidate pairs at scale without all-pairs comparison — approximate blocking that complements the self-join.
- ⬜ **07 — Graph Theory & Clustering** (~1 session)
  - Topics: connected components, union-find, BFS/DFS, transitive matches
  - Unlocks: how matched pairs merge into one master entity — the final ER step that turns pairs into clusters.

### Phase 4 — Pipeline Mastery (Capstone)  (~2 sessions)
- ⬜ **08 — Spark Performance (Remaining Levers)** (~1 session)
  - Topics: column pruning, predicate pushdown, memory tuning, partition sizing
  - Unlocks: optimize the full pipeline beyond shuffle/join/skew.
- ⬜ **09 — Pipeline Design (Capstone)** (~1 session)
  - Topics: join-back strategies, enrichment, intermediate datasets, YAML plugin arch
  - Unlocks: design the full MDM entity resolution architecture end to end with confidence.

---

## Why this order (from roadmap.html)
- **01 before 04:** can't score strings without first knowing how strings are processed and stored. Nested types and normalization come before the scoring algorithms that consume them.
- **03 in Phase 1, not Phase 2:** window functions are Spark mechanics, not entity-resolution concepts — finish the toolkit before touching scoring.
- **06 (LSH) before 07 (graph):** LSH produces another stream of candidate pairs; graph clustering consumes ALL pairs (blocking + LSH) and merges them into entities, so LSH must come first.
- **09 last (capstone):** needs vocabulary from every prior module to reason about each architectural decision — which joins to broadcast, where shuffles live, how LSH integrates with blocking.

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
- Nothing parked from Module 04 itself.
- Module 05 should open by reusing the Stage 05 precision/recall lever and turning the two thresholds into something tuned against labeled data + review-queue size.
- **Carried from an earlier Module 01 planning note (not confirmed resolved on the live site):** null handling inside arrays · schema evolution mechanics (Delta `mergeSchema`) · array-of-structs (the real MDM shape) · `transform`/`inline`. Worth a 15-min warm-up check next time nested-data content resurfaces, to confirm these were actually covered.

## Calibration notes that held this session
- Table-driven teaching throughout (every mechanism has a worked table).
- "X is a red herring; Y decides" + side-by-side contrast used twice (weighting, null handling) — the core misconception-repair device.
- Every code block shows its output; wrong→right pairs always show both outputs.
- Depth = use: all examples point at his real ScoringPlugin / YAML config shape.

---

## Supplementary planning notes (from original 2026-06-18 curriculum draft, not on the live site)

Retained for course-design reference only — not confirmed against roadmap.html, so treat as planning context rather than tracked progress.

### Issue → module map (the A–O pipeline issues)
- B → Module 02 · C, E → Module 01 · I → Modules 01, 05 · H, G → Module 00 + blocking in 04
- F → Module 06 · N, M → Module 07 · D → Module 08 · J, K, L, O → Module 09
