# RBI Grade B Question Predictor

Independent **future research and model-development repository** for studying verified RBI Grade B previous-year questions (PYQs), backtesting historical patterns and generating original practice questions.

## Project relationship

- **This repository:** `question-predictor` — historical PYQ auditing, extraction/normalization, topic-frequency analysis, blind backtests and future model-generated practice sets.
- **Separate consumer:** [rbi-mock-app](https://github.com/cleanerAbhigyan/rbi-mock-app) — the mock examination simulator.
- **Local workspace:** `~/projects/rbi-app/question-predictor`, alongside the independent sibling `~/projects/rbi-app/rbi-mock-app`.
- These are **two independent Git repositories**, not a monorepo. Integration is deferred.

## Research principles

First establish a real source-backed PYQ corpus. The 2018–2025 research folders are not themselves evidence that papers exist or have been imported. Record source provenance, year, phase/paper, question number, confidence, answer-key status and limitations.

When usable data exists, analyze documented topic patterns and run blind out-of-sample backtests before forward-looking experiments. Predictions are hypotheses, **not leaked papers or guarantees**. Future model-generated questions must be labeled `MODEL-GENERATED PRACTICE — NOT AN ACTUAL PYQ`.

A future export to the simulator will use a versioned, validated question format and human approval gate. Do not add direct code coupling to `rbi-mock-app` now.

## Status

Phase 0 repository foundation and technical research specification are complete; see the [development evidence](docs/DEVELOPMENT_LOG.md). All pipeline stages and data contracts below are **proposed**, with no implemented model, validated corpus, ingestion engine, backtest, generated question set or simulator integration. A research page or year label does not establish that an exam occurred or a paper is available.

This is an independent research project, unaffiliated with and not endorsed by the Reserve Bank of India. Forecasts would be hypotheses, not guarantees. Dates, pattern, eligibility and marking for 2027 require official notices; no 2027 exam configuration is confirmed here.

## Setup and documentation

Phase 0 contains Markdown documentation and `.gitignore` only. No dependency installation, Python environment, API key or application command is needed. There is no runnable CLI or test suite yet. Python is the proposed future research implementation language.

Start with the [current task](docs/CODEX_NEXT_TASK.md) and [agent instructions](AGENTS.md). Develop on the persistent `feature` branch, safely fetch and fast-forward when clean, preserve local edits and reuse one PR into `main`. Never force-push or merge without explicit approval. A completed task means stop until a new task is published.

| Document | Purpose |
| --- | --- |
| [Project context](docs/PROJECT_CONTEXT.md) | Boundaries, requirements and present status |
| [Architecture](docs/ARCHITECTURE.md) | Proposed local Python-first research pipeline |
| [Roadmap](docs/ROADMAP.md) | Phases 0–7 and evidence gates |
| [Data schema](docs/DATA_SCHEMA.md) | Proposed identifiers, records and independent assertions |
| [Source verification](docs/SOURCE_VERIFICATION.md) | Candidate inventory and audit procedure |
| [Backtest protocol](docs/BACKTEST_PROTOCOL.md) | Leakage controls, forecast locking and scoring |
| [Export contract](docs/EXPORT_CONTRACT.md) | Proposed future offline exchange; no producer/importer |
| [Development log](docs/DEVELOPMENT_LOG.md) | Actual work and validation evidence |
| [Archived Phase 0 task](docs/prompts/2026-11-07-phase-0-repo-foundation.md) | Full sanitized implementation specification |

For this documentation milestone, check local Markdown links and status consistency, run `git diff --check`, and review the complete change for credentials and restricted content. Future code milestones must document their own reproducible tests.

## GitHub–Notion–ChatGPT continuity

GitHub is authoritative for actual code, experiment artifacts and reproducible results. Notion is authoritative for research goals, question-source references and Govt planning. ChatGPT uses live reads of both when asked. Each new implementation prompt should be archived (sanitized), implemented, tested, documented, committed and pushed to this independent repo. This is a manual/agent-assisted workflow, **not automatic three-way real-time sync**.

Do not commit secrets, private information, or question papers without redistribution rights. This repository is currently public.
