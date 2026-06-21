# Code Fluency Ledger

Tracks Rajesh's Python/PySpark *syntax* literacy — separate from the
domain-concept calibration in `profile.md`. Domain calibration is per-domain;
this ledger is per-construct and cross-cutting, because the same PySpark idiom
(e.g. `F.when().otherwise()`) shows up across unrelated domains/modules.

Read by Stage 7 (Publish) before writing any code walkthrough: look up each
idiom the code uses here before deciding how much hand-holding it needs.

## How to read this file

- **Grain:** one row per *idiom/chunk*, not per atomic operator. `&`/`~`
  used together inside a filter expression is one row ("boolean column-mask
  filter"), not three.
- **Status ladder:** `needs-hand-holding` → `building` (1 pass) →
  `consolidating` (2 passes) → `fluent` (3 passes, each pass in a *different*
  module). A pass only comes from:
  - a passed Code-Comprehension Probe (see `probe-types.md`) — correct
    prediction on a sample not already shown in that walkthrough, or
  - an explicit **manual override** ("I've got this, stop explaining") —
    logged as `manual-override`, advances one tier immediately.
  - Exposure alone (a construct just appearing in a module) never advances a
    tier — it's logged under "Last evidence" as context, nothing more.
- **Demotion:** if Rajesh flags confusion on something marked
  `consolidating`/`fluent` in a later session, demote one tier and reset that
  tier's pass.
- **Stale recall:** a construct sitting at `building`/`consolidating` for
  several modules with no organic reuse should get a short "remember this?"
  recall callout seeded into an unrelated later module, rather than waiting
  indefinitely for coincidental reuse.

## Ledger

| Construct (idiom) | First seen (module) | Passes | Status | Last evidence | Notes |
|---|---|---|---|---|---|
| `F.when().otherwise()` classification pattern | score-aggregation-confidence | 0 | needs-hand-holding | exposed 2026-06-19 | column-wise conditional, not a Python `if`/`else` |
| Boolean column-mask filter (`&`/`~`/comparisons combined on Spark Columns) | score-aggregation-confidence | 0 | needs-hand-holding | exposed 2026-06-19 | overloaded bitwise ops as per-row boolean masks, not Python `and`/`not` |
| `Row` attribute access after `.first()` (e.g. `cm.tp`) | score-aggregation-confidence | 0 | needs-hand-holding | exposed 2026-06-19 | `.first()` returns a `Row`; dot-access reaches a column by name |
| `.withColumn` | nested-types (Module 01) | 0 | needs-hand-holding | exposed pre-ledger, no probe on record | seen ~3x before this system existed; verification-not-repetition rule means no credit without a passed probe |
| `.cast("int")` | score-aggregation-confidence | 0 | needs-hand-holding | exposed 2026-06-19 | type conversion, truncates rather than rounds |
| `.groupBy().agg()` | score-aggregation-confidence | 0 | needs-hand-holding | exposed 2026-06-19 | pivot-table equivalent: collapse rows sharing a key into one row per group |
| `.orderBy()` | score-aggregation-confidence | 0 | needs-hand-holding | exposed 2026-06-19 | sort by column, ascending by default |
| `.select(cols)` for column pruning | spark-performance (Module 10) | 0 | needs-hand-holding | exposed 2026-06-19; Code Companion drill available (Parquet 200 MB vs CSV 400 MB) — no probe taken | column-subset projection; on Parquet skips column bytes on disk, on CSV reads all then drops |
| `repartition(n)` vs `coalesce(n)` | spark-performance (Module 10) | 0 | needs-hand-holding | exposed 2026-06-19; Code Companion drill available (coalesce-can't-grow gotcha) — no probe taken | repartition = full shuffle, any count; coalesce = merge-only, decrease-only, no shuffle |
| `F.broadcast(df)` | spark-performance (Module 10) | 0 | needs-hand-holding | exposed 2026-06-19; Code Companion drill available (which side ships / no big-side shuffle) — no probe taken | ships the wrapped (small) side to every executor; skips shuffling the big side |
| `.cache()` / `.persist()` laziness | spark-performance (Module 10) | 0 | needs-hand-holding | exposed 2026-06-19; Code Companion drill available (recompute? / nothing cached w/o action) — no probe taken | marks for caching; materializes only on the first action, reused from 2nd action on |
| `spark.conf.set("spark.sql.shuffle.partitions", n)` | spark-performance (Module 10) | 0 | needs-hand-holding | exposed 2026-06-19; Code Companion drill available (set 16→16; unset→200) — no probe taken | runtime knob; post-shuffle output partition count; default 200, data-blind; AQE coalesces it |
| `F.collect_list(col)` in `groupBy().agg()` | graph-clustering (Module 08) | 0 | needs-hand-holding | exposed 2026-06-21; subgoal `.note` shown, no probe taken | gathers all values for a group key into one array column; here = collect every record_id of a cluster |
| `F.array_sort(col)` | graph-clustering (Module 08) | 0 | needs-hand-holding | exposed 2026-06-21; subgoal `.note` shown, no probe taken | sorts array elements into a fixed order; the load-bearing step that makes the entity_id hash order-independent |
| `F.concat_ws(sep, col)` | graph-clustering (Module 08) | 0 | needs-hand-holding | exposed 2026-06-21; subgoal `.note` shown, no probe taken | glue an array (or cols) into one string with a separator; "with separator" |
| `F.sha2(col, 256)` | graph-clustering (Module 08) | 0 | needs-hand-holding | exposed 2026-06-21; subgoal `.note` shown, no probe taken | deterministic hash → fixed 64-hex fingerprint; same input always same output; basis of the stable entity_id |
| `F.explode(arrayCol)` | nested-types (Module 01) → reused graph-clustering (Module 08) | 0 | needs-hand-holding | exposed 2026-06-21 (entity_map → record_to_entity fan-out); seen in Module 01 pre-ledger | one array row → many rows, one per element; here fans a cluster's member array back to one row per record_id |
| Self-join with `.alias("l")/.alias("r")` + `l.key < r.key` | graph-clustering (Module 08) | 0 | needs-hand-holding | exposed 2026-06-21 (household edges), no probe taken | join a table to itself to pair rows sharing a key; the `<` guard drops self-pairs and mirror-duplicates |
