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
```

Every stage has an exit criterion. Do not advance silently.

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

**Exit criterion:** Profile updated; session ends.

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

## Templates

- `templates/calibration.md` — Stage 1 fill-in template
- `templates/session-log.md` — Per-session log format
- `templates/artifact.md` — Artifact format options with examples
