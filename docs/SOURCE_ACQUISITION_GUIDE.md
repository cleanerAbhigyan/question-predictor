# Safe local source acquisition

Phase 1A discovers public metadata only. Its CLI never downloads, follows links, transcribes questions, submits login forms, or calls a model. The six [candidate leads](../registry/sources.json) have unknown acquisition/analysis/quotation/model-ingestion/redistribution rights. Their landing pages are readable; their papers and keys remain unreviewed. See the reproducible [availability report](SOURCE_AUDIT_REPORT.md).

## 1. Review the lead and permission first

Inspect the publisher's actual landing page and terms in Chrome. Determine whether the item is an official sample, claimed historical question paper, memory-based reconstruction, coaching reconstruction, practice/mock test, or unknown. An official sample is not automatically a modern historical PYQ. Keep paper year/phase/subject/shift as attributed claims until document-level review. No 2020 exam or 2027 configuration is established by this registry.

Record the terms or explicit permission in a private review ledger: non-personal reviewer reference, UTC review time, permission reference, applicable candidate revision, permitted actions and limitations. Review acquisition, personal analysis, quotations, model ingestion and public redistribution separately. A free download or official publisher does not settle these permissions. If acquisition or personal analysis is unclear, stop before downloading or hashing. Do not send content to ChatGPT or another external model merely because local analysis was allowed.

The public registry can record a known publication date with matching ledger evidence; a site footer update date or exam-year label is not its publication date. Do not store accounts, names/contact details, cookies, temporary access links, signed/tokenized URLs, question text, solutions, local file paths or acquired-file hashes in public metadata. Whitelisted fields and URL checks help, but human review of descriptive text is still necessary.

## 2. Chrome workflow for interactive access

1. Open the canonical landing URL. ixamBee shows sign-in controls, Oliveboard shows locked tests, and the C4S page-level PDF form requests contact information. Access to a landing page does not establish access to its advertised files. This audit submitted no forms and opened no linked paper/PDF.
2. Where legitimately required, sign in yourself and review the provider's permission/terms. Do not share credentials, cookies or browser-session URLs with the agent. Do not bypass authentication, DRM, robots restrictions, CAPTCHA, registration gates or paywalls. Do not submit personal details simply to make automated discovery work.
3. Only after permission is established, use the provider's own download button for an allowed PDF. Keep the original bytes in ignored `data/raw/` under a non-personal filename. Do not upload it to this public repository. An interactive test without a permitted downloadable file remains an access limitation; do not turn it into a scraped paper.
4. Record claimed identity, original publisher, publication evidence and any missing pages or answers in the private ledger. A download does not authenticate the source, establish completeness or approve an answer.

## 3. Direct-download workflow

Use a direct fetch only for an actually public, stable PDF URL whose terms permit acquisition and personal analysis. Manually confirm the URL, content type and rights first; do not fetch an inferred URL or reuse a signed session link. A local command such as `curl --fail --output data/raw/user-supplied.pdf 'PASTE_REVIEWED_PUBLIC_PDF_URL'` is a template requiring a real reviewed URL, not an implemented downloader or permission grant. Handle redirects manually after checking the destination. Never bypass a blocked response or turn this command into a crawler. None of the discovered provider PDFs was downloaded in Phase 1A.

## 4. Checksum an explicitly supplied file

From the repository root, validate the metadata first:

```bash
python3 -m predictor validate registry/sources.json
python3 -m predictor audit registry/sources.json
python3 -m predictor audit registry/sources.json --format json
```

Select the actual candidate ID from the validated registry. The following templates intentionally require edits; they are not fictional historical records and do not supply a permission decision or timestamp:

```bash
python3 -m predictor register-local registry/sources.json \
  --candidate 'PASTE_REAL_CANDIDATE_ID' \
  --file data/raw/user-supplied.pdf \
  --registered-at 'ACTUAL_UTC_TIMESTAMP_ENDING_Z' \
  --assessor 'NON_PERSONAL_REVIEWER_REFERENCE' \
  --permission-reference 'PRIVATE_PERMISSION_RECORD_REFERENCE' \
  --rights-cleared
```

`--rights-cleared` is an explicit human attestation for acquisition **and personal analysis only**, not an override for a known restriction. The command requires these fields before it reads a file. By default it prints a **private dry-run receipt** to the local terminal, saves nothing and leaves the registry unchanged. Do not paste its hashes/byte counts into a public issue or commit them.

To deliberately save, append `--save data/private/first-acquisition.json` to the same invocation after reviewing the private output. Only a new JSON file directly under ignored `data/private/` is accepted. Saves are atomic, mode 0600, and refuse overwrites or symlinked storage. The raw file is never copied. Attach the receipt to your private permission/review ledger; keep one immutable receipt per file/acquisition, not an editable public record.

The tool accepts regular, non-symlink local `.pdf` files with a PDF signature, streams SHA-256/byte count, and detects size/mtime changes during hashing. It does not parse or certify a PDF's internal structure, readability, paper identity, authenticity, correctness, rights or completeness. Missing files, unsupported formats and invalid signatures fail safely without echoing private paths. A valid receipt only establishes that an explicitly supplied byte sequence was hashed under the supplied attestation. No real files have been registered by this milestone; tests use artificial temporary bytes.

## 5. Request the next human review

Provide ChatGPT with the **safe candidate ID/revision, canonical landing URL, attributed year/phase/paper claims, missingness, access barriers and a summary of permitted actions**. Say which evidence remains private and what review you need. Do not send a PDF, protected question text, answer solution, receipt hash, personal path or tokenized URL by default. If content review is needed, first establish separate permission/privacy approval for sharing it with the chosen service.

Notion remains the planning/source workspace and is not changed by these commands. A future scoped task must handle evidence-bearing paper verification and corpus admission; the Phase 1A CLI has no historical-PYQ promotion, question-bank import, OCR, prediction, backtest or simulator export operation.
