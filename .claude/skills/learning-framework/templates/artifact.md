# Artifact Formats

The artifact is the durable output of a session — the thing that proves understanding happened and stores it for later retrieval. **It's also the specification that drives Stages 2–4 backward**: source segmentation, loop count, probe types, and depth all collapse toward producing the artifact.

Pick the format in Stage 1 before any reading begins. If you can't name an artifact, you don't yet have a clear enough goal to run a session.

---

## Format options

### 1. One-paragraph compression
**Shape:** ≤150 words. No jargon Vineel doesn't already own. Compresses the source into the spine.

**When to use:** Quick literacy, decision context, refresher for something half-known.

**Example:**
> Raft achieves consensus by electing a single leader who serializes all writes. Followers replicate the leader's log; once a majority acknowledges an entry, it's committed. If the leader dies, followers detect timeout, increment a term number, and one becomes a candidate — winning the vote requires a majority. Term numbers prevent split-brain because old leaders learn they're outdated when they see a higher term. Compared to Paxos, the design choice is clarity over flexibility: a single leader per term simplifies reasoning at the cost of leader-bottleneck throughput. Used in etcd, Consul, and CockroachDB. Failure modes worth knowing: leader thrash under flaky networks, slow followers blocking commit, and split-vote in even-numbered clusters.

---

### 2. Diagram
**Shape:** Mermaid, ASCII, or sketch. Labeled with Vineel's anchors, not the source's native vocabulary.

**When to use:** Spatial / structural / flow-based concepts. Architecture, state machines, data flow, lifecycle diagrams.

**Example structure:**
```
[Client] → [Leader (Raft)] ─append→ [Followers]
                │                       │
                └──── acks ────────────┘
                           │
                    majority? → commit → apply to state machine
```

---

### 3. Predictions
**Shape:** 3–5 testable predictions that the new mental model lets Vineel make. Each prediction states: situation → predicted outcome → why.

**When to use:** When the goal is to internalize a *model* that's used to forecast or evaluate (theory, economics, system behavior).

**Example:**
1. *If a Raft cluster has 4 nodes and 2 are partitioned*, writes stall (no majority). → Because commits require >N/2 acks.
2. *If you add a node to a 3-node cluster mid-write*, joint consensus is needed during transition. → Otherwise a majority of the old config could disagree with a majority of the new.
3. *If leader's disk is slow*, the whole cluster's write throughput drops. → All writes serialize through the leader.

---

### 4. Working code
**Shape:** Runnable code that implements the concept. Comments tie code lines back to the concept.

**When to use:** `build` agenda, technical depth, anything where the bug-free implementation IS the understanding.

**Notes:** Test it. If it doesn't run, the loop didn't actually pass.

---

### 5. Explain-to-junior script
**Shape:** A ~60-second spoken explanation aimed at a smart engineer who hasn't seen the concept. Includes (a) the analogy, (b) why it matters, (c) one common misconception corrected.

**When to use:** `teach` depth, interview prep where you'll be expected to explain.

**Example structure:**
> [10s hook with anchor] "You know how X works? Y is the same pattern but for Z."
> [20s mechanism] "Specifically, it does A, then B, then C..."
> [15s why it matters] "Without this, [failure mode]."
> [15s misconception] "People often think Y means M, but it actually means N because..."

---

### 6. Three questions answered
**Shape:** Three non-trivial questions that the source addresses + Vineel's answer to each + a one-line justification from the source.

**When to use:** Interview prep, study sessions, exam-style verification.

**Example:**
1. *Q: Why does Raft use term numbers instead of timestamps?*
   A: Timestamps require synchronized clocks; term numbers are local-monotonic and survive arbitrary clock skew. Source: §3.3.

2. *Q: What happens to in-flight writes during a leader election?*
   A: They're lost — clients must retry. Raft guarantees committed entries persist, not in-flight ones. Source: §5.4.

3. *Q: Why is the recommended cluster size odd?*
   A: Even-numbered clusters tolerate the same number of failures as odd-1, with worse split-vote risk. Source: §5.6.

---

### 7. Decision criteria
**Shape:** Explicit criteria (in Vineel's voice) for when to use / not use the concept. Often 2–4 bullet points each side.

**When to use:** When the learning is for a real decision (tool choice, architecture call, investment).

**Example:**
> **Use Raft when:**
> - Strong consistency required across a small cluster (3–9 nodes)
> - Write throughput is moderate (single-leader bottleneck acceptable)
> - You can tolerate election downtime (typically 100ms–1s)
>
> **Don't use Raft when:**
> - You need high write throughput across many regions (use a leaderless system)
> - Eventual consistency is acceptable (use Dynamo-style)
> - Cluster size > ~15 (election + replication overhead grows)

---

### 8. Steelman + critique
**Shape:** Strongest version of the source's argument (1 paragraph), strongest counter-argument (1 paragraph), Vineel's resolution (1 paragraph).

**When to use:** Contested / opinionated topics (economics, philosophy, methodology debates).

---

## Composite artifacts

For longer sessions, combine formats. Common combinations:

- **Diagram + 3 questions** — visual model + verification
- **Compression + decision criteria** — for "should I use this" sessions
- **Working code + explain-to-junior** — for `teach` depth on technical topics
- **Predictions + steelman** — for theory and economics

If combined, declare the combination in Stage 1.

---

## The Honest Gaps section

**Every artifact ends with a "Honest Gaps" section.** Format:

```
## Honest Gaps
- Parked: [concept] — reason: [missing prereq / off-path / out of budget]
- Depth note: reached `use` on X but only `recognize` on Y (declared target was `use`)
- Future session: would need [source] to get to [depth] on [topic]
```

This is non-negotiable. Pretending coverage is worse than acknowledging gaps — it corrupts the profile and misleads future sessions.
