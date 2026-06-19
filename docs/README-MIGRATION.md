# Learning Framework — Claude Code Migration

This bundle moves Rajesh's `/learning-framework` skill (and its state files) into a
git repo so Claude Code can run learning sessions and publish to the-learning-lab
without the sandbox-reset / token re-embedding workaround.

## What's in here

```
.claude/skills/learning-framework/
├── SKILL.md
├── references/
│   ├── probe-types.md
│   ├── profile-schema.md
│   ├── profile.md              <- running calibration state
│   └── source-segmentation.md
└── templates/
    ├── artifact.md
    ├── calibration.md
    └── session-log.md
```

## What's MISSING — you need to add these yourself

1. **`mdm-learning-path.md`** — the MDM/Spark progress tracker (module 00/01 done,
   02-08 pending). It wasn't present in this sandbox at migration time, so grab the
   latest copy from wherever you have it (likely `/mnt/user-data/outputs/` in a
   recent claude.ai session, or re-export it there first) and drop it at:
   `.claude/skills/learning-framework/references/mdm-learning-path.md`

   (Since this migration, the skill became multi-roadmap: this file now lives at
   `.claude/skills/learning-framework/references/roadmaps/mdm-spark.md`, and any
   future topic gets its own `references/roadmaps/<track-id>.md` — see root
   `CLAUDE.md`. This section is left as historical record of the original migration.)

2. **Your GitHub repo** — this bundle is standalone. To use it with the-learning-lab:
   ```bash
   git clone https://github.com/rajeshsoora/the-learning-lab.git
   cp -r /path/to/this/bundle/.claude the-learning-lab/
   cd the-learning-lab
   git add .claude
   git commit -m "Add learning-framework skill for Claude Code"
   git push
   ```
   No token URL surgery needed — Claude Code uses your normal local git auth.

## How it works in Claude Code

- Claude Code scans `.claude/skills/` at startup and auto-discovers `learning-framework`
  by its SKILL.md description — same trigger logic as before, no manual invocation needed.
- `references/profile.md` and `references/mdm-learning-path.md` are now plain
  version-controlled files. Update them with normal edits + `git commit`, no heredoc-append
  bash gymnastics required.
- Session-start / session-end rituals are unchanged: read the learning path at the top
  of a session, update it at the end.
- For the Learning Lab publish step specifically: once you're inside the actual repo
  clone, `git push` just works (your machine, your credentials) — `DEPLOY.md`'s
  remote-url-with-token step becomes unnecessary. Keep DEPLOY.md for reference but the
  token-embedding step is claude.ai-sandbox-specific and can be skipped in Claude Code.

## Notion (Python/PipelineEngine track)

Unaffected — Notion updates still happen via whatever client has the Notion MCP
connector enabled. If Claude Code doesn't have that connector, keep using claude.ai
for Notion log updates, or connect Notion's MCP server in Claude Code if available.
