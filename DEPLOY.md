# Deploy Runbook — The Learning Lab

The site auto-deploys via Vercel whenever `main` on this GitHub repo changes.
There is **no automatic push from Claude's sandbox** — the container resets every
session and never persists the GitHub token. So every session that adds/edits a
module MUST run the steps below.

## Required first step EVERY session (before any push)

The git remote must have the token embedded, or `git push` fails with
`could not read Username for 'https://github.com'`.

```bash
cd /home/claude/learning-lab          # (or wherever the repo is cloned this session)
git remote set-url origin "https://<GITHUB_TOKEN>@github.com/rajeshsoora/the-learning-lab.git"
```

The token is a GitHub Personal Access Token with `repo` scope, supplied by Rajesh
in chat. It is never stored in the repo or in skill files.

## Standard module-publish flow

```bash
git add <new-module>.html index.html roadmap.html
git commit -m "feat: Module NN — <title>"
git push origin main
```

Vercel redeploys within ~30–60s. Verify the live site:
https://the-learning-lab-vgq2.vercel.app

## When publishing a new module, always update THREE files

1. `<module-slug>.html`  — the new module artifact
2. `index.html`          — flip the module card from `soon:true` to live (add href, date,
                           move the `latest:true` flag to the new module)
3. `roadmap.html`        — change the module's `status` from `locked`/`next` to `done`,
                           set the next module's status to `next`, progress bar auto-updates

## Verifying a push actually landed (do this, don't assume)

```bash
git rev-parse HEAD                    # local commit
git ls-remote origin main             # remote commit — must MATCH local
```

If they match, the push succeeded and Vercel will deploy. If they differ, the push
did not land — re-check the remote URL has the token.
