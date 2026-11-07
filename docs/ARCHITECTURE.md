# Proposed research architecture

Status: Phase 0 design only. No CLI, ingestion engine, model pipeline, database, API integration or export tooling exists. Python-first refers to a future local research CLI; the export boundary remains language-independent.

## Data flow and trust boundaries

1. **Candidate source registry:** record publisher, URL, dates, rights evidence and claimed paper identity before acquiring permitted material. A Notion link is a discovery pointer, not a readable input.
2. **Local extraction:** hash acquired bytes, retain page/question locators and record tool/version/configuration. OCR or model transcription remains unverified until compared with readable source content. Restricted/raw files stay outside public Git.
3. **Verification:** review source identity, transcription, completeness, answer evidence and rights independently using append-only events. Quarantine disputes and preserve conflicting versions instead of silently choosing an answer.
4. **Normalization and taxonomy:** admit only supported observations with stable references. Version Phase I sections independently from Phase II ESI, Finance & Management and English Writing. Unknown topics remain unannotated; freeze taxonomy mappings before scoring.
5. **Descriptive analytics:** compute observed counts with source/question references, eligibility rules, exclusions and denominators. Report partial coverage; exact repeats, conceptual repeats and related themes are separate categories.
6. **Frozen backtests:** pass an allowlisted training snapshot to a baseline or future model. A separate evaluator controls held-out text, annotations and keys. Save immutable forecast bytes and hash before reveal; see [protocol](BACKTEST_PROTOCOL.md).
7. **Original generation:** only after research validation, stage original practice with model/run provenance and the label `MODEL-GENERATED PRACTICE — NOT AN ACTUAL PYQ`. Require independent answer, originality, rights and human review before approval. Model proposals cannot become historical evidence.
8. **Future offline export:** a separately validated, approved JSON package may be transferred to the independent simulator under the [proposed contract](EXPORT_CONTRACT.md). No producer, importer, shared package or cross-repository import is included now.

Each stage consumes immutable versioned inputs, writes a new derived revision, and retains a manifest of input IDs/hashes, configuration, tool versions, Git SHA, actor and timestamp. A stage must fail or quarantine records with unresolved required evidence; it must never repair missing historical content by generation.

## Proposed local implementation approach

A later task may introduce a small Python package and CLI with explicit stages, local JSON/JSONL records and manifests, and optional local indexing only when useful. Schema validation, deterministic ordering and fixtures would precede ingestion. No web app, hosted service, vector database, orchestration service or production infrastructure is needed for this design.

Raw bytes and private review notes stay in controlled local storage. Approved public metadata can enter Git only after content/rights review; an ignore rule does not authorize publication. Public manifests must not expose private paths, signed URLs, credentials, restricted excerpts or reviewer personal information. Record internal references where public evidence cannot be redistributed and state public reproducibility limitations.

Use separate working directories, sessions and access permissions for forecasting and held-out evaluation. Training manifests must not leak held-out filenames/content through logs, caches, embeddings, retrieval indexes, prompts or summaries. The forecast process has no unrestricted retrieval. Model pretraining contamination remains a separate limitation even with perfect local isolation.

## Paper and configuration boundaries

Every calculation identifies exam, year, phase, paper/section, language, session where evidenced, pattern version and corpus revision. Phase I and Phase II are never pooled as one interchangeable paper. Phase II objective and descriptive tasks need distinct eligibility and scoring; English Writing uses reviewed rubric evidence rather than an invented MCQ key.

Pattern changes require evidence and explicit comparability decisions. Historical labels do not establish that an exam occurred in every indexed year. Any future 2027 configuration requires official notices for dates, pattern, eligibility and marking; unknown fields block configuration approval.

See [record contracts](DATA_SCHEMA.md), [audit procedure](SOURCE_VERIFICATION.md) and [phase gates](ROADMAP.md). Future implementation must choose and test actual storage, schema and CLI versions in a scoped task rather than treating these proposals as installed software.
