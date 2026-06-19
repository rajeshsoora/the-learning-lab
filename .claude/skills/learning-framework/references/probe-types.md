# Probe Types

Probes are how Stage 3c validates that understanding actually happened. The probe type is **derived from the depth target** declared in Stage 1 — not chosen arbitrarily.

The principle: a probe must be the kind of question that the declared depth would let you answer. If you only need `recognize` depth, a recall probe is enough. If you declared `teach` depth, only an explain-to-novice probe is honest validation.

---

## Depth: `recognize`

**What it means:** You can identify the concept when you see it. You know what it is. You can pick it out of a list.

**Probe shape — Recall:**
- "What is [concept]?"
- "Which of these is an example of [concept]?"
- "Define [concept] in one sentence."
- "Where in this diagram is [concept]?"

**Pass criterion:** Vineel produces a correct identification or definition. Doesn't need to apply it or teach it.

**Typical fit:** Skimming a field for general literacy, scanning a domain before deciding to go deeper, breadth-first context.

---

## Depth: `use`

**What it means:** You can apply the concept to a novel case. You can predict what it implies. You can debug or design with it.

**Probe shape — Application:**
- "Apply [concept] to this scenario: [novel case Vineel hasn't seen]."
- "Predict what happens if [variable] changes — and why."
- "Here's a system with a bug. Use [concept] to locate it."
- "Design a small thing that uses [concept]."
- "When would you NOT use [concept]? What's the failure mode?"

**Pass criterion:** Vineel's prediction or design is correct AND the reasoning shows the concept is doing the work (not pattern-matching).

**Typical fit:** Learning something to build with it, interview prep where you'll be asked to apply, evaluating tools/decisions.

**Note on novel cases:** The case must be one Vineel hasn't seen in the source. Recycling the source's example tests memory, not understanding.

---

## Depth: `teach`

**What it means:** You can explain the concept to someone who doesn't have it yet. You can anticipate their confusions. You can pick the right analogy.

**Probe shape — Explain-to-novice:**
- "Explain [concept] to a junior engineer in 60 seconds, no jargon."
- "A smart non-expert asks 'why does this matter?' — answer them."
- "Teach [concept] using only things in [Vineel's anchor domain]."
- "What's the most common misconception about [concept]? How would you correct it?"

**Pass criterion:** The explanation is (a) accurate, (b) uses no unexplained jargon, (c) names the right analogy or anchor, (d) anticipates at least one likely confusion.

**Typical fit:** Genuine mastery, becoming the go-to person, writing about it publicly, mentoring.

**Note on teach depth:** This is expensive. Don't declare it casually — it can take 2–4× the time of `use` depth. If budget < 30 min, drop to `use`.

---

## Patch sequence when a probe fails

| Attempt | Projection |
|---|---|
| Initial | Whatever Stage 1 angle declared |
| Patch 1 | Switch projection: formal ↔ analogy ↔ comparative |
| Patch 2 | (If first patch failed) — switch again, exhaust projections |
| Two patches failed | Escalate to Stage 4 immediately. Likely missing prerequisite or wrong frame. |

---

## What a passing probe looks like (examples)

**Recognize-depth pass:**
> Vineel: "Idempotency means an operation produces the same result whether called once or many times. Like PUT in HTTP vs POST."
> ✅ Pass — definition correct + anchor used.

**Use-depth pass:**
> Probe: "You're designing a payment retry mechanism. Apply idempotency."
> Vineel: "I'd attach an idempotency key per request, store the result keyed by it for some TTL, and on retry return the stored result instead of re-charging. Without it, retries would double-charge on transient failures."
> ✅ Pass — applied to novel case, names failure mode, reasoning is correct.

**Teach-depth pass:**
> Probe: "Explain idempotency to a junior engineer who's never heard the term."
> Vineel: "Imagine the elevator button — pressing it five times doesn't call five elevators. That's idempotent: same outcome regardless of how many times you press. In APIs, we want the same property for retries. Without it, your retry logic can charge someone's card twice if a response gets lost. The common misconception is that idempotent means 'safe' or 'read-only' — it doesn't. It means 'repeatable without extra effect.'"
> ✅ Pass — analogy is apt, explains why it matters, anticipates the misconception.

---

## Anti-patterns

- **The leading probe:** "So idempotency means same-result-on-retry, right?" — answers itself. Useless.
- **The source-recycled probe:** Using the exact example from the source. Tests memory, not understanding.
- **The vague pass:** Accepting "yeah I get it" without a concrete answer. Always require an artifact-sized answer.
- **The over-probe:** Asking 5 probes per concept. One good probe per concept; move on.
