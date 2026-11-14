# Project Context — PYQ Predictor

_Last updated: 2026-11-14. Phase 0 foundation and Phase 1A metadata tool implemented; corpus/model research remains future work._

## Goal

Build an independent long-term RBI Grade B PYQ analysis and original practice-question generation research project.

## Repository boundary

- Working folder: `~/projects/rbi-app/question-predictor`
- GitHub: `cleanerAbhigyan/question-predictor`
- Active development branch: `feature`; persist this branch and [PR #1](https://github.com/cleanerAbhigyan/question-predictor/pull/1) into `main`. Do not merge without explicit user approval.
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

Phase 0 foundation is complete. Phase 1A adds a strict, versioned metadata registry, offline validation/auditing CLI, private opt-in file checksum receipts, safe acquisition guide, deterministic tests and read-only CI. See [development log](DEVELOPMENT_LOG.md), [current task](CODEX_NEXT_TASK.md), [format](SOURCE_REGISTRY_FORMAT.md) and [availability report](SOURCE_AUDIT_REPORT.md). Phase 1A does not complete document acquisition/verification or the wider Phase 1 source-audit program. No Phase 1B or later task is selected automatically.

There is no corpus extraction, ingestion engine, prediction model, completed backtest, scored result, generated practice set or mock-app integration. Runtime validation is implemented only for metadata candidates, research slots, evidence and private receipts; the eight future research contracts remain proposals. No official 2027 dates, pattern, eligibility or marking are established. This independent project is unaffiliated with RBI.

## Requirements reviewed

The following Notion pages were read through the connected service on 2026-11-07 without modification: [Govt](https://app.notion.com/p/3ff504b1d5b68046a1e5e662573d45ea), [RBI Grade B](https://app.notion.com/p/3ff504b1d5b680eeb770c3395de0fdde), [LLM PYQ Prediction](https://app.notion.com/p/410504b1d5b681f98f3aca13b0612ebf) and [PYQ Analysis](https://app.notion.com/p/410504b1d5b68125a29fc8d2317e66a0). The newer `feature` handoff supersedes the older branch proposal on the LLM page. Notion still described Phase 0 as pending at this read; it is not automatically updated by this implementation.

The source index links 2018–2025 year/phase pages, but those child pages and papers were not audited in Phase 0. Their earlier reported blank state is historical context, not a current verified inventory. No year label proves an exam or source exists. [Source verification](SOURCE_VERIFICATION.md) records the discovery boundary.

Phase 1A reread all four references and all 16 child pages on 2026-11-14. All child reads returned blank pages; no attachment or question text was observed. The six supplied public landing-page leads were inspected via web reads, without opening their advertised PDFs or interactive tests. Category/identity claims remain attributed metadata, rights unknown, source readability/completeness/answers unverified, and approved/acquired paper counts zero. The Career Power 2020 link remains unresolved. Notion was not modified; implementation progress is recorded in GitHub only.

Research must remain separate from study progress. Preserve the established **60% common banking / 40% RBI-specific** allocation without double-counting overlap. Repository work, forecasts and proposed study tasks do not mark topics studied or mocks attempted.

## Technical specification navigation

The [architecture](ARCHITECTURE.md) describes a proposed local Python-first CLI. [Data schema](DATA_SCHEMA.md) separates provenance, verification, answer evidence and rights. [Backtest protocol](BACKTEST_PROTOCOL.md) defines frozen manifests and limitations of historical LLM tests. [Export contract](EXPORT_CONTRACT.md) proposes an offline, approved, versioned JSON boundary only. [Roadmap](ROADMAP.md) gives dependencies and verifiable exit gates; no phase is implicitly authorized by its presence there.

## Development continuity

ChatGPT writes complete sanitized development prompts to `docs/prompts/` on the `feature` branch and updates `docs/CODEX_NEXT_TASK.md`. The VS Code agent receives a **short trigger instruction**, safely pulls the current branch, reads the full GitHub task and `AGENTS.md`, implements only that milestone, runs tests, documents, commits and pushes to the same branch/PR. After completion it marks the task **Completed — awaiting next task**; ChatGPT reviews the actual diff/CI before treating it as done.

Read the Notion **LLM PYQ Prediction** and **PYQ Analysis** specifications when available. Maintain README, PROJECT_CONTEXT, ROADMAP, DEVELOPMENT_LOG and sanitized prompts. Report branch/SHA/push failures. Treat GitHub as code truth and Notion as requirement truth; ChatGPT checks both when asked. There is no automatic real-time three-way sync.

Avoid publishing secrets or restricted source papers in this public repository.
