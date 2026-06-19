# Source Segmentation

How to break different source types into loops for Stage 2. The rule is: **respect the source's native seams, then trim to the artifact**.

---

## Book (textbook, technical book, non-fiction)

**Native seams:** Chapters. Sometimes sections within chapters.

**Default mapping:** 1 chapter = 1 loop. Dense chapters may split into 2 loops; light chapters may combine with adjacent ones.

**Trimming for the artifact:**
- Identify the spine chapters (the ones the artifact actually needs)
- Skim chapters provide context only — one loop with a recall-depth probe
- Skip chapters are explicitly named and skipped; if Vineel ever needs them, they become future sessions

**Example:** A 12-chapter book, artifact = "explain Raft consensus to a junior engineer."
- Spine: Ch 3 (replicated state machines), Ch 5 (leader election), Ch 7 (log replication) — 3 deep loops
- Skim: Ch 1 (intro), Ch 2 (overview of consensus history) — 2 skim loops
- Skip: Ch 4, 6, 8–12 — off-path
- Total: 5 loops

---

## Blog post / article

**Native seams:** Sections under headers, or a single argument with no sub-structure.

**Default mapping:** 1 section = 1 loop for sectioned posts; entire post = 1 loop for short flowing ones.

**Trimming for the artifact:** Usually all sections matter for blog-sized posts. If not, name the irrelevant ones explicitly.

**Common shapes:**
- Tutorial blog (with code) → 1 loop per code section, probe = "run it" or "modify it"
- Opinion/argument blog → 1 loop for the thesis, 1 loop for the strongest counter-argument check
- Conceptual explainer → 1 loop, treat like a single chapter

**Flag:** Blog posts can rarely produce `teach`-depth understanding on a non-trivial topic. Surface this in Stage 2.

---

## Video (lecture, talk, tutorial)

**Native seams:** Topic shifts. Use timestamps if available; otherwise scrub through and identify them.

**Default mapping:** 1 topic-shift = 1 loop. A 60-min talk typically yields 4–7 loops.

**Trimming for the artifact:**
- Watch at appropriate speed (1.25–1.5× is fine for familiar adjacencies)
- Pause at topic-shift boundaries for the probe — don't try to probe while video plays
- For dense technical talks, transcribe the key segment first

**Probe specifics:** Videos invite passive consumption. The probe is the antidote. Don't let a chunk pass without a forced production from Vineel.

**Flag:** Tutorial videos (especially coding ones) often skip the *why* in favor of the *how*. If artifact is `use` or `teach`, supplement with a doc or paper.

---

## Paper (academic, technical, white paper)

**Native seams:** Sections — typically Intro, Background/Related Work, Method, Experiments, Results, Discussion, Conclusion.

**Default mapping:** Don't read top-to-bottom. Use the three-pass method:
- **Pass 1 (1 loop):** Abstract + Intro + Conclusion + figures. Probe: "What problem, what claim, what method family?"
- **Pass 2 (2–4 loops):** Method section in detail; key experiments. Probe per concept.
- **Pass 3 (1–2 loops, optional):** Replicate or extend mentally. Only for `use` or `teach` depth.

**Trimming for the artifact:**
- `recognize` depth → just Pass 1 (1 loop total)
- `use` depth → Passes 1 + 2 (3–5 loops)
- `teach` depth → all three passes (5–7 loops); honestly, often needs a follow-up source

**Flag:** Papers assume prerequisites. Identify them in Stage 1 anchor check — if missing, load them first or relax artifact.

---

## Codebase (open-source project, internal repo)

**Native seams:** Modules, packages, or call-graph entry points.

**Default mapping:** Don't read file-by-file. Use entry-point traversal:
- **Loop 1:** Read the README + top-level structure. Identify entry points.
- **Loop 2..N:** Trace one entry point through the call graph; one loop per major module touched.

**Trimming for the artifact:**
- `recognize` depth → just README + architecture diagram if present
- `use` depth → entry points + critical-path modules; skip tests, skip configs
- `teach` depth → also read the tests (they show the public contract)

**Probe specifics:** For code, the probe should be "predict the output", "modify the behavior", or "explain why this design choice".

**Flag:** Large codebases are bottomless. Set a hard loop budget in Stage 2 and stop when hit, regardless of coverage.

---

## Course (multi-lecture, structured)

**Native seams:** Lectures + the course's own structure.

**Default mapping:** 1 lecture = 1 loop. Combine with lecture notes/slides if available.

**Trimming for the artifact:** Courses tend to be over-comprehensive. Identify the 30–40% of lectures that produce the artifact and skip the rest. Use the course syllabus as the spine.

**Flag:** Course videos are slow. Prefer lecture notes if both exist; videos only when notes are insufficient.

---

## Documentation (API docs, framework docs)

**Native seams:** Topic pages, often organized by concept or feature.

**Default mapping:** Goal-directed reading only — never read docs front-to-back.
- Loop 1: Conceptual overview / getting started
- Loop 2..N: One loop per concept the artifact requires

**Probe specifics:** Run the code. Docs without execution don't stick.

---

## When the source is wrong for the artifact

Surface explicitly in Stage 2. Common mismatches:

| Declared artifact | Wrong source | Why |
|---|---|---|
| `teach`-depth explanation | Single blog post | Insufficient depth |
| Working code | Conceptual blog | No reference implementation |
| Operational mastery | YouTube intro video | Missing the failure-mode coverage |
| Quick decision | Full textbook | Massive over-investment |
| `use`-depth on niche topic | Generic overview | Doesn't reach the actual concept |

In all cases: recommend a better source, OR relax the artifact, before running loops.
