# MDM / Spark / Entity Resolution — Learning Path

> Living reference for Rajesh's curriculum, broken into ordered modules across 4 phases.
> The live, canonical progress tracker is **roadmap.html** on the site. This file mirrors it for version control — kept in sync with roadmap.html's `PHASES` data.
> Frame (locked): Why=build · Anchor=MDM/PySpark ER pipeline · Angle=mechanistic+table-driven · Depth=use · Budget≈45min/session.

## Status legend
- ✅ done · 🔜 up next · ⬜ locked

---

## Progress snapshot (as of 2026-06-20) — modules 00–11 across 4 phases; ALL BUILT ✅ TRACK COMPLETE

> **Code Companions are now standalone modules**, each placed immediately before the concept module it supports: **05** before Score Aggregation (06), **09** before Spark Performance (10). Mirrors roadmap.html (11 modules excl. the 00 overview).

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
- ✅ **05 — Code Companion — ThresholdTuner Mechanics** — `score-aggregation-confidence-code.html` *(built 2026-06-19)*
  - Topics: F.when/otherwise, boolean column masks, Row attribute access, .cast, groupBy().agg()/orderBy()
  - Unlocks: read the ThresholdTuner PySpark idioms fluently before the concept module — predict-then-reveal drills on fresh data.
- ✅ **06 — Score Aggregation & Confidence** — `score-aggregation-confidence.html` *(built 2026-06-19)*
  - Topics: weighted aggregation, confidence bands, review queues, precision vs recall
  - Unlocks: tune the thresholds that decide which pairs auto-merge, which go to human review, and which are rejected.

### Phase 3 — ER at Scale  (~2 sessions)
- ✅ **07 — LSH & MinHash** — `lsh-minhash.html` *(built 2026-06-19)*
  - Topics: minhash, banding, jaccard, candidate generation
  - Unlocks: find candidate pairs at scale without all-pairs comparison — approximate blocking that complements the self-join.
- ✅ **08 — Graph Theory & Clustering** — `graph-clustering.html` *(built 2026-06-19)*
  - Topics: connected components, union-find, BFS/DFS, transitive matches
  - Unlocks: how matched pairs merge into one master entity — the final ER step that turns pairs into clusters.

### Phase 4 — Pipeline Mastery (Capstone)  (~2 sessions)
- ✅ **09 — Code Companion — Performance Idioms** — `spark-performance-code.html` *(built 2026-06-19)*
  - Topics: .select pruning, repartition/coalesce, F.broadcast, .cache, spark.conf.set
  - Unlocks: read the five performance idioms fluently before the levers module — predict-then-reveal drills with hand-verified traces.
- ✅ **10 — Spark Performance (Remaining Levers)** — `spark-performance.html` *(built 2026-06-19)*
  - Topics: column pruning, predicate pushdown, memory tuning, partition sizing
  - Unlocks: optimize the full pipeline beyond shuffle/join/skew.
- ✅ **11 — Pipeline Design (Capstone)** — `spark-pipeline-design.html` *(built 2026-06-20)*
  - Topics: DAG & contracts, intermediate datasets, YAML plugin engine, join-back, enrichment, incremental vs full, orchestration, observability, end-to-end simulator
  - Unlocks: design the full MDM entity resolution architecture end to end — and feel how a knob at any stage ripples through to the final master entities.

---

## Why this order (from roadmap.html)
- **01 before 04:** can't score strings without first knowing how strings are processed and stored. Nested types and normalization come before the scoring algorithms that consume them.
- **03 in Phase 1, not Phase 2:** window functions are Spark mechanics, not entity-resolution concepts — finish the toolkit before touching scoring.
- **07 (LSH) before 08 (graph):** LSH produces another stream of candidate pairs; graph clustering consumes ALL pairs (blocking + LSH) and merges them into entities, so LSH must come first.
- **Code Companions (05, 09) sit just before their concept module:** drill the heavy PySpark idioms to fluency *before* meeting them embedded in the concept walkthrough (05 → 06 Score Aggregation; 09 → 10 Spark Performance).
- **11 last (capstone):** needs vocabulary from every prior module to reason about each architectural decision — which joins to broadcast, where shuffles live, how LSH integrates with blocking.

---

## Module 04 — what was covered (built 2026-06-19)
9-stage flow-module-builder treatment, matching the Module 03 style.
- **Stage 01** Why a flat average breaks — two distinct pairs (same-household vs moved-person) that average identically; the corruption argument.
- **Stage 02** Field weighting — courtroom/DNA analogy; the **"raw score is a red herring; discriminating power decides"** contrast (Rajesh's signature fix); shippable weight table; weights as YAML config.
- **Stage 03** Composite score — Σ(sim×weight); worked contribution table + accumulating debug trace; weighted-sum = weighted-average when weights sum to 1.
- **Stage 04** Null handling (the climax) — disagreement (0.0, stays in denominator) vs absence (null, drops from both); the **"they look the same in the numerator; the denominator decides"** red-herring contrast; verdict-flips-on-renormalization worked example; wrong vs right scorer with output.
- **Stage 05** Thresholds — three bands (match/review/no-match); classify ladder; precision↔recall lever (forward-link to Mod 06).
- **Stage 06** Full PySpark ScoringPlugin pattern — `F.when(present, ...)` as the column-wise null guard; num/den accumulators; config-vs-logic separation.
- **Stage 07** Interactive Score Builder — live sliders + absent toggles, renormalizing math readout, 4 presets (household trap, moved person, absent SSN, reset).
- **Stage 08** Self-test — 8 scenario-recognition questions (the format that re-energizes Rajesh).

## Module 06 — what was covered (built 2026-06-19)
10-stage flow-module-builder treatment, matching the Module 04 style. *(Code drills for its idioms live in the preceding **Module 05 — Code Companion**.)*
- **Stage 00** Overview — where Module 06 picks up from Mod 04's threshold guessing; the four core concepts (labeled data, confusion matrix, precision/recall, confidence bands).
- **Stage 01** Why fixed thresholds fail — the implicit promise, two datasets same thresholds opposite disasters, the distribution problem.
- **Stage 02** Labeled data — what a labeled set looks like, how much you need, stratified sampling, the "label everything later" red herring.
- **Stage 03** Precision & recall — confusion matrix (TP/FP/FN/TN), worked 200-pair example, precision as "how clean are my merges", recall as "how many did I catch", the trade-off concretely with raise/lower threshold contrast.
- **Stage 04** The PR curve — sweeping every threshold, reading the curve, the "elbow" (diminishing returns analogy), two thresholds not one.
- **Stage 05** Confidence bands — calibration table (score bin → match rate), the "score height means confidence" red herring, adding a confidence column to the pipeline, calibration drift warning.
- **Stage 06** Review queue sizing — the three-way budget (auto-merge / review / auto-reject), worked 50k-pair queue sizing, the capacity formula, queue overflow as the silent killer, the tuning loop end to end.
- **Stage 07** ThresholdTuner pattern — full PySpark class (confusion_matrix, pr_at, pr_curve, calibration_table, queue_size methods), usage alongside ScoringPlugin.
- **Stage 08** Interactive Threshold Tuner — live sliders for match/review thresholds, 200 simulated labeled pairs, real-time precision/recall/F1/queue readouts, 5 presets (conservative, balanced, aggressive, tight review, reset).
- **Stage 09** Self-test — 8 scenario-recognition questions covering precision failures, sampling bias, queue overflow, calibration per-dataset, the elbow, F1 limitations, calibration table interpretation, calibration drift.

## Module 07 — what was covered (built 2026-06-19)
11-stage treatment, matching the Module 06 style.
- **Stage 00** Overview — visualizes LSH blocking in the pipeline; Jaccard, MinHash, Banding, and S-curve tuning.
- **Stage 01** The N² Wall — growth table of N vs N²/2 comparisons; contrasts rigid blocking keys vs LSH fuzzy blocking.
- **Stage 02** Jaccard Similarity — k-gram character shingling; Venn diagram analogy; worked shingle intersection/union table.
- **Stage 03** The MinHash Trick — set compression; random permutations index matching math; worked shingle permutation matrix.
- **Stage 04** Banding & LSH — dividing signature $K = b \times r$; Murmur hashing bands; "LSH is a replacement for scoring" red herring.
- **Stage 05** Tuning LSH — S-curve formula $P = 1 - (1 - s^r)^b$; threshold elbow calculation $t \approx (1/b)^{1/r}$; worked b/r tuning table.
- **Stage 06** PySpark Pattern — RegexTokenizer, NGram, CountVectorizer, MinHashLSH, approxSimilarityJoin; PySpark Jaccard distance trap ($D = 1-S$).
- **Stage 07** The Hybrid Pipeline — union and distinct of exact blocking and LSH candidates; full Spark pipeline pattern.
- **Stage 08** Interactive LSH Tuner — live b and r sliders; dynamic SVG S-curve plotting; deterministic band collision simulation on 10 customer records.
- **Stage 09** Self-test — 8 scenario-recognition questions covering LSH parameters, distance join, shingle size, case tokenization.

## Module 08 — what was covered (built 2026-06-19)
10-stage treatment, matching the Module 07 style.
- **Stage 00** Overview — visualizes clustering closing the pipeline; connected components, BFS/DFS, union-find, transitive closure.
- **Stage 01** From Pairs to Entities — the moved-person scenario (A↔B match, B↔C match, A↔C never scores), motivating why pairwise verdicts alone are insufficient.
- **Stage 02** Graph Model — ER-to-graph-theory term mapping table; friendship-circle analogy; worked component trace on the moved-person graph.
- **Stage 03** BFS/DFS Traversal — component-finding algorithm; full debug trace on a 6-record graph (A-B, B-C, D-E, isolated F); cost/scale caveat motivating union-find.
- **Stage 04** Union-Find — find/union operations; same 6-record graph traced via union-find for direct comparison; path compression explained.
- **Stage 05 (climax)** Transitive Closure — the "clustering just groups matched pairs" red herring; the bridge-edge failure mode (one weak match fuses two large clusters); cluster-size sanity-check mitigation.
- **Stage 06** Choosing an Approach — 3-question decision tree (memory fit → Spark-native vs hand-rolled → audit-path needs) + side-by-side comparison table.
- **Stage 07** PySpark Pattern — GraphFrames `connectedComponents()` from ThresholdTuner match verdicts; checkpoint-dir trap; join-back into Module 03's window-function golden-record selection.
- **Stage 08** Interactive Cluster Builder — canvas-based union-find widget; click candidate pairs to add edges live; guided sequence demonstrating the transitive-fuse climax visually.
- **Stage 09** Self-test — 8 scenario-recognition questions covering transitive closure, bridge-edge risk, checkpoint dir, path compression, BFS/DFS vs Spark fit, edge-list sourcing, singleton components.

## Module 10 — what was covered (built 2026-06-19)
11-stage treatment, matching the Module 08 style. *(Code drills for its five idioms live in the preceding **Module 09 — Code Companion**, `spark-performance-code.html`.)*
- **Stage 00** Overview — Module 10 tunes every existing stage rather than adding one; distinguishes the three *structural* levers from Module 00 (shuffle/join/skew) from the five *cost* levers here; five concept cards (column pruning, predicate pushdown, partition sizing, spill/memory, caching+AQE).
- **Stage 01** The "it runs, ship it" cost trap — naive 2 TB / 40-col read vs the 6-col / active-only footprint (~11× waste); the "performance bugs don't throw" framing; SELECT * anchor.
- **Stage 02** Column pruning — row-major vs columnar (Parquet skips unread column-runs on disk); CSV buys nothing; the wide-table MDM trap; prune-too-aggressively-is-a-correctness-bug caveat (keep `updated_at` for Mod 03's window).
- **Stage 03** Predicate pushdown — filter-in-engine vs filter-pushed-into-scan (herring contrast); partition pruning (skip directories) vs row-group min/max; what blocks pushdown (UDF/explode/regex); `.explain()` → `PushedFilters` verification.
- **Stage 04** Partition sizing — ~128 MB target; desks-and-paper anchor reused from Mod 00; `repartition` (full shuffle, can grow, even) vs `coalesce` (no shuffle, shrink-only, uneven) comparison table; the 200-default `spark.sql.shuffle.partitions` trap → tiny files.
- **Stage 05 (climax)** Spill & memory — what spill is (execution region overflow → disk), spill ≠ OOM; the **"just add more RAM is the wrong reflex"** red herring (spill is per-task data-vs-memory, fix = more/smaller partitions or fix skew); caching as the other memory lever with the "cache everything" anti-pattern; cache-is-lazy warning.
- **Stage 06** AQE — three runtime features (coalesce shuffle partitions, skew-join split, dynamic broadcast switch); the "AQE owns the shuffle, you own the read + the DAG" split table (pruning/pushdown/caching stay manual).
- **Stage 07** Decision tree — five symptom→lever cards keyed to Spark-UI-observable symptoms (bytes scanned, task count, spill, recompute, big-vs-tiny join); "one symptom, not all five" framing; "most slow tickets are Symptom 1."
- **Stage 08** PySpark pattern — the Stage 01 read rewritten with all five levers (AQE conf, select+filter, `F.broadcast`, `.cache`, `.coalesce(64)` write, `.explain()`), highlighted line-by-line; order-matters trap; links to the Code Companion.
- **Stage 09** Interactive Tuning Calculator — **combined two-mode widget** (Rajesh chose "both"): Partition Sizing (data + target MB → partitions, per-task MB, spill-band verdict) and Shuffle Tuning (output size + shuffle.partitions → files, avg size, tiny-files verdict, the 200 trap). U-shaped-cost-curve takeaway.
- **Stage 10** Self-test — 8 scenario-recognition questions (prune vs memory, coalesce vs repartition, coalesce-can't-grow, spill-first-move, lazy DataFrame recompute, cache-without-action, the 200 default, what AQE won't fix).

### Module 09 — Code Companion (Performance Idioms) — `spark-performance-code.html`
Now a standalone module sitting just before Module 10 (sibling to Module 05, the ThresholdTuner Code Companion). Five idioms, predict-then-reveal, two fresh-data reps each, hand-verified trace values: `.select()` pruning (Parquet 200 MB vs CSV 400 MB), `repartition` vs `coalesce` (coalesce-can't-grow gotcha), `F.broadcast` (which side ships / no big-side shuffle), `.cache()` laziness (recompute? / nothing cached without an action), `spark.sql.shuffle.partitions` (set 16 → 16; unset → 200). Includes the PySpark lazy/distributed "logical result, not literal execution order" caveat. See `code-fluency.md` for the ledger entries.

## Parked / for later
- Nothing parked from Module 07 itself.
- **From Module 10:** bucketing & pre-sorted tables (write-time-for-read-time), the unified memory model knobs (`spark.memory.fraction`/`storageFraction`, region borrowing) in detail, `.persist()` storage levels (MEMORY_ONLY vs MEMORY_AND_DISK vs serialized/off-heap), a hands-on Spark-UI tour (SQL/Stages tabs), dynamic resource allocation & cluster sizing (executor count, cores-per-executor, autoscaling).
- **From Module 08:** weighted/probabilistic clustering (edge-confidence-aware community detection), cluster-splitting/review-queue tooling at the cluster level, GraphFrames' internal algorithm (Hash-to-Min label propagation) and convergence behavior, graph algorithms beyond connectivity (centrality, shortest-path, community detection for fraud rings).
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
- B → Module 02 · C, E → Module 01 · I → Modules 01, 06 · H, G → Module 00 + blocking in 04
- F → Module 07 · N, M → Module 08 · D → Module 10 · J, K, L, O → Module 11
