# Proposed research record contracts

Status: the eight contracts below remain proposals delivered in Phase 0. Phase 1A implements a narrower [metadata format](SOURCE_REGISTRY_FORMAT.md) for source candidates, research slots, assertion ledgers and private acquisition receipts, with strict runtime validation. It does not implement SourceDocument/PYQ admission or question records. There are no historical-paper examples or sample observations in this document.

## Identity, revisions and missingness

Every record has `schema_version` (semantic version), a globally unique immutable typed ID, positive integer `revision`, `created_at` (UTC timestamp), `created_by` (non-personal actor reference), and `supersedes` (prior ID/revision or null for an initial revision). References pin both ID and revision; document references also pin the byte hash. Corrections append revisions and audit events, never rewrite a published snapshot. Breaking meaning/required-field changes require a major schema version and an explicit migration; additive optional fields use a minor version.

Proposed ID prefixes are `src-`, `paper-`, `pyq-`, `answer-`, `topic-`, `verify-`, `run-`, and `backtest-`, followed by an opaque UUID. Do not encode assumed years, URLs, question numbers or mutable topic labels into IDs. A document's SHA-256 identifies bytes, not its publisher or legal status. Different bytes get a new source ID with `derived_from`/`duplicate_of` links as applicable. URL mirrors of the same bytes remain acquisition records under that source. Paper IDs identify verified sittings/papers, with controlled reconciliation of duplicate candidates; questions retain IDs across transcription revisions. Distinct reconstructions retain separate question IDs until a reviewed equivalence link is recorded.

Unknown scalar values are null with a field-level `missing_reason`: `not_provided`, `unreadable`, `not_yet_reviewed`, `conflicting`, or `not_applicable`. Omitted required fields are invalid. Empty arrays mean a known empty set, not an unknown set; unknown collections use null plus a reason. Zero means an observed zero, never missingness. Dates use ISO 8601 with recorded precision; do not invent a day/time when only a year is known. Record uncertainty and conflicting claims with evidence references rather than filling them from general knowledge.

Any future example must have `example_only=true` and IDs beginning `EXAMPLE-`. The production historical-PYQ admission rule must reject either marker, model-generated source categories, unresolved paper identity, or missing required source/verification evidence. Example markers cannot be removed to manufacture a real record.

## Independent assertions

| Dimension | Proposed values and meaning |
| --- | --- |
| `source_category` | `official`, `memory_based`, `coaching_reconstruction`, `unverified`, `model_generated`; origin claim only, supported by evidence |
| `authentication_status` | `unreviewed`, `supported`, `disputed`, `rejected`; whether publisher and claimed paper identity are supported |
| `transcription_status` | `unreviewed`, `verified`, `partial`, `disputed`, `rejected`; fidelity to the cited readable source |
| `answer_status` | `unknown`, `proposed`, `approved`, `disputed`, `rejected`; correctness assertion supported by AnswerEvidence and review |
| `rights_status` | `unknown`, `permitted`, `restricted`, `prohibited`; scoped to a named action and supported terms/permission |
| `review_status` | `pending`, `approved`, `rejected`, `revoked`; approval for a specific immutable revision and use |

These are separate fields, not a single confidence score. An official source can have unknown reuse rights, an accurately transcribed memory-based question can have a disputed answer, and a generated question can have an approved answer without becoming an actual PYQ. Numerical confidence, if later justified, needs a documented method and cannot replace these assertions.

## SourceDocument

| Field group | Required contract |
| --- | --- |
| Identity | `source_id`, common revision fields, `source_category`, claimed title and publisher (nullable with reasons) |
| Acquisition | `origin_url`, mirror/acquisition URLs, `retrieved_at`, `published_at`, date precision/evidence, media type and language; strip signed credentials from public metadata |
| Integrity | `sha256` of exact acquired bytes, byte length, controlled storage reference, `derived_from` and `duplicate_of` references; an unacquired candidate has null bytes/hash and cannot enter a corpus |
| Identity evidence | Claimed exam/year/phase/paper/session; `authentication_status`, supporting source locators and verification event references |
| Usability | Readability status (`unreviewed`, `readable`, `partial`, `unreadable`), observed page coverage, extraction tool/version/config, output hash and limitations |
| Rights | Per-action assertions for acquisition, local analysis, quotation, redistribution and export: status, holder/publisher, terms/permission reference, scope, reviewed timestamp/actor, expiry if applicable |

Do not infer permission from public availability. Acquisition and source publication dates are different; a later reconstruction of an older exam is not automatically eligible before a historical training cutoff.

## ExamPaper

`paper_id` identifies one evidenced paper/sitting, not a year-folder. Required fields: `exam_name`, `exam_year`, `phase` (`I` or `II`), `paper_name`, section/session/language where supported, `identity_evidence_refs`, `source_refs`, `pattern_version_ref`, `exam_date` with precision/evidence, and `identity_status` (`unreviewed`, `supported`, `disputed`, `rejected`). All unknown attributes retain reasons; unsupported identity blocks analytical admission.

Record `completeness` (`unknown`, `partial`, `complete`, `disputed`), observed pages/question locators, observed count, expected count (nullable, with independent supporting evidence), missing ranges, duplicate/conflict references, and completeness review events. Never infer expected count from reconstructed numbering. Separate Phase I section identifiers from Phase II ESI, Finance & Management and English Writing; retain historical pattern and objective/descriptive component evidence. A proposed 2027 configuration cannot use a paper record as proof of unannounced rules.

## PYQQuestion

Required fields: `question_id`, pinned `paper_ref`, `source_category`, one or more `source_refs` with page/printed number/region locators, observed question number (nullable), exact observed text, language, format, options where present, parent/subquestion references, `transcription_status`, verification events and content hash. A short summary is a separate derived field, never a substitute for source text. Mark illegible spans and missing options explicitly; never reconstruct them silently.

Pin approved `answer_evidence_refs`, `topic_annotation_refs`, action-scoped rights, and intended-use review events. Record duplication/equivalence links with evidence and distinction between exact repeat, conceptual repeat and related theme. Question source category must match the supporting provenance claim; mixed-source composites must preserve per-span attribution and remain quarantined until resolved. Generated practice belongs in a separate future record class, never `PYQQuestion`.

## AnswerEvidence

Required fields: `answer_evidence_id`, pinned `question_ref`, source/locator references, `evidence_kind` (`official_key`, `publisher_key`, `reviewed_solution`, `rubric`, `model_proposal`), answer value (option ID, text or rubric reference), rationale, `answer_status`, reviewer event references and applicable pattern/marking reference. Cite the key version, publication date and errata; retain competing answers as separate evidence records.

Approval requires readable question/options, supporting reasoning/key and independent human review of the exact revision. Source authentication does not approve an answer. A model proposal stays proposed until independently checked. Descriptive tasks require reviewed rubric criteria; do not invent a unique answer key. Unknown or disputed answers block scored practice export but do not require deletion of an otherwise valid source observation.

## TopicAnnotation

Required fields: `annotation_id` (using `topic-` prefix), pinned `question_ref`, `taxonomy_id`, `taxonomy_version`, phase/paper scope, primary topic, optional subtopics/styles, annotation method (`human`, `model_proposed`, `rule`), evidence locator, rationale, and review events/status. Uncertain annotations use null plus a reason and are excluded or separately reported according to a preregistered rule.

Freeze leaf labels and mappings per paper for evaluation. Revisions do not retroactively improve an existing forecast's score. Model-proposed labels need review; cross-paper taxonomy similarity does not justify pooling question counts.

## VerificationEvent

Required fields: `event_id`, subject ID/revision/hash, assertion dimension, previous and new assertion values, actor reference/role, UTC timestamp, decision/rationale, evidence references/locators, review method/version and intended use. Append-only events record approvals, disputes, corrections and revocations, including rights scope. Never overwrite adverse decisions; link superseding evidence and retain history. Public actor references must not expose private contact information. Review of one revision does not approve later changed content.

## PredictionRun

Required fields: `run_id`, purpose (`backtest` or `forward_practice`), status (`planned`, `frozen`, `forecast_locked`, `revealed`, `evaluated`, `invalidated`), phase/paper/pattern scope, training cutoff, held-out paper references under evaluator control, training manifest hash and immutable location, eligible years actually observed, exclusion ledger, taxonomy/scoring versions, baseline/model identifier and version, model knowledge-cutoff/contamination limitations, prompt/config hash, tool/dependency versions, Git SHA, random seed and determinism limitations.

Store ranked unique topic IDs, K, rationales and supporting training question references, speculative tags, forecast-byte hash, lock timestamp and independent lock receipt, reveal timestamp/access log, and blindness classification (`locally_blind`, `non_blind`, `unknown`). Held-out data must not be accessible to the forecaster; the public run description may identify the target without exposing its text. No evidence or scores are prefilled for a planned run. Record model/provider version instability; a seed does not guarantee identical LLM output.

## BacktestResult

Required fields: `result_id`, pinned locked `run_ref` and forecast hash, held-out manifest/hash, reveal/evaluation timestamps, protocol/taxonomy/scorer versions, actual truth topic set, ranked forecast set, K, hits, false positives, misses, Precision@K and Recall@K with numerator/denominator, coverage/completeness, excluded/ambiguous items, baseline comparison, blindness/contamination classification and limitations.

Null metrics must explain unavailable/zero denominators, incomplete truth or invalid locking. Pin evidence question IDs for every truth label and match, plus immutable output bytes/hash. Corrections create a new result revision. Results on observed partial papers are explicitly partial-corpus results, not whole-exam accuracy. Neither topic hits nor broad style agreement establish exact-question prediction. See [scoring rules](BACKTEST_PROTOCOL.md).

## Admission and downstream use

A future validator must check unique IDs/revisions, resolvable pinned references/hashes, enumerations, required fields, scope consistency, independent verification/rights evidence, chronology and example rejection. Corpus eligibility is declared per analysis: exact text studies require verified transcription; answer scoring additionally requires approved answers; public exports additionally require explicit redistribution/export permission and revision-specific approval. Unknown rights block publication even when local analysis is permitted. See [source audit](SOURCE_VERIFICATION.md) and [export rejection rules](EXPORT_CONTRACT.md).
