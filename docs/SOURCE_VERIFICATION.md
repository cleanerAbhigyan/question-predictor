# Proposed source verification procedure

Status: Phase 0 procedure only. No historical papers have been acquired, transcribed, authenticated or approved by this milestone. No question/answer dataset is included.

## Candidate discovery inventory as of 2026-11-07

| Candidate/reference | Publisher and date evidence | Identity/content status | Rights and next action |
| --- | --- | --- | --- |
| [PYQ Analysis index](https://app.notion.com/p/410504b1d5b68125a29fc8d2317e66a0) | Notion planning index; page metadata last edited 2026-11-06; paper publisher/publication dates unknown | Index read live; links research placeholders labeled 2018–2025 Phase I/II. Child pages/papers not audited here; no exam occurrence, readable source or completeness established | No paper reuse permission established; inspect an individual candidate only under a future source-audit task |
| [LLM PYQ Prediction](https://app.notion.com/p/410504b1d5b681f98f3aca13b0612ebf) | Notion research specification; page metadata last edited 2026-11-07 | Read live; research instructions and links, not paper evidence or a completed prediction | Planning reference only; no historical paper rights inferred |
| Official recruitment/paper/key material, if located later | Publisher, actual URL, publication date and authenticity all to be recorded; no document selected in Phase 0 | No source audited; do not assume official question papers/keys are available | Establish permitted acquisition, analysis and redistribution separately before use |
| Memory-based/coaching reconstructions, if located later | Actual publisher/date/URL required; none selected in Phase 0 | Unverified candidate class, not an imported source | Assess rights, completeness and conflicts; never relabel as official |

The last two rows describe discovery categories, not actual documents. Earlier reports of blank year pages are not a fresh audit. Page last-edit dates are not paper publication dates. An unavailable source remains missing; do not create content to fill an indexed year.

## Per-candidate audit

1. **Register before inclusion.** Assign a candidate source reference; record title, claimed publisher, canonical URL, publication-date evidence/precision, retrieval time and claimed exam/year/phase/paper/language/session. Unknown fields remain null with reasons. Avoid private/signature-bearing URLs in public logs.
2. **Check rights before acquiring or sharing.** Record terms/license or explicit permission, holder, date, scope and expiry. Assess download, local analysis, excerpts, redistribution and generated derivatives separately. Public access and official origin do not establish reuse rights. If unclear, retain only safe metadata and block redistribution; do not upload the document to public Git or an external model.
3. **Authenticate identity.** Compare publisher/domain and document context against independent evidence. Check actual year, phase, paper and sitting; a filename is insufficient. Preserve competing claims, possible non-occurrence and pattern changes. Record the assertion and its evidence in a VerificationEvent.
4. **Freeze permitted bytes.** Compute SHA-256 and byte length; preserve the original in controlled local storage. Record mirrors, acquisition history and derived versions without overwriting originals. Identical hashes identify duplicate bytes, not independent corroboration.
5. **Check readability and extraction.** Inspect every available page for legibility, clipping, missing pages, OCR errors, tables, formulas, options and language. Record actual readable ranges and extraction tool/version. A link without accessible bytes is not an input. Compare transcription against page/question locators; flag ambiguous spans rather than guessing.
6. **Establish coverage.** Record observed locators, missing ranges, observed count and independently evidenced expected count if available. Detect duplicated questions, renumbering, parent/subquestions and alternate sessions. Partial papers support only observed counts; neither full-paper denominators nor absent-topic claims follow from missing pages.
7. **Resolve reconstruction conflicts.** Keep official, memory-based, coaching and unverified material distinct. Trace mirrors/reposts to their origin; do not count syndicated copies as independent evidence. Preserve conflicting text/keys in separate revisions with reviewed equivalence links. Unresolved identity or merged reconstructions remain quarantined.
8. **Audit answer evidence independently.** Record key publisher, URL/date, version, covered question range, explanation and errata. Map answer options against the exact transcription. Review calculations/reasoning independently; use rubric evidence for writing. Only a revision-specific human event approves an answer. No missing key may be invented or filled by an unreviewed LLM response.
9. **Approve specific uses.** Decide source authentication, transcription fidelity, answer correctness, rights and per-use review independently. Freeze an eligible corpus manifest listing exact IDs/revisions/hashes and exclusions; retain reviewer events and limitations. Later revocations quarantine affected uses and trigger new manifests/results, never silent edits.

## Audit outputs and eligibility

The proposed audit ledger includes candidate/source/paper/question references, all assertions and evidence locators, reviewer role/time, conflicts, unresolved questions, action-scoped rights and approval history. Store source text locally when restricted. A public metadata-only ledger must pass privacy and rights review too; safe metadata does not imply full public reproducibility.

Descriptive analytics must state which source categories were admitted, which papers are partial and which questions were excluded. Report source-sensitive results separately; official origin does not automatically prove the answer. Historical-cutoff eligibility also needs publication-date evidence under the [backtest protocol](BACKTEST_PROTOCOL.md). Export requires the additional [approval and rights gates](EXPORT_CONTRACT.md).

An audit is complete for a chosen scope only when every included record has traceable evidence and every gap/conflict/exclusion is visible. This does not require finding a paper for every index label, and it never authorizes filling gaps with fictional material.
