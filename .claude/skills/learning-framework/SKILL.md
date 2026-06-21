---
name: learning-framework
description: "A staged learning protocol for Rajesh that turns any source (book, blog, video, paper, codebase, course) into validated understanding via initial calibration, source segmentation, and a Map→Translate→Probe→Patch loop. Triggers when the user wants to learn, study, understand, work through, prep on, or go deep on any subject or source. Use this skill for 'I want to learn X', 'help me understand Y', 'I'm reading [book/blog/paper]', 'walk me through this video', 'study session on Z', 'prep me on W', 'go deep on V', or any request that pairs a learning intent with a source to consume. Use this skill any time Rajesh starts a learning session, even if he doesn't explicitly name the framework."
---

# Learning Framework

A staged protocol for translating any source into validated understanding, with per-domain calibration that improves over sessions.

## Why this skill exists

Most learning fails because: (1) the source is read from the wrong projection for the learner's actual goal, (2) "understanding" is assumed from passive reading rather than validated by probes, (3) pacing doesn't adapt to current energy or domain familiarity, and (4) what's learned isn't crystallized into a durable artifact.

This skill fixes all four with a six-stage pipeline where each stage has an explicit exit criterion. The artifact specification (declared in Stage 1) drives all downstream decisions backward — segmentation, loop count, probe types, and depth all collapse toward producing it.

## The Pipeline

```
Stage 1: INITIAL CALIBRATION       (declare the frame)
   ↓
Stage 2: SOURCE SEGMENTATION       (chunk the source for the artifact)
   ↓
Stage 3: SESSION LOOP              (Map → Translate → Probe → Patch) — repeats per chunk
   ↓
Stage 4: RUNNING CALIBRATION       (every K loops; can renegotiate frame)
   ↓
Stage 5: ARTIFACT ASSEMBLY         (produce the declared output)
   ↓
Stage 6: PROFILE UPDATE            (write per-domain calibration data)
   ↓
Stage 7: PUBLISH                   (the-learning-lab only — see below)
```

Every stage has an exit criterion. Do not advance silently.

Stage 7 only applies when the declared Stage 1 artifact is a website module for
the-learning-lab (this repo). For any other artifact (compression, diagram,
predictions, code, script, questions), the pipeline ends at Stage 6.

---

## Stage 1: Initial Calibration

Declare the frame. Six fields, all required.

**Before asking Rajesh anything,** read `references/profile.md` (if it exists) for prior calibration data on this domain. Pre-fill any fields the profile can answer (chunk size, angles that worked, prerequisites already confirmed). Only ask for fields not declared and not inferable.

| Field | Question | Notes |
|---|---|---|
| **Why** | What's this learning for? | decision / build / interview / curiosity / teach |
| **Anchor** | What adjacent thing do you already know well? | Translate target into this |
| **Angle** | Which projection? | first-principles / mechanistic / comparative / applied / adversarial / historical |
| **Depth** | How deep? | recognize / use / teach |
| **Budget** | Minutes available + energy state | e.g., "45 min, energy med" |
| **Artifact** | What you'll produce at the end | See `templates/artifact.md` for options |

**Internal consistency check (exit criterion):** Flag any obvious mismatch before proceeding.

- Depth = `teach` with budget < 30 min → flag
- Depth = `teach` with no prior anchor in this domain → flag
- Angle = `applied` with artifact = "explanation" → flag, suggest realignment
- Energy = `low` with depth = `teach` → flag, suggest dropping to `use`
- Source is light (blog) with depth = `teach` → flag source-artifact mismatch early

Do not auto-resolve mismatches. Surface them and let Rajesh re-declare.

**Exit criterion:** All 6 fields declared, internally consistent.

---

## Stage 2: Source Segmentation

Look at the source. Propose chunking based on three inputs:

1. **Source's native structure** — chapters, sections, video timestamps, paper sections, code modules
2. **Stage 1 artifact + depth** — which chunks are spine (deep), context (skim), off-path (skip)
3. **Rajesh's chunk size for this domain** — from `references/profile.md`

See `references/source-segmentation.md` for type-specific segmentation rules (books vs. blogs vs. videos vs. papers vs. codebases).

Output format:

```
Source: [name]
Native structure: [N chapters / N sections / N timestamps / N modules]
Plan for your artifact:
  Deep loops:  [chunks 1, 3, 5]      ← spine
  Skim loops:  [chunks 2, 7]         ← context only
  Skip:        [chunks 4, 6, 8-12]   ← off-path
Total: N loops. Estimated time: M minutes.
Running calibration every K loops (default K=3; lower for unfamiliar domains).
```

**Source-artifact mismatch check (exit criterion):** If the source can't produce the declared artifact, say so directly. Examples:

- "This blog gives a conceptual overview but won't get you to operational mastery — you'll need a textbook chapter or codebase walkthrough for that."
- "This 90-minute video covers breadth but no depth on Topic X — fine for `recognize`, insufficient for `teach`."
- "This paper assumes prerequisite Y; load that first or relax artifact to `recognize`."

If mismatch: recommend a different source OR a relaxed artifact. Do not proceed with a mismatched plan.

**Exit criterion:** Rajesh approves the chunk plan, OR source/artifact is replaced.

---

## Stage 3: Session Loop

One loop per chunk. Four steps. Do not skip steps.

### 3a. Map
Sketch the minimal concept set for THIS chunk that's relevant to the artifact.
- List 3–7 concepts in dependency order
- Mark concepts that depend on prerequisites Rajesh may not have (check anchor from Stage 1 and `profile.md`)
- If a prerequisite is missing, pause the loop and run a mini-loop on the prerequisite first

### 3b. Translate
Render each concept using Rajesh's anchors, not the source's native vocabulary.
- "This is like X you already know, except for Y difference"
- Use his actual domain language (backend, FastAPI, GCP/AWS, distributed systems, RAG, etc.)
- Defer the source's jargon until after the anchor lands

### 3c. Probe
Validate that understanding actually happened. **Probe type is derived from depth target** (see `references/probe-types.md`):

| Depth | Probe type | Example shape |
|---|---|---|
| recognize | Recall | "What is X?" / "Which of these is X?" |
| use | Application | "Apply X to this novel case" / "Predict what happens if..." |
| teach | Explain-to-novice | "Explain X to a junior engineer in 60 seconds" |

The probe is the loop's gate. Move on only after it passes.

### 3d. Patch
If the probe fails, switch projection and retry — don't repeat louder.

- Formal failed → try analogy
- Analogy failed → try formal/mechanistic
- Both failed → try comparative ("X is what you get when you remove constraint C from Y")
- Comparative failed → check for missing prerequisite

**Two-failure escalation rule (hard rule):** If two patches in a row fail on the same concept, do NOT continue the loop. Escalate immediately to Stage 4 running calibration, regardless of where you are in the K-loop interval. Likely causes:
- Missing prerequisite → load it as a mini-loop
- Wrong angle declared → renegotiate Stage 1 angle
- Concept genuinely off-path → park it, log as known gap

**Exit criterion per loop:** Probe passes (with or without one patch), OR loop is explicitly parked with a note for the artifact.

---

## Stage 4: Running Calibration

Run every K loops (K from Stage 2), AND immediately whenever the two-failure escalation rule fires.

Check two signals:

**Energy** (self-reported, 1–5)
- Ask: "Energy check, 1–5?"
- Combine with AI's signal: probe latency rising? Answer quality degrading? Hedged answers?

**Understanding** (AI-tracked)
- Probe pass rate over last K loops
- Number of patches needed
- Time per loop trend

Decision matrix:

| Energy | Understanding | Action |
|---|---|---|
| 4–5 | Strong | Continue; optionally increase chunk size |
| 3 | Strong | Continue as-is |
| 1–2 | Any | Stop session; assemble artifact with what's covered |
| Any | Weak + Energy ≥3 | Shrink chunks OR switch angle OR check missing prerequisite |
| Any | Weak + Energy ≤2 | Stop session |

**Frame renegotiation:** Running calibration can change the Stage 1 declaration mid-session, not just pacing. If the declared angle isn't working, surface it explicitly and let Rajesh re-declare angle, depth, or artifact. Don't grind in a bad frame.

**Exit criterion:** An explicit decision is logged. No silent continuation.

---

## Stage 5: Artifact Assembly

The artifact has been accumulating across loops. Finalize it now.

Match the artifact format declared in Stage 1. See `templates/artifact.md` for shapes. Common ones:

- **One-paragraph compression:** ≤150 words, no jargon Rajesh doesn't already own
- **Diagram:** Mermaid or ASCII, labeled with Rajesh's anchors
- **Predictions:** 3–5 testable predictions the new model lets him make
- **Working code:** Runnable, with comments tying code to the concept
- **Explain-to-junior script:** ~60-second spoken explanation
- **Three questions:** Three non-trivial questions he can now answer, with the answers

**Always include a "Honest Gaps" section:** What was parked, what depth wasn't reached, what would need a future session. Do not pretend coverage that didn't happen.

**Exit criterion:** Artifact meets the Stage 1 spec, OR gap is logged honestly.

---

## Stage 6: Profile Update

Append to `references/profile.md` (create if missing — see `references/profile-schema.md` for schema).

Write the following for the domain just studied:

- Chunk size that worked (small / medium / large)
- Sustain window (minutes before quality degraded)
- Angles that worked / didn't work
- Prerequisites confirmed present
- Known gaps (with date)
- Last session reference (date, source, artifact link/summary)

Read by Stage 1 and Stage 2 next time the same domain comes up.

**Exit criterion:** Profile updated. Session ends here — unless the Stage 1 artifact was a the-learning-lab website module, in which case continue to Stage 7.

---

## Stage 7: Publish (the-learning-lab website only)

Only runs when Stage 1's declared artifact is a published HTML module for this site. Closes the loop between "Rajesh learned something" and "a module is live on the website" — see root `CLAUDE.md` for the full two-system orchestration this stage completes.

**Back-apply rule (hard rule).** When a later remediation or running-calibration logs a calibration lesson about a topic whose module is *already published* (e.g. the 2026-06-20 LSH remediation that found the sticker-bag framing), the lesson is not done until the **published module HTML is patched** — not just `profile.md` and this `SKILL.md`. A lesson that lives only in the profile/skill while the live module still contradicts it is an open defect. (This exact gap shipped the formula-first Module 07 that Rajesh later rejected; the fix landed in the 2026-06-21 flow rebuild.)

1. **Build the module file** under `modules/`. The list of section types below (motivating example → analogy/anchor → worked mechanism → climax/gotcha → decision criteria → runnable code → widget → self-test → mandatory Honest Gaps) is a **palette, not a running order, and not a checklist to fill**. A module is a single descending thread, not a catalog of these sections laid end to end. Build for the **North Star: put Rajesh in flow state while reading, without overwhelming him** — he can drop into the module and keep going without ever having to supply his own motivation for the next step. In-repo modules that already achieve this and should be used as the reference standard: `match-scoring-classification.html` and `score-aggregation-confidence.html` (problem "stated once" in plain language → tension headers that pose questions → each section pulled by the prior one's open gap). Avoid the failure mode of `lsh-minhash.html` *before its 2026-06-21 rebuild*: mechanism-noun headers ("The Banding Mechanism"), `sec-sub`s that restate their own titles, and stages that each cold-start.
   - *Self-check*: Verify that all custom CSS classes and ID selectors defined in the module's `<style>` block (like charts, canvas wrappers, or diagram containers) are actually implemented and referenced in the HTML body, ensuring no layout features are left as empty placeholders.
   - **Through-line gate (run before writing the file, hard rule).** State two things explicitly: (a) the **single spine question** the whole module answers, and (b) the ordered list of **tension-handoffs** — for each section, the gap that pulls the reader into it, which must equal the previous section's closing tension. *If any section can't name the gap that motivates it, it is a catalog entry: re-motivate it or cut it.* Headers must express that tension (a question or a stakes phrase), never a bare mechanism noun; no `sec-sub` may merely restate its own `sec-h`. This is the flow analogue of the optional-menu pre-build check — a quick stated plan, not a blank-slate interrogation.
   - **Flow over coverage (success criterion).** The module is graded on whether it reads as one continuous thread with minimum cross-boundary cognitive load — NOT on whether every section type is present or every concept is individually probed. Prefer **one chained analogy world** carried end to end (e.g. the sticker-bag world that runs Jaccard → MinHash → banding → S-curve in the rebuilt Module 07) over a fresh metaphor per section, which forces the reader to re-onboard at every boundary. Coverage with no through-line is the defect this criterion exists to catch.
   - **Subject-driven sizing (hard rule, both directions).** The number of stages/sections is an *output* of the topic's real conceptual structure, never an *input target*. A rich topic earns more stages; a simple one earns fewer — both are correct. Explicitly forbid **both** failure modes: padding a simple topic up to match the ~8–14-stage chassis of sibling modules "for the sake of the template," and trimming a rich topic down to look lean. Fit to the subject; do not bias toward long or short.
   - **Formula-first is a failure mode (hard rule for probabilistic / abstract-math topics).** When a topic's core rests on a formula — probability, expectation, similarity metrics, information theory, anything where a symbol like $P(\cdot)$ / $\sum$ / a ratio is the load-bearing idea — the module MUST lead with a **concrete physical analogy and let the number emerge from it**, then introduce the formula *only after* the intuition is built, as a compact restatement of what the analogy already showed. Do NOT present the formula as the primary explanation with the analogy bolted on after. Evidence this matters: Module 07 (MinHash) shipped at `use` depth but taught via the probability framing ($P = |A\cap B|/|A\cup B|$ + signature tables); on cold re-probe Rajesh said "seems very tough" and disengaged before attempting. Re-teaching with a raffle/sticker-bag analogy first (pull stickers from a bag, "match" only when the first-pulled sticker is on both lists → match-rate *is* the overlap fraction) landed first try, and the formula then read as obvious. The notation triggers shutdown *before* engagement; the analogy is the on-ramp, not a garnish. This generalizes the Stage 3b anchor-before-jargon principle specifically to math-heavy module builds, where the temptation to lead with the clean formula is strongest.
   - **Optional menu (include only if it earns its place for this specific topic):** decision criteria (only if the topic is genuinely a "choose between options" call), runnable code pattern (only if the topic is code-shaped), interactive widget (only if there's a real tunable parameter/threshold worth exploring hands-on — not every topic has one), climax/gotcha framing, scenario-based self-test.
   - **Pre-build check (run before writing the file):** propose, in 2–3 short bullets, which optional sections this topic needs and why (e.g. "07 — Graph Theory: no natural tunable parameter → skip widget; clustering vs. no clustering is a real tradeoff → include decision criteria"). Let Rajesh confirm or override. This is a quick confirm, not a blank-slate interrogation — same pre-fill-then-ask pattern as Stage 1.
   - **Code-fluency check (run for every code block in a runnable-code-pattern section):** for each Python/PySpark idiom the code uses, look it up in `references/code-fluency.md`.
     - **needs-hand-holding / building / consolidating:** structure as Predict-then-reveal — show the code + a small toy dataset, ask for a prediction on one key line, then reveal the real computed value via a concrete sample-data trace table (reuse the existing "watch the values" / traced-table pattern already used elsewhere on this site — don't invent a new pattern). **The prediction target must be the literal evaluated value of the syntax idiom itself** (e.g. what does `predicted & is_match` evaluate to for this row, what does `.cast("int")` produce for 8.8, what does `cm.fp` return) — never the domain-level conclusion derived from it (e.g. which TP/FP bucket, what precision computes to). A domain-conclusion question tests something Rajesh likely already has from the concept walkthrough; only a question about the code's own evaluated value actually tests the idiom this check exists for. If the idiom has no prior plain-language aside logged, add a short subgoal-style `.note` callout naming what that chunk's job is, separate from the domain-logic explanation. If the idiom is PySpark-specific (lazy/vectorized/distributed), include a one-line caveat that the trace table shows the *logical* result, not literal row-by-row execution order — Spark evaluates across a whole column at once, and a sequential-looking table can otherwise teach the wrong mental model.
     - **fluent:** skip the predict step and the aside. Keep the data trace only if it still serves understanding of the *domain* algorithm — a separate goal from syntax fluency, judgment call.
     - Trace-table values must be independently verified (hand-computed values are exactly what causes wrong "ground truth" in a Predict-then-reveal step), not just asserted.
     - After publishing, log this module as the idiom's encounter context in `code-fluency.md` — this never advances a tier by itself; only a passed Code-Comprehension Probe or an explicit manual override does (see `references/probe-types.md`).
2. **Update `references/roadmaps/<track-id>.md`** for the topic this module belongs to (done in Stage 6, but verify here): flip the module's status to done, set the next module to `🔜`, carry forward any gaps. If this is the first module for a brand-new topic, this file won't exist yet — create it (same shape as `references/roadmaps/mdm-spark.md`: phases → modules → topics/tags → "unlocks").
3. **Update the two website registries for this track's `id`** — they are parallel and must stay in sync:
   - `index.html` `TRACKS` array — flip the module from `soon:true` to live (add `href`, `date`; move `latest:true` to the new module). If the track doesn't exist yet, add a new entry.
   - `roadmap.html` `ROADMAPS` array — change `status` from `locked`/`next` to `done`; set the next module's `status` to `next`. If the track doesn't exist yet, add a new entry (phases can start empty).
4. **Commit and push** following `docs/DEPLOY.md`'s standard module-publish flow, then verify the push landed (`git rev-parse HEAD` vs `git ls-remote origin main`).

**Exit criterion:** Module live on Vercel, both registries updated and in sync, push verified per `docs/DEPLOY.md`.

---

## Quick-Start Invocation

When Rajesh signals a learning intent (see description triggers), jump straight to Stage 1 — ask the 6 calibration questions concisely. Do NOT first explain the framework; just run it.

If he's mid-session and pings ("OK next chunk", "continue", "next"), continue at Stage 3 with the next loop.

If he says "running cal", "energy check", or shows fatigue (slow answers, hedged responses, asking for breaks), trigger Stage 4 explicitly.

If he gives the source up front but no calibration fields, start with Stage 1 questions before touching the source.

## Reference Files

- `references/probe-types.md` — Probe types per depth target, with concrete examples
- `references/source-segmentation.md` — How to segment books / blogs / videos / papers / codebases
- `references/profile-schema.md` — Schema for `profile.md`
- `references/profile.md` — Per-domain calibration data (created on first real session)
- `references/roadmaps/<track-id>.md` — Per-topic module curriculum for the-learning-lab website (e.g. `roadmaps/mdm-spark.md`); one file per roadmap/track, created when a new topic is broken into modules
- `references/code-fluency.md` — Cross-track ledger of Python/PySpark syntax-idiom fluency, separate from domain calibration; consulted in Stage 7's code-fluency check

## Templates

- `templates/calibration.md` — Stage 1 fill-in template
- `templates/session-log.md` — Per-session log format
- `templates/artifact.md` — Artifact format options with examples
