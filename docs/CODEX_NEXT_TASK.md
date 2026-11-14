# Current Codex task — question-predictor

**Status:** Completed — awaiting next task.
**Task:** Phase 1A — Source Registry and PYQ Availability Audit.
**Full instructions:** [Phase 1A Codex implementation task](prompts/2026-11-07-phase-1a-source-registry-audit.md)
**Repository:** [cleanerAbhigyan/question-predictor](https://github.com/cleanerAbhigyan/question-predictor)
**Active branch:** `feature`; continue on the **existing [PR #1](https://github.com/cleanerAbhigyan/question-predictor/pull/1)**. Do not create another branch/PR, force-push or merge into `main`.

**Completion evidence:** Phase 1A metadata CLI/registry, audit reports, safe acquisition guide and tests/CI are implemented. See [development log](DEVELOPMENT_LOG.md), [availability report](SOURCE_AUDIT_REPORT.md) and [format](SOURCE_REGISTRY_FORMAT.md). Six landing leads and 16 checked blank Notion slots establish no acquired or approved paper. The archived task remains unchanged. Stop pending a new task; do not start Phase 1B.

## How to run

1. Confirm this file says **Ready for implementation**. If it says **Completed — awaiting next task**, stop; do not rerun a previous milestone.
2. Check current local Git state and preserve uncommitted work. On the matching `feature` branch, safely fetch and fast-forward `origin/feature` if appropriate. GitHub updates are not automatically in the VS Code checkout.
3. Read `AGENTS.md`, `README.md`, `docs/PROJECT_CONTEXT.md` and the **entire linked Phase 1A task**. Read the referenced architecture, schema, roadmap, source verification and Phase 0 development log. Follow the complete task, do not merely summarize it.
4. Implement **only** Phase 1A: a tested metadata-only research source registry, PYQ availability audit, acquisition guide and basic CI, as specified. Do not download copyrighted PDFs by default, claim paper authenticity, implement model/backtesting, or change `rbi-mock-app`.
5. Run and document actual checks, archive the task, update development docs, commit and push to the same `feature` branch/PR #1. No merge or force-push.
6. Only after genuine implementation and checks pass, mark this file **Completed — awaiting next task** and record results in `docs/DEVELOPMENT_LOG.md`. Do not automatically start another milestone.

## ChatGPT → GitHub → VS Code

The full task lives in GitHub; the user only needs a short VS Code instruction to read this file. After Codex's push, ChatGPT reviews the real GitHub changes and current CI; Notion progress updates are handled separately when requested.

**Baseline:** Phase 0 documentation completed on commit `b7f43e4777ab1080396df830167b2b25fb8cfddc`, PR #1 open. No historical PYQs, acquired source PDFs, predictive software, backtests or generated questions are claimed. Publishing this task does not implement Phase 1A.
