# Development log

## 2026-11-07 — Phase 0 repository foundation

### Baseline and scope

The initial local checkout was clean on `main` at `b8110f6`, with only README tracked locally. Fetching origin revealed the already existing remote `feature` branch. Checked it out with tracking and ran `git pull --ff-only origin feature`; it was already current at `0e9ccea`. There were no uncommitted edits to stash, discard or incorporate. No new remote development branch was created. Git metadata writes required the environment's elevated execution path because `.git` is mounted read-only in the default sandbox.

Read all five baseline tracked files, including `AGENTS.md`, the task entrypoint and the entire existing sanitized Phase 0 archive. Read the four linked Notion requirements live without modification; see [context](PROJECT_CONTEXT.md). The newer persistent-`feature` handoff supersedes the older branch suggestion. No open `feature` PR was returned by the initial GitHub search. The prior task publication/history established requirements only, not completed Phase 0 implementation.

### Actual changes

- Expanded README setup/navigation/status/non-affiliation, preserved and extended agent instructions, and updated canonical context with live requirement-read scope and present limitations.
- Added proposed architecture, eight research record contracts, independent source/transcription/answer/rights assertions, candidate discovery inventory and verification procedure.
- Added frozen backtest design with publication cutoffs, isolated held-out access, independent forecast-lock evidence, deterministic baselines and per-paper scoring/limitations.
- Added proposed versioned offline export, revision-specific human approval, rights/checksum/idempotency/rejection gates, and phases 0–7 with dependencies and verifiable exits.
- Added `.gitignore` for secrets, environments, caches, local/raw/restricted research inputs and outputs. Preserved the existing prompt archive without duplication or edits.

No Python/package scaffolding, runnable pipeline, model, dataset, fictional PYQ, answer key, prediction, score, importer or producer was added. No sibling repository or Notion record was modified. Year-page child content and official exam notices were not audited. Research work is not recorded as study completion. The 2027 exam configuration remains unconfirmed.

### Validation evidence

Passed a temporary Python 3.13 documentation audit (kept outside the repository, not a new test framework):

- All 13 required deliverable paths present; all 12 Markdown documents have balanced fenced blocks and all 43 relative Markdown links resolve inside this repository. External references are not covered by this link count; the four required Notion references were read live.
- Archived prompt is byte-for-byte unchanged from baseline `0e9ccea`; SHA-256 `4ba2b9991c0e8a947616a3ea328d249241666b0ac5d064a8f2c82bc0a185ff56`.
- `git check-ignore --no-index` probes: 16 sensitive/local paths ignored and 15 legitimate paths (including all deliverables and `.env.example`) visible.
- Publication allowlist and credential-pattern scan passed for all 13 documentation/ignore files. Manual content review found no source-paper text, private records, credentials, dataset, fabricated observations or performance results. Pattern scanning is scoped evidence, not a universal secret-detection guarantee.
- No JSON/YAML/other machine-readable examples were added, so example parsing/schema validation is not applicable. No executable test suite, build configuration or CI workflow exists; no unit tests or model tests are claimed.

`git diff --check` passed. Completion-status checks verify Phase 0 only, with phases 1–7 not started and the archived prompt treated as historical. The task entrypoint is marked **Completed — awaiting next task** after the implementation checks; no later phase was selected. Final staged-diff review and the same checks are repeated before committing so added files and this status update are covered.

### GitHub handoff

Commit/push/PR and latest-head remote/CI evidence are reported after the checked content is committed. The implementation commit containing this entry is the Phase 0 artifact; its SHA cannot be embedded in its own content. No merge is authorized. After the completed task marker, stop pending a new published task.

## 2026-11-14 — Phase 1A source registry and availability audit

### Starting evidence and scope

Started clean on the existing `feature` branch tracking `origin/feature` at `a9ecfa6`. Ran `git fetch origin` and `git pull --ff-only origin feature`; already current, with no local edits to preserve/stash. Read AGENTS, the current entrypoint, the entire existing Phase 1A archive, README/context and all referenced Phase 0 specifications/log. GitHub PR #1 was open, unmerged, targeting `main`, with the same head. Both prompt archives remain unchanged; no new branch/PR or sibling-repository modifications were made.

Read the four authorized Notion requirements and all 16 linked 2018–2025 year/phase pages live. Every child read returned blank content. No Notion writes occurred. Inspected the six supplied canonical HTML landing pages through web reads: RBI sample index and General DR archive, ixamBee, Oliveboard, Career Power and C4S. No advertised PDF, authenticated test, form or paper/key was opened/downloaded. This is landing-page discovery only, not independent exam authentication or document review.

The registry records six candidate leads, 16 checked blank research slots and 22 attributed metadata events. All source publication dates and action-scoped permissions remain unknown; no paper/answer/completeness approval is claimed. The Career Power 2020 link remains an unverified publisher claim. RBI's official category describes inspected HTML references, not an authenticated modern corpus. Combined-paper leads are shown against component sections only as potential leads. The report distinguishes blank Notion evidence from external claims; all exam occurrences remain unverified.

### Implemented behavior

- Standard-library Python >=3.12 package/CLI: strict version-1.0.0 registry/slot/evidence validation, deterministic JSON/Markdown coverage/exception reports, and explicit local-only file hashing. No runtime dependency or networking/scraping code. `unittest` is built in; Ruff 0.14.4 is the sole pinned development dependency for lint/format checks.
- Candidate IDs/revisions are distinct from private acquired source IDs. Evidence pins subject/revision and checks claim/category/access/publication/rights fidelity. Null fields require explicit reasons. Unknown/extra/private fields, unsafe URLs, duplicate identities, false acquired/approved states and public EXAMPLE records fail closed. Public paper promotion is intentionally unavailable in this discovery-only model; partial/reviewed papers need future document evidence and a separate task/schema.
- `register-local` requires affirmative human acquisition/personal-analysis clearance, reviewer/time and a private permission reference before reading a regular non-symlink local PDF. It computes byte size/SHA-256 without copying/transcribing; dry-run is default. Explicit private saves are mode 0600, atomic, under ignored `data/private/`, and refuse overwrites. A PDF signature/hash does not validate document structure, authenticity, answers or rights. Receipts never alter public candidates or reports.
- Public registry, generated audit JSON/Markdown, format notes and Chrome/direct-download acquisition guide; updated README/AGENTS/context/architecture/schema/source verification/roadmap and ignore rules. No real source PDF, private receipt, protected questions/solutions, model, corpus extraction, backtest, generated practice or simulator integration was added.
- Read-only GitHub Actions with commit-pinned official checkout/setup-python actions, credential persistence disabled and Python 3.12/3.13 checks on `feature` pushes and its PR. Fast tests require no live source, registered account, paid API or secrets.

### Actual local validation

On Python 3.13.5, all following commands passed after implementation:

```bash
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/python -m unittest discover -v
.venv/bin/python -m predictor validate registry/sources.json
.venv/bin/python -m predictor audit registry/sources.json > /tmp/predictor-audit.md
.venv/bin/python -m predictor audit registry/sources.json --format json > /tmp/predictor-audit.json
cmp /tmp/predictor-audit.md docs/SOURCE_AUDIT_REPORT.md
cmp /tmp/predictor-audit.json registry/audit.json
git diff --check
```

The validator prints `Valid registry 1.0.0: 6 candidates, 16 slots; 0 approved papers.` All **25 tests passed**. Tests cover metadata/rights/missingness/date/type/identity/evidence rejection; private data/URL rejection; atomic failures; no source-file/network reads on import/validate/audit; artificial temporary file receipts/hash/size and missing/unsupported/invalid-signature/symlink failures; duplicate receipt IDs; stable zero/partial-coverage reports and 2020 uncertainty; generated/sample exclusion from historical availability; regenerated real reports; Markdown links, archive integrity, ignored private paths and common credential patterns. Test-owned artificial PDF-signature bytes contain no question content. A separate `register-local` CLI dry-run smoke check with temporary artificial bytes passed, emitted no path/content, saved nothing and did not mutate the registry. No real acquisition is claimed. Exact-head CI outcome is included in the PR handoff.

The Phase 0 archive SHA-256 remains `4ba2b9991c0e8a947616a3ea328d249241666b0ac5d064a8f2c82bc0a185ff56`; the Phase 1A archive remains `2fb80f5ef5050d26d012817bd465591482f1945787ee48ef2e4f7b4bc90cfe7e`. Both also match baseline `a9ecfa6`. Initial Ruff installation in the restricted sandbox could not resolve the package index; installation through the approved elevated path into `.venv` succeeded. No runtime/test network access is needed. Local Python 3.12 is unavailable; that version is covered by the configured remote CI, whose actual result must be checked after push.

### Completion and limitations

The milestone implements metadata discovery/tooling only, with zero acquired/approved papers. All 16 Notion slots were checked and blank; all six landing pages were read, but their files, actual readability/completeness, keys, publication dates and permissions were not audited. Registered access and unknown rights remain barriers to actual acquisition, not blockers to this metadata-only milestone. Known provider identity/coverage conflicts remain in the registry rather than guessed away. No 2027 exam configuration or study completion is established.

Phase 1A is marked **Completed — awaiting next task** after local implementation/checks. Final staged checks, commit/push on `feature`, existing PR #1 update and exact-head CI verification follow as the GitHub handoff. This entry is part of the implementation commit; final SHA/transport evidence belongs in the PR/final handoff to avoid a self-referential commit hash. No Phase 1B task was selected and no merge is authorized.
