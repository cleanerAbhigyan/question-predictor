# Proposed blind backtest protocol

Status: design only. No forecast, training manifest, model run, baseline result, held-out score or performance claim exists. Apply this protocol in a separately authorized implementation task after a usable audited corpus exists.

## Preregister the comparison

Choose one exam phase/paper/pattern scope, a held-out sitting/year, a historical training cutoff and only years actually available. Phase I sections and Phase II ESI, Finance & Management and English Writing require separate truth sets, taxonomies and scoring rules. Document any justified cross-year pattern mapping before the test. Fewer than two usable training years is insufficient for trend-based prediction; record insufficient evidence instead of running that experiment.

Before any held-out inspection, freeze eligibility/exclusion rules, taxonomy version and leaf level, K, tie rules, baseline definitions, prompt/configuration, scoring version and partial-paper policy. The Notion research proposal suggests ranking 8–12 topics/types; fix one K within that range when enough eligible topics exist. If the vocabulary is smaller, preregister the smaller K and state why. Do not change K after reveal or substitute broad parent labels to improve a hit.

Choose folds only when the actual training/test papers and rights are available. Indexed year ranges are not a fold list or evidence that every exam occurred. Changes to hypotheses after a revealed fold must be evaluated on a new untouched fold, not presented as a fresh blind score on the same paper.

## Freeze training inputs and prevent temporal leakage

Create an immutable manifest containing exact source, paper, question, answer and annotation IDs/revisions/hashes; taxonomy/pattern versions; publication/availability-date evidence; approved-use rights; actual training years; excluded records with reasons; and Git/tool/config versions. Hash the exact manifest bytes. Every derived feature, retrieval index, summary and cache must resolve to these allowlisted inputs.

For historical-as-of evaluation, each source and external feature must be demonstrably available on or before the cutoff. A reconstruction, key, annotation informed by later material, or web page published after the cutoff cannot be treated as historically available merely because it describes an older exam. Unknown publication dates are excluded from that claim. Record date precision conservatively; acquisition today alone cannot establish earlier availability. Post-cutoff annotations may only be mechanical application of a frozen rubric by a reviewer isolated from held-out material, with the timing and risk disclosed.

Current affairs, syllabus notices and policy/report versions need the same date controls. Do not browse for new information during a frozen forecast. If source dates or model training data cannot support historical availability, label the run as a retrospective experiment and explain the limitation; local input isolation alone does not make it a fully historical simulation.

## Hold out, lock, then reveal

1. A separate evaluator controls held-out papers, keys and topic annotations in inaccessible storage. The forecasting process/session gets only the training allowlist and target identity, without held-out text, summaries, answer keys, topic counts, embeddings or caches. Record prior exposure by the human/model operator; do not claim blindness after seeing the target.
2. Save the run configuration, baseline inputs and model identifier/version, prompt bytes, dependency versions, seed, tool access and determinism limits. A future hosted model may be nondeterministic or have unknown pretraining exposure. Unknown cutoff/contamination prevents a strict historical-blind claim even when the local session was isolated.
3. Generate ranked distinct leaf-topic IDs with evidence question references, rationale, failure reasons and explicit speculative/current-affairs tags. Speculation cannot manufacture training evidence or calibrated probability. This scores topic coverage; original practice generation, if later performed, stays separately labeled and reviewed.
4. Save exact UTF-8 forecast bytes and SHA-256, configuration hash and manifest hash before reveal. Obtain an independent lock receipt in an append-only record or remote commit recording those hashes and time. A locally editable timestamp alone does not establish the ordering. Freeze baseline outputs under the same conditions.
5. Only after the lock receipt may the evaluator reveal/score the held-out material. Record the first reveal/access timestamp and scoring input hashes. Any change to forecast bytes invalidates that locked run; append a new run or non-blind analysis rather than overwriting it.
6. If isolation, timing or hash checks fail, preserve the artifacts but classify the run `non_blind` (known exposure) or `unknown` (insufficient evidence). Never mix these with `locally_blind` results as equivalent evidence. Report model pretraining exposure separately from local blindness.

## Deterministic reference baselines

Use the same frozen eligible questions and vocabulary, no held-out tuning, and lexicographic topic-ID order to break ties. Count each eligible question once under its approved primary leaf annotation; subquestions require the preregistered counting rule and cannot inflate a parent count.

| Baseline | Fixed ranking rule |
| --- | --- |
| Historical frequency | Descending observed question count by primary topic across training papers |
| Most recent training year | Descending count in the latest actually available eligible training year; then descending full-training count |

All remaining ties use topic ID. Include only training-observed eligible topics; if fewer than K exist, return fewer and record the shortfall. Do not fill gaps from held-out labels. Future variants such as recency weighting need a separately frozen formula and parameters. Baseline reproducibility requires stable inputs, ordering, code version and expected output hashes, not a promised score.

## Per-paper scoring

Let T be the set of unique approved primary leaf topics actually observed in eligible held-out questions; each truth label cites question/source evidence. Let P be the first K distinct valid predicted leaf IDs in the frozen ranked list. Reject duplicate/out-of-vocabulary IDs; do not silently map or deduplicate them after reveal. A short valid list has fewer than K entries and the unfilled positions receive no credit.

- Hits H = intersection of P and T; false positives = P minus T; misses = T minus P.
- Precision@K = size(H) / K, with the preregistered positive K as denominator, including unfilled slots.
- Recall@K = size(H) / size(T). If T is empty or cannot be established, report null with a reason, not zero or perfect recall.

Report numerators/denominators, K, topic IDs and question evidence for matches/misses, truth coverage, excluded/ambiguous questions and shortfalls for the model and each baseline. A broad topic mention, parent/child match or related theme is not a leaf hit unless an explicit frozen mapping authorized that comparison. Exact-question repetition is a separate source-backed analysis and cannot be inferred from topic hits.

Default headline scoring requires a completeness-reviewed held-out paper and reviewed labels on all in-scope questions. Otherwise report separately as observed-partial-corpus scoring: apparent false positives may be present in missing content, and recall describes only the observed truth. Record unknown full-paper denominators; never extrapolate them. Answer correctness metrics, question-style coverage and descriptive writing rubric evaluations require separate predefined protocols; these topic metrics do not measure marks or answer quality.

Keep per-paper results visible. Aggregate only comparable completed folds under a preregistered method (for example, an unweighted mean of valid per-paper metrics with the included fold count); never hide missing/invalid folds, pool incomparable taxonomies, or select the best K after seeing scores. Small samples, incomplete/reconstructed sources, annotation disagreement, pattern drift and LLM contamination limit any generalization.

## Reproducible result and forward experiments

Persist the [PredictionRun and BacktestResult](DATA_SCHEMA.md) references, immutable manifests/forecasts/hashes, lock receipt, access/reveal log, scorer version and actual outputs. Corrections append a result revision with the original preserved. Distinguish protocol failures, source gaps and model limitations from measured misses.

Only after audited backtesting may a separately authorized forward-practice experiment use all genuinely available sources under a new manifest. Label it an unvalidated forecast with original practice, never an actual future paper. No 2027 dates, pattern, eligibility or marking are assumed; official notice evidence is required before configuration approval. No study completion follows from a research run.
