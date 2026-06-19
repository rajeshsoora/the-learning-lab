# Calibration Template (Stage 1)

Copy-paste this when starting a session if you want to pre-fill the frame yourself instead of being asked.

```
Subject: [topic or source name]
Source:  [book chapter / blog URL / video link / paper title / repo]

Why:     [decision / build / interview / curiosity / teach]
Anchor:  [adjacent thing I already know well]
Angle:   [first-principles / mechanistic / comparative / applied / adversarial / historical]
Depth:   [recognize / use / teach]
Budget:  [N minutes, energy: high/med/low]
Artifact: [what I'll produce at the end]

Run learning-framework.
```

---

## Examples

### Example 1: Backend interview prep, dense paper

```
Subject: Raft consensus algorithm
Source:  https://raft.github.io/raft.pdf

Why:     interview prep — likely system design question
Anchor:  I know Paxos at recognize level; distributed systems background strong
Angle:   mechanistic
Depth:   use
Budget:  60 min, energy med
Artifact: 60-second whiteboard explanation + 3 likely interview questions with answers

Run learning-framework.
```

### Example 2: Quick decision check, blog post

```
Subject: When to use vector DB vs Postgres pgvector for RAG
Source:  https://[blog-url]

Why:     decision for portfolio project
Anchor:  RAG production experience at Kore.ai; Postgres strong; pgvector recognize-level
Angle:   comparative
Depth:   use
Budget:  20 min, energy high
Artifact: One-paragraph decision criteria + which I'd pick for my multi-agent finance project

Run learning-framework.
```

### Example 3: Going deep, full chapter

```
Subject: LSM trees — write path
Source:  Database Internals (Petrov), Ch 7
 
Why:     build — implementing a toy storage engine
Anchor:  B-trees at use level; SSTables at recognize level
Angle:   mechanistic
Depth:   teach
Budget:  90 min, energy high
Artifact: Working Python prototype of write path (memtable + WAL + flush) + diagram

Run learning-framework.
```

### Example 4: Skimming for literacy

```
Subject: Modern monetary theory (MMT)
Source:  [video lecture URL, ~45 min]

Why:     curiosity / general literacy for macroeconomic positioning
Anchor:  Mainstream macro at use level; Austrian school at recognize level
Angle:   comparative (vs mainstream)
Depth:   recognize
Budget:  30 min, energy med
Artifact: 5 sentence summary of core claims + how it differs from mainstream + steelman + main critiques

Run learning-framework.
```

---

## Notes on filling this in

- **Why:** Be specific. "Curiosity" is fine but "decision for X project" is much better — it lets segmentation prune aggressively.
- **Anchor:** Name the strongest adjacent thing. "I know X at use level" is more useful than "I'm a backend engineer".
- **Angle:** If unsure, default to `mechanistic` for technical topics and `comparative` for theory/opinion topics.
- **Depth:** Be honest. Over-declaring depth ("teach") wastes 2–4× the time. Most learning sits at `use`.
- **Budget:** Pad by 20% for unfamiliar domains. Energy is real — don't lie to yourself.
- **Artifact:** The single most important field. If you can't name an artifact, you don't yet have a clear enough goal to run a session.
