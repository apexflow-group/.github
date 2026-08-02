# .github — org-wide defaults

Default community health files for every `apexflow-group` repo that doesn't
override them: issue forms, PR template, and the canonical label set.

**The rules these files implement live in
[`handbook/TASK_PROCESS.md`](https://github.com/apexflow-group/handbook/blob/main/TASK_PROCESS.md)**
— title prefixes, the six label dimensions, the issue contract, splitting,
dependencies, and what is enforced versus what needs a human. Read it before
changing anything here.

| Path | What it is |
|---|---|
| `ISSUE_TEMPLATE/` | Seven issue forms, one per `type/*`: task, feature, bug, ops, research, decision, epic. Blank issues are off |
| `PULL_REQUEST_TEMPLATE.md` | Default PR template |
| `labels.yml` | **Canonical label taxonomy** — the single source. Never create a label in the UI |
| `sync_labels.py` | Pushes `labels.yml` to every org repo; deletes the retired GitHub defaults |
| `profile/README.md` | Public org profile |

```bash
python3 ~/workspace/apexflow/.github/sync_labels.py --dry-run   # preview
python3 ~/workspace/apexflow/.github/sync_labels.py             # apply
python3 ~/workspace/apexflow/handbook/tools/task_lint.py        # audit issues
```

**This repo is public.** Nothing product-confidential goes in it — label names
and form prompts only.
