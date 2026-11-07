# Project Context — PYQ Predictor

_Last recorded architecture decision: 2026-11-07. Planning reference; not a report of implemented model work._

## Goal

Build an independent long-term RBI Grade B PYQ analysis and original practice-question generation research project.

## Repository boundary

- Working folder: `~/projects/rbi-app/question-predictor`
- GitHub: `cleanerAbhigyan/question-predictor`
- Active development branch: `feature`; persist this branch across milestones, with one later PR into `main`. Do not merge without explicit user approval.
- Future downstream consumer: `cleanerAbhigyan/rbi-mock-app`
- Independent repositories; no monorepo, package sharing or direct runtime dependency.

## Data and methodology

1. Source available historical papers and independently validate provenance, readability, phase/year/paper and answer keys.
2. Normalize questions with stable source and question IDs; record missing, ambiguous and memory-based content honestly.
3. Extract historical topic evidence only from the actually available corpus.
4. Blind-backtest on held-out historical years; save forecasts before reviewing the test-year data.
5. Generate explicitly original practice questions only after research validation; classify them as generated practice, never PYQs.
6. Prepare a future versioned JSON export with source category, model/run ID, provenance, answer key, verification and review status. The simulator imports *approved* records later, through validation.

## Status

Future-phase research specification. The `feature` branch exists and `docs/CODEX_NEXT_TASK.md` links the Phase 0 planning/foundation task. This is **not** evidence of a corpus, prediction model, completed backtest, scored result, implementation of Phase 0 or any mock-app integration.

## Development continuity

ChatGPT writes complete sanitized development prompts to `docs/prompts/` on the `feature` branch and updates `docs/CODEX_NEXT_TASK.md`. The VS Code agent receives a **short trigger instruction**, safely pulls the current branch, reads the full GitHub task and `AGENTS.md`, implements only that milestone, runs tests, documents, commits and pushes to the same branch/PR. After completion it marks the task **Completed — awaiting next task**; ChatGPT reviews the actual diff/CI before treating it as done.

Read the Notion **LLM PYQ Prediction** and **PYQ Analysis** specifications when available. Maintain README, PROJECT_CONTEXT, ROADMAP, DEVELOPMENT_LOG and sanitized prompts. Report branch/SHA/push failures. Treat GitHub as code truth and Notion as requirement truth; ChatGPT checks both when asked. There is no automatic real-time three-way sync.

Avoid publishing secrets or restricted source papers in this public repository.
