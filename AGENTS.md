# The Learning Lab

> **START HERE — read before doing anything in this repo.**
> If Rajesh asks to learn, study, understand, prep on, or build a module for
> any topic: before writing or editing anything, open and follow
> `.claude/skills/learning-framework/SKILL.md` in full, step by step. That
> file is the protocol — not optional reference material. Do not skip to
> writing a module file directly.

Rajesh's general-purpose, on-the-job learning system. The learning-framework
skill itself is **domain-agnostic** — it works for any field Rajesh wants to
upskill in. The repo runs two systems together: a structured learning
protocol that calibrates what Rajesh actually knows and runs real sessions
against sources, and a static website that publishes each session's output
as an interactive module, organized as one **roadmap per topic/track**. The
website is a side effect of learning, not the goal — if a module is on the
site, it's because a real calibrated session produced it.

**MDM / Spark / Entity Resolution is just the first roadmap.** It happens to
be the most built-out today (5 of 9 modules live), but the framework and the
website are both designed to carry any number of additional roadmaps —
Python/Backend is already stubbed in as the second track. When Rajesh wants
to upskill in a new field, the workflow is: give the topic(s) → break it into
phases/modules (a new roadmap) → run learning sessions per module → each
session publishes a module to the site under that roadmap's track.

## Two systems

**1. Learning Framework** — `.claude/skills/learning-framework/`
A structured protocol, fully defined in `SKILL.md`, that runs a 7-stage
pipeline: Calibration → Segmentation → Session Loop (Map→Translate→Probe→
Patch) → Running Calibration → Artifact Assembly → Profile Update → Publish.

**This is mandatory, not optional packaging.** Any agent, on any platform,
MUST read `.claude/skills/learning-framework/SKILL.md` in full and follow it
step by step before producing or updating a learning module — regardless of
whether the platform has an automatic skill-trigger mechanism. Claude Code
happens to auto-load this file via its `Skill` tool when it detects learning
intent; a platform without that mechanism must instead treat "Rajesh wants
to learn/study/understand/prep on something" as the same trigger and open
`SKILL.md` itself before doing any work. Skipping straight to writing a
module without running the protocol in `SKILL.md` is not a valid shortcut.

The protocol reads and writes:
- `references/profile.md` — **cross-domain** calibration data: what chunk
  size works, what angles land, confirmed prerequisites, known gaps, session
  log, organized into one section per domain studied so far (e.g.
  `spark/data-engineering`). This is "where Rajesh currently stands," and it
  accumulates across every roadmap, not just one.
- `references/roadmaps/<track-id>.md` — one file per roadmap: the module
  curriculum for that topic (phases, modules, status, sequencing rationale,
  carried-forward gaps). `mdm-spark.md` is the first one. A new topic gets
  its own file here, e.g. `references/roadmaps/python-backend.md`.

**2. Website** — `modules/`, `index.html`, `roadmap.html`
A static HTML site (no build step, no framework) deployed to Vercel on push
to `main`. Both shell pages are **multi-track**, keyed by the same track
`id` (e.g. `mdm-spark`, `python-backend`):
- `index.html` — landing page, `TRACKS` array, one entry per track with its
  module list (a tab switcher renders each track's cards).
- `roadmap.html` — full phase-by-phase plan, `ROADMAPS` array, one entry per
  track with its phases (a matching tab switcher renders each track's plan;
  a track with no phases yet shows a "hasn't been broken into modules"
  placeholder instead of an empty page).

A roadmap/track only fully exists once it has entries in all three places:
`references/roadmaps/<id>.md` (skill side), `TRACKS` in `index.html`, and
`ROADMAPS` in `roadmap.html` (website side). Module files themselves always
live under `modules/`, regardless of which track they belong to.

## The end-to-end orchestration flow

This is the loop that ties calibration to website development for **any**
topic — it's what "using this learning framework to build the website"
actually means in practice, for the current MDM roadmap or a future one:

```
Rajesh signals learning intent (existing roadmap, or a new topic to plan)
        │
        ▼
Stage 1  Calibration       read profile.md for this domain → declare Why/
                            Anchor/Angle/Depth/Budget/Artifact. Artifact =
                            "next module HTML file" for an existing roadmap,
                            or "a new roadmap file" if planning a new topic.
        │
        ▼
Stage 2  Segmentation       chunk the source against the roadmap's next
                            module and its declared topics. If no roadmap
                            exists yet for this topic, this stage is where
                            the topic gets broken into phases/modules and
                            written to references/roadmaps/<new-id>.md.
        │
        ▼
Stage 3  Session Loop       Map → Translate → Probe → Patch, once per chunk,
                            until every concept the module needs is probed
        │
        ▼
Stage 4  Running Calibration   energy + understanding checks every K loops
        │
        ▼
Stage 5  Artifact Assembly  build the actual module content (still just
                            content at this point, not yet the HTML file)
        │
        ▼
Stage 6  Profile Update     append session to profile.md (this domain's
                            section); update references/roadmaps/<id>.md
                            (module done, gaps, next)
        │
        ▼
Stage 7  Publish            write modules/<slug>.html in the established
                            pattern → update index.html TRACKS + roadmap.html
                            ROADMAPS for this track's id → commit/push per
                            docs/DEPLOY.md → verify the push landed → Vercel
                            deploys
```

Stage 7 only fires when the Stage 1 artifact is a website module. Other
artifacts (a compression, a diagram, working code, etc.) stop at Stage 6 —
see `SKILL.md` for the general-purpose pipeline.

## Adding a brand-new roadmap (new topic, not yet on the site)

1. Rajesh gives the topic(s) to learn.
2. Break it into phases and modules (same shape as the MDM roadmap: phase →
   modules → topics/tags → "unlocks" description), and write it to a new
   file `.claude/skills/learning-framework/references/roadmaps/<track-id>.md`.
3. Add a matching track entry to `TRACKS` in `index.html` (modules can start
   as `soon:true` placeholders) and to `ROADMAPS` in `roadmap.html` (phases
   can start empty — the UI shows a "not broken into modules yet" state).
4. From there, every learning session against that topic runs Stages 1–7
   exactly as the MDM roadmap does, publishing into that track's modules.

## Repo map

```
AGENTS.md                                  this file — read this first, any platform
CLAUDE.md                                  Claude Code auto-load pointer -> @AGENTS.md
.claude/skills/learning-framework/         the learning protocol (skill) — domain-agnostic
  SKILL.md                                 7-stage pipeline definition
  references/
    profile.md                             cross-domain calibration state
    roadmaps/
      mdm-spark.md                         MDM/Spark module curriculum + progress
      <new-topic>.md                       future roadmaps go here, one file each
    profile-schema.md                      schema for profile.md
    probe-types.md                         probe shapes per depth target
    source-segmentation.md                 chunking rules per source type
  templates/
    calibration.md, artifact.md, session-log.md
modules/                                   published module HTML files (all tracks)
  entity-resolution-walkthrough.html       mdm-spark Module 00
  nested-types-decision-card.html          mdm-spark Module 01
  string-processing-normalization.html     mdm-spark Module 02
  window-functions.html                    mdm-spark Module 03
  match-scoring-classification.html        mdm-spark Module 04
index.html                                 landing page (TRACKS registry, multi-track)
roadmap.html                                phase-by-phase plan (ROADMAPS registry, multi-track)
vercel.json                                static deploy config
docs/
  DEPLOY.md                                publish runbook (commit/push/verify)
  README-MIGRATION.md                      history: sandbox → Claude Code migration
```

## Conventions

- **Module file naming:** `modules/<topic-slug>.html`, one self-contained
  file (inline CSS/JS, no external deps beyond what's already used),
  regardless of which track it belongs to — there's no per-track
  subdirectory under `modules/`.
- **Module internal pattern** (formalized as Stage 7's build step in
  `SKILL.md`): an **invariant core** present in every module — motivating
  example/anchor tied to something Rajesh already knows → worked mechanism →
  mandatory **Honest Gaps** section — plus an **optional menu** (decision
  criteria, runnable code pattern, interactive widget, climax/gotcha framing,
  scenario-based self-test) included only when the specific topic actually
  calls for it. Stage 7 runs a quick pre-build check to decide which optional
  sections apply before the module is written — this is not a fixed
  checklist every module follows verbatim.
- **Three registries, one truth, per track:** a track's roadmap file
  (`references/roadmaps/<id>.md`), `index.html` `TRACKS`, and `roadmap.html`
  `ROADMAPS` all describe the same modules for that track `id`. Adding or
  changing a module touches all three — never just one.
- **Links between modules and the shell:** module files use `../index.html`
  and `../roadmap.html` to get back to the shell pages (they live one
  directory down, in `modules/`).

## Where state lives

- **What Rajesh currently knows / how he learns, across all domains:**
  `references/profile.md`
- **What's done / what's next, per topic:**
  `references/roadmaps/<track-id>.md`
- **Everything else** (HTML content, exact wording, past deploys): git history
- **How to actually publish:** `docs/DEPLOY.md`
