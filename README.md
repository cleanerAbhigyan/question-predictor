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

Phase 0 foundation is complete. Phase 1A implements an offline, tested **metadata-only source registry and availability audit**; see the [development evidence](docs/DEVELOPMENT_LOG.md) and [generated report](docs/SOURCE_AUDIT_REPORT.md). Six landing-page leads were inspected, and all 16 Notion year/phase pages were accessible and blank. There are **zero acquired or approved historical papers** in this milestone. A research page or year label does not establish that an exam occurred or a paper is available. No corpus extraction, model, backtest, generated set or simulator integration is implemented.

This is an independent research project, unaffiliated with and not endorsed by the Reserve Bank of India. Forecasts would be hypotheses, not guarantees. Dates, pattern, eligibility and marking for 2027 require official notices; no 2027 exam configuration is confirmed here.

## Setup and documentation

Use Python **3.12 or newer** from the repository root. The runtime and deterministic `unittest` suite use only the standard library. Ruff is the sole development dependency, pinned for reproducible lint/format checks. No API keys or source PDFs are needed.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m predictor validate registry/sources.json
.venv/bin/python -m predictor audit registry/sources.json
.venv/bin/python -m predictor audit registry/sources.json --format json
.venv/bin/python -m unittest discover -v
.venv/bin/ruff check .
.venv/bin/ruff format --check .
git diff --check
```

Validation currently prints `Valid registry 1.0.0: 6 candidates, 16 slots; 0 approved papers.` Audits read only the explicit metadata file, make no network requests and never follow stored paths or URLs. JSON/Markdown output is deterministic; tests and CI compare checked-in reports against regeneration. Failures exit with code 2 and no partial report or registry mutation.

The explicitly invoked `register-local` command hashes a user-supplied, rights-cleared regular PDF into a **private dry-run receipt**; deliberate saves are restricted to ignored `data/private/`. It never copies the file, modifies the public registry or approves a PYQ. See the [acquisition guide](docs/SOURCE_ACQUISITION_GUIDE.md) before using it.

This public repository accepts safe candidate metadata only: **never commit PDFs, raw questions, protected solutions, personal paths, accounts, cookies, tokenized URLs or private checksum receipts**. Store raw files in ignored `data/raw/` and receipts in `data/private/`. Free access or official origin does not authorize redistribution or external model ingestion; review each action separately. No downloader or scraper is implemented.

Start with the [current task](docs/CODEX_NEXT_TASK.md) and [agent instructions](AGENTS.md). Develop on the persistent `feature` branch, safely fetch and fast-forward when clean, preserve local edits and reuse one PR into `main`. Never force-push or merge without explicit approval. A completed task means stop until a new task is published.

| Document | Purpose |
| --- | --- |
| [Project context](docs/PROJECT_CONTEXT.md) | Boundaries, requirements and present status |
| [Architecture](docs/ARCHITECTURE.md) | Proposed local Python-first research pipeline |
| [Roadmap](docs/ROADMAP.md) | Phases 0–7 and evidence gates |
| [Data schema](docs/DATA_SCHEMA.md) | Proposed identifiers, records and independent assertions |
| [Source verification](docs/SOURCE_VERIFICATION.md) | Candidate inventory and audit procedure |
| [Registry format](docs/SOURCE_REGISTRY_FORMAT.md) | Implemented version 1.0.0 fields and conservative admission rules |
| [Source registry](registry/sources.json) | Public metadata input and assertion ledger |
| [Availability report](docs/SOURCE_AUDIT_REPORT.md) | Generated 2018–2025 component matrix and gaps |
| [Acquisition guide](docs/SOURCE_ACQUISITION_GUIDE.md) | Chrome/direct-download choices and private local checksums |
| [Backtest protocol](docs/BACKTEST_PROTOCOL.md) | Leakage controls, forecast locking and scoring |
| [Export contract](docs/EXPORT_CONTRACT.md) | Proposed future offline exchange; no producer/importer |
| [Development log](docs/DEVELOPMENT_LOG.md) | Actual work and validation evidence |
| [Archived Phase 0 task](docs/prompts/2026-11-07-phase-0-repo-foundation.md) | Full sanitized implementation specification |
| [Archived Phase 1A task](docs/prompts/2026-11-07-phase-1a-source-registry-audit.md) | Source registry/audit milestone specification |

The read-only GitHub Actions workflow runs lint, formatting, offline tests, registry validation and report comparisons on Python 3.12/3.13 for `feature` pushes and its PR. No real PDFs, registered websites, Notion access or external secrets are required by the tests. See the development log and latest PR checks for actual outcomes, not assumed success.

## GitHub–Notion–ChatGPT continuity

GitHub is authoritative for actual code, experiment artifacts and reproducible results. Notion is authoritative for research goals, question-source references and Govt planning. ChatGPT uses live reads of both when asked. Each new implementation prompt should be archived (sanitized), implemented, tested, documented, committed and pushed to this independent repo. This is a manual/agent-assisted workflow, **not automatic three-way real-time sync**.

Do not commit secrets, private information, or question papers without redistribution rights. This repository is currently public.
