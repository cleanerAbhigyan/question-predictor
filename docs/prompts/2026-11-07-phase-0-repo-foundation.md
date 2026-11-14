# Question Predictor — Phase 0 Codex implementation specification

**Status:** Ready for implementation; this document is a task specification, not evidence that work was performed.
**Repository:** `cleanerAbhigyan/question-predictor`
**Existing active development branch:** `feature` — do not create a new branch.
**Working directory:** `~/projects/rbi-app/question-predictor`
**Task category:** Repository foundation and documentation only. **Do not build a prediction model.**

## Purpose and baseline

Establish a reliable, evidence-first research/development foundation for independent RBI Grade B historical PYQ verification, analysis, blind backtesting and *future* original practice-question generation. The initial remote `feature` branch was created from `main` at `538080fde0ef9fdefa558a2a188e6bf0d064cd66`, containing only `README.md`, `AGENTS.md`, and `docs/PROJECT_CONTEXT.md`. Recheck current local and remote state; do not assume this baseline is still current.

Authoritative requirements and research direction:
- Govt: https://app.notion.com/p/3ff504b1d5b68046a1e5e662573d45ea
- RBI Grade B: https://app.notion.com/p/3ff504b1d5b680eeb770c3395de0fdde
- LLM PYQ Prediction: https://app.notion.com/p/410504b1d5b681f98f3aca13b0612ebf
- PYQ Analysis: https://app.notion.com/p/410504b1d5b68125a29fc8d2317e66a0

Read Notion live when available. If not accessible, use documented repository requirements and report the access limitation. The 2018–2025 phase/year Notion research pages were blank at the preceding review; they are source placeholders, not proof of a historical paper or an imported dataset.

## Mandatory Git and safety checks

1. Confirm `pwd`, `git status -sb`, `git remote -v`, `git branch --show-current`, `git log -n 10 --oneline` and upstream tracking. Check for uncommitted edits before sync; never overwrite or discard them.
2. Work on the EXISTING `feature` branch, never on `main`. Fetch remote refs and fast-forward safely where appropriate. Do not create a different branch or PR for each task.
3. Read all existing project documentation and task archives before changing files. Do not replace unrelated work.
4. Keep the predictor completely separate from `../rbi-mock-app`. Do not modify the sibling repository, create a monorepo, shared package, runtime integration, or cross-repository import.
5. No fabricated PYQs, answer keys, exam years, topic counts, accuracy statistics, or completed experiments. Distinguish official, memory-based, coaching reconstruction, unverified, and model-generated material. Do not publish restricted exam papers, personal data, tokens or secrets.

## Phase 0 deliverables

Create or update existing files safely (no duplicates):

- `README.md`: clear status, setup/document navigation, boundary and non-affiliation.
- `AGENTS.md`: branch `feature`, linked task workflow, safety rules and completion reporting; preserve existing guidance.
- `docs/PROJECT_CONTEXT.md`: canonical project boundaries, methodology and honest present status.
- `docs/ARCHITECTURE.md`: proposed Python-first CLI research pipeline, source registry, extraction, verification, taxonomy, analytics, frozen backtests, original generation and future offline export. Distinguish proposal from implementation; no unnecessary production infrastructure.
- `docs/ROADMAP.md`: phases 0–7 with dependencies, scope, verifiable exit gates and statuses (Phase 0 only becomes completed after evidence).
- `docs/DATA_SCHEMA.md`: proposed `SourceDocument`, `ExamPaper`, `PYQQuestion`, `AnswerEvidence`, `TopicAnnotation`, `VerificationEvent`, `PredictionRun` and `BacktestResult` contracts, stable identifiers, references, document hashes, versioning, missingness and source rights. Source authentication, question correctness and rights are separate assertions.
- `docs/SOURCE_VERIFICATION.md`: candidate source inventory, publisher/date/URL, exam/phase/year identity, readability, licensing, duplicate/reconstruction conflicts, completeness, answer-key approval, audit trail. Partial papers support only observed counts.
- `docs/BACKTEST_PROTOCOL.md`: frozen source manifests and training cutoffs, held-out paper isolation, publication-date leakage prevention, deterministic baselines, locked forecast hashes, per-paper taxonomy/scoring, Precision@K/Recall@K, misses/false positives, limitations and non-blind labeling.
- `docs/EXPORT_CONTRACT.md`: **proposed only** language-independent, versioned JSON package for future `rbi-mock-app` import; stable IDs, model/run/evidence references, source category, questions/answers, scoring profile, reviewer approval, usage rights, checksum, idempotency and rejection rules. No importer or producer now.
- `docs/DEVELOPMENT_LOG.md`: initial baseline and actual work/check evidence; never claim model implementation.
- `.gitignore`: exclude secrets, caches, virtual environments, local/raw/restricted papers and non-redistributable datasets without concealing legitimate tracked docs.
- Keep this full task as the sanitized prompt archive in `docs/prompts/2026-11-07-phase-0-repo-foundation.md`.

Design an explicit distinction between source type, verification status, answer correctness and legal rights. Plan Phase I separately from Phase II (ESI, Finance & Management, English Writing). Where documentation references the Govt study strategy, preserve the 60% common banking / 40% RBI-specific allocation without treating research activity as study completion.

Examples must be clearly fictional placeholders that *cannot* pass a production historical-PYQ validator. Do not invent paper observations or mark missing values verified. The 2027 examination dates, pattern, eligibility and marking require official notices; no 2027 configuration can be assumed confirmed.

Do NOT create a runnable LLM pipeline, web app, ingestion engine, data corpus, API integration or empty scaffolding solely to mimic the architecture diagram. No changes to Notion in this implementation task.

## Validation, commits, PR and handoff

1. Verify documentation files, cross-links and stated statuses. Validate any machine-readable examples actually added. Run `git diff --check`, check for credentials/restricted data, and run existing repository tests/checks if present. Report exactly which checks ran and their outcomes; do not invent unit-test results.
2. Update documentation to reflect actual changes; append factual entries to `docs/DEVELOPMENT_LOG.md`. Keep this prompt archived. When **all** requested Phase 0 work is actually implemented and checked, mark `docs/CODEX_NEXT_TASK.md` as **Completed — awaiting next task**. Do not silently advance to Phase 1.
3. Review diff, commit all applicable files and push to `origin feature` using normal Git. Never force-push or merge to `main`. If no predictor PR exists, open one from `feature` to `main` after committing if possible; otherwise report the blocker and provide the compare URL. Keep that single PR updated for later phases; merge only on explicit user approval.
4. Recheck the remote branch head and any CI for **this latest commit**. Prior runs are not current evidence. If GitHub push/PR operations fail, report them explicitly instead of claiming remote completion.
5. Report actual branch, changed files, validation results, commit SHA, push/PR status and remaining blockers. ChatGPT will separately review real GitHub changes and perform requested Notion progress synchronization.

**Acceptance criterion:** An audited documentation/repository foundation, consistent task workflow, reproducible and source-safe design, actual checks recorded and an honest GitHub commit/push report. No implemented prediction engine, PYQ dataset, mock-app modifications or claimed experimental accuracy.
