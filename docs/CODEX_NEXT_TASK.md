# Current Codex task — question-predictor

**Status:** Ready for implementation (not completed).
**Task:** Phase 0 — Repository foundation and technical research specification.
**Full instructions:** [Phase 0 Codex implementation task](prompts/2026-11-07-phase-0-repo-foundation.md)
**Repository:** [cleanerAbhigyan/question-predictor](https://github.com/cleanerAbhigyan/question-predictor)
**Active branch:** `feature` (already exists). Do not create a new branch.

## Codex execution procedure

1. Verify this file still says **Ready for implementation**. If it says **Completed — awaiting next task**, STOP; never rerun a completed milestone.
2. In the `question-predictor` VS Code workspace check the worktree/remote and safely sync `origin/feature` if clean, using `git fetch origin` then `git pull --ff-only origin feature` on the matching branch. Do not discard local edits.
3. Read `AGENTS.md`, `README.md`, `docs/PROJECT_CONTEXT.md` and the **entire** linked Phase 0 task. Follow it in full; don't just summarize.
4. Implement **only** the current task; test, document, commit and push to `feature`. No new development branch, no force push and no merge into `main`. Open/update the predictor's one PR as directed in the task, if possible.
5. After actual completion mark this file **Completed — awaiting next task**, report evidence in `docs/DEVELOPMENT_LOG.md`, commit and push those status changes with the work. Do not select another task yourself.

## ChatGPT → GitHub → VS Code

ChatGPT publishes the comprehensive, sanitized milestone prompt **in GitHub**, updates this single entrypoint to link it, and supplies only a very short VS Code instruction. Codex must read the current remote prompt and project files rather than rely on prior chat context. GitHub updates do not automatically appear in local files: pull safely on the correct branch. ChatGPT later reviews the actual pushed diff/CI, and updates existing Notion research records when synchronization is requested.

**Baseline:** As of the task publication, the predictor has no validated historical corpus, model implementation or completed backtest. The branch creation and task publication are not Phase 0 implementation.
