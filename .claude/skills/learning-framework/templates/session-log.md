# Session Log Template

Used during a session to track loops, probes, calibration checks, and decisions. Claude maintains this in working memory across the session; the relevant parts feed into the Artifact (Stage 5) and Profile Update (Stage 6).

```markdown
# Learning Session — [date]

## Stage 1: Calibration
- Subject:  [topic]
- Source:   [name]
- Why:      [...]
- Anchor:   [...]
- Angle:    [...]
- Depth:    [...]
- Budget:   [N min, energy: X]
- Artifact: [...]
- Consistency flags: [none / list]

## Stage 2: Segmentation
- Native structure: [N units]
- Plan: [deep / skim / skip breakdown]
- Total loops: N
- K (running cal interval): 3
- Source-artifact match: ✅ / ⚠ [note]

## Stage 3: Loops

### Loop 1 — [chunk name]
- Map: [concepts]
- Translate: [anchor mapping used]
- Probe: [probe question]
- Probe result: ✅ pass / ⚠ patched / ❌ parked
- Patch attempts: [if any]
- Time: [N min]

### Loop 2 — [chunk name]
...

## Stage 4: Running Calibration Checks

### After Loop 3
- Energy: [1–5]
- Probe pass rate (last 3): [X/3]
- Decision: [continue / shrink chunks / switch angle / stop / renegotiate frame]

### After Loop 6
...

## Stage 5: Artifact
[The actual artifact, in the format declared in Stage 1]

### Honest Gaps
- [What was parked, why]
- [What depth wasn't reached]
- [What would need a future session]

## Stage 6: Profile Update (proposed entry)
- Domain: [...]
- Chunk size observed: [...]
- Sustain window: [...]
- Angles worked / didn't: [...]
- New prerequisites confirmed: [...]
- New known gaps: [...]
```

---

## Notes

- The session log is **internal** to Claude. Vineel sees the artifact and the profile update, not the full log, unless he asks.
- Time per loop matters for sustain-window calibration. Estimate even if not precise.
- "Parked" loops always need a one-line reason; never silently abandon.
