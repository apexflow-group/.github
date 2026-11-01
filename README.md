# .github — org-wide defaults

> **Status:** CANONICAL · **Owner:** .github · **Last-verified:** 2026-10-31 (every claim below against `git ls-tree origin/main`, `ISSUE_TEMPLATE/config.yml`, `sync_labels.py --dry-run` and `gh repo list`, 2026-10-31)

Default community health files for every `apexflow-group` repo that doesn't
override them: issue forms, PR template, and the canonical label set.

**The rules these files implement live in
[`handbook/TASK_PROCESS.md`](https://github.com/apexflow-group/handbook/blob/main/TASK_PROCESS.md)**
(the link opens for org members only) — title prefixes, the six
label dimensions, the issue contract, splitting, dependencies, and what is
enforced versus what needs a human. Read it before changing anything here.

| Path | What it is |
|---|---|
| `ISSUE_TEMPLATE/` | Seven issue forms, one per `type/*`: task, feature, bug, ops, research, decision, epic. Blank issues are off |
| `PULL_REQUEST_TEMPLATE.md` | Default PR template |
| `labels.yml` | **Canonical label taxonomy** — the single source. Never create a label in the UI |
| `sync_labels.py` | Pushes `labels.yml` to every org repo (`--dry-run` writes nothing); deletes the retired GitHub defaults when unused. A label on a repo but not in `labels.yml` is **reported, never deleted** |
| `profile/README.md` | Public org profile |

```bash
python3 ~/workspace/apexflow/.github/sync_labels.py --dry-run   # preview
python3 ~/workspace/apexflow/.github/sync_labels.py             # apply
python3 ~/workspace/apexflow/handbook/tools/task_lint.py        # audit issues
```

**This repo is public.** Nothing product-confidential goes in it — label names,
form prompts, a PR template and the sync script only.

**Known mismatch:** the comment at the top of `labels.yml` tells you to run
`sync_labels.sh`. There is no such file; the script is `sync_labels.py` (the
commands above).
