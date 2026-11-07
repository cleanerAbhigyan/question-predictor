# Proposed offline question export contract

Status: proposal only, not an implemented or agreed simulator interface. No producer, importer, JSON Schema, package fixture, API, shared dependency or sibling-repository change is included in Phase 0. Both independent repositories must explicitly approve and validate a future version before exchanging data.

## Package and identity

Propose a language-independent UTF-8 JSON envelope with `contract_version`, `package_id`, positive `package_revision`, `created_at`, `producer`, `payload`, and `payload_sha256`. Use semantic contract versions: reject unsupported majors; accept minor additions only under explicitly tested compatibility rules. Never silently coerce unknown fields or versions. A later implementation task must publish the machine-readable schema and compatibility fixtures before enabling transfers.

The payload contains an immutable question list, evidence manifest, run/model references, scoring profiles, usage rights and revision-specific human approval records. IDs are stable opaque identifiers, independent of array order or prompt text; each question has its own positive revision and content hash. Historical IDs/references resolve to [research records](DATA_SCHEMA.md). Generated practice uses a separate `practice-` ID namespace and can never be cast into a historical `pyq-` identity.

## Proposed fields and gates

| Payload element | Required information |
| --- | --- |
| Package provenance | Producer name/version, repository commit, source manifest version/hash and permitted evidence references; no private file paths or signed URLs |
| Question identity/scope | Stable ID/revision/hash, source category, language, exam/phase/paper/section, question format, pattern reference and exact reviewed content |
| Question and answer | Prompt, stable option IDs/text for objective formats, approved answer option/text or rubric, explanation/evidence, topic/taxonomy version and answer-review events |
| Historical evidence | Pinned source/paper/question/AnswerEvidence/VerificationEvent IDs and hashes, source locators, publisher/date and independent authentication/transcription/answer statuses |
| Generated provenance | Model/provider/version, immutable run ID, prompt/configuration hash, supporting evidence references and originality/review limitations; source category `model_generated` and label `MODEL-GENERATED PRACTICE — NOT AN ACTUAL PYQ` on every generated question |
| Scoring profile | Stable ID/version, objective versus descriptive mode, correct/incorrect/unanswered points as exact decimal strings, maximum marks, section rules, rubric reference as needed and supporting official or explicitly practice-only basis |
| Rights | Per-question and per-evidence permission for export/redistribution/use, holder/terms references, scope, review event/time and expiry; an internal permission reference must be resolvable by the approving reviewer |
| Human approval | Non-personal reviewer reference, role, UTC timestamp, decision, approved intended use, exact content/revision hash and rights/scoring review references; revocation/supersession information |

For historical questions, require supported paper/source identity, verified transcription, approved answer evidence, appropriate rights and export approval. A memory-based or coaching record must retain that category and its limitations even when approved for practice. Unverified-origin records remain in staging. Every included historical or generated item needs checked question content, answer/rubric and permitted usage; model approval of its own output is insufficient. Package approval pins the complete payload hash and must be recorded outside the payload it approves to avoid a self-referential hash. Item approval pins item content hashes, excluding approval metadata.

A scoring profile may use explicitly labeled practice rules when supported by review, but must not present them as confirmed RBI exam rules. Official configurations need the actual applicable notice and pattern evidence; no 2027 defaults may be inferred. Descriptive English Writing cannot be exported as an automatically correct/incorrect MCQ unless it actually is an objective task in the evidenced scope.

## Integrity and idempotency proposal

A later producer and consumer must use the same documented canonical payload bytes: UTF-8 without BOM, object keys sorted lexicographically by Unicode code point, compact separators, JSON escaping of control characters/quote/backslash only, other Unicode preserved, no insignificant whitespace or Unicode normalization, ordered arrays preserved, and no duplicate keys. Use strings for decimal values and integers for revisions/counts; reject floating-point literals, NaN and infinities. SHA-256 is computed over those canonical payload bytes and excludes the envelope/checksum. Specify and test edge cases across languages before adopting this scheme. Checksums detect byte changes; they do not authenticate a publisher or establish rights/approval.

The consumer would validate the whole package in staging before any persistent import. Reimporting the same package ID/revision/hash is a no-op; the same ID/revision with a different hash is a conflict and must be rejected. A newer revision may supersede only through an explicit reviewed update path; older/revoked revisions cannot silently replace newer ones. Apply the same conflict rule to question IDs/revisions across packages; retain provenance, previous revisions and import receipts. Atomic acceptance prevents partial packages. No automatic network synchronization or import on generation is proposed.

## Mandatory future rejection rules

Reject malformed JSON, duplicate keys, unsupported contract/format versions, missing required fields, unresolved references, scope mismatches, checksum mismatches, duplicate/conflicting identities or unreviewed revisions. Reject `example_only=true`, `EXAMPLE-` identifiers, fictional placeholders, guessed historical identity, missing question/options/answer or rubric, invalid answer-option references, unapproved/disputed correctness, missing/expired/prohibited export rights, absent/revoked approvals, and generated questions missing provenance or their mandatory label.

Unsupported scoring/pattern profiles, unsupported descriptive evaluation, confirmed-exam claims without notice evidence, and restricted text embedded in otherwise safe evidence metadata also block export. Partial-source limitations must remain explicit; missing content is never completed by generation. Reviewers must be able to inspect cited evidence under its allowed access terms; embedding restricted evidence in a public package is not a solution to unresolved references.

Approval is specific to content and intended use, not a blanket permission for future runs. A future simulator task must implement and test rejection, idempotency, approved revision handling and human review before any transfer. Until then the repositories remain completely independent, with no runtime coupling.
