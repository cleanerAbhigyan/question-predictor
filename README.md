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

This README documents an agreed future project vision. **No completed prediction model, validated corpus or backtest is claimed.**

See [Project context](docs/PROJECT_CONTEXT.md) and [Agent instructions](AGENTS.md).

## GitHub–Notion–ChatGPT continuity

GitHub is authoritative for actual code, experiment artifacts and reproducible results. Notion is authoritative for research goals, question-source references and Govt planning. ChatGPT uses live reads of both when asked. Each new implementation prompt should be archived (sanitized), implemented, tested, documented, committed and pushed to this independent repo. This is a manual/agent-assisted workflow, **not automatic three-way real-time sync**.

Do not commit secrets, private information, or question papers without redistribution rights. This repository is currently public.
