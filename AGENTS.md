# Development Agent Instructions — question-predictor

This is an independent future model/research repository. Do **not** merge it with `../rbi-mock-app` or create cross-repository runtime coupling.

**Active development branch: `feature` — reuse it for all upcoming phases.** Do not create a branch or pull request for each milestone. After the first implementation, maintain one predictor PR from `feature` into `main`; never merge without explicit user approval.

**Task entrypoint:** Read `docs/CODEX_NEXT_TASK.md` first. It points to the complete current milestone prompt archived in `docs/prompts/`. When the task is marked completed, STOP; do not rerun or auto-start the next task. Always prefer the current GitHub task files over previously pasted prompts.

Read `README.md`, `docs/PROJECT_CONTEXT.md`, research docs and prompt archive before implementation. Check `pwd`, `git status -sb`, `git remote -v`, current branch, upstream and latest history. Safely fetch/pull on `feature` when appropriate without overwriting uncommitted work. Do not write to `main` or another repository.

For every actual development milestone:

1. Keep the full sanitized task in `docs/prompts/YYYY-MM-DD-short-task.md`; ChatGPT publishes and links the task in GitHub before the VS Code agent is run. Do not duplicate existing archives.
2. Implement only the linked task and maintain the appropriate tests. Do not invent question papers, answer keys, prediction results, topic counts, exams or backtest scores.
3. Update `README.md`, `docs/PROJECT_CONTEXT.md`, `docs/ROADMAP.md`, and `docs/DEVELOPMENT_LOG.md` to describe what actually happened.
4. Run appropriate checks, commit code/tests/prompts/docs, push to `origin feature` and update the one open predictor PR if it exists. Never force-push or merge. Verify latest remote head/CI; report branch, SHA, checks, push and PR outcomes honestly.
5. When the current milestone is truly finished, mark `docs/CODEX_NEXT_TASK.md` **Completed — awaiting next task**, and stop. The next task will be published after GitHub review.
6. Keep official/memory-based/coaching/LLM-generated question sources distinct. No invented PYQs. Preserve blind held-out-year backtesting and reproducible source IDs.
7. Prepare only a future versioned schema/approved data export for the independent simulator; no sibling-repository modifications.
8. Do not publish secrets, personal information, restricted papers or redistribution-prohibited data.

Notion is the authoritative research/planning specification, GitHub is the implementation record, and ChatGPT reconciles both when asked. No automatic real-time three-way synchronization is implied. Current notices, data availability and progress must be verified rather than assumed.

## Phase 0 foundation and handoff

The proposed research contracts live in [Architecture](docs/ARCHITECTURE.md), [Data schema](docs/DATA_SCHEMA.md), [Source verification](docs/SOURCE_VERIFICATION.md), [Backtest protocol](docs/BACKTEST_PROTOCOL.md) and [Export contract](docs/EXPORT_CONTRACT.md). They are designs, not implemented validators or running services. Read the [roadmap](docs/ROADMAP.md) before future implementation, but never select its next phase without a newly published task.

Keep source category, source authentication, transcription verification, answer correctness and usage rights separate. Unknown values must remain unknown. Never infer redistribution permission from an official-looking source or a readable download. Examples must use an explicit example-only marker and reserved `EXAMPLE-` identifiers, and must fail historical-PYQ admission.

Keep Phase I separate from Phase II; within Phase II isolate ESI, Finance & Management and English Writing. Do not assume any 2027 dates, eligibility, pattern or marking without official notice evidence. Preserve the Govt 60% common banking / 40% RBI-specific study allocation when referenced; research work never counts as completed study.

For documentation-only changes, check cross-links, statuses, any machine-readable examples, whitespace, and the full diff for credentials/restricted data. Run existing checks if any, and explicitly report when no executable suite exists. Final reporting must identify branch, commit SHA, changed scope, checks actually run, push outcome, PR URL, latest-head CI evidence and remaining blockers. Mark the current task completed only after its requested implementation and checks pass; leave transport failures explicit in the handoff.
