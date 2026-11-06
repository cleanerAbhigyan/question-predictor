# Development Agent Instructions — question-predictor

This is an independent future model/research repository. Do **not** merge it with `../rbi-mock-app` or create cross-repository runtime coupling.

Read `README.md`, `docs/PROJECT_CONTEXT.md`, existing research docs and prompt archive before implementation. Check `git status -sb`, `git remote -v`, active branch, and integrate remote changes without overwriting local work.

For every substantive development prompt:
1. Save a sanitized copy in `docs/prompts/YYYY-MM-DD-short-task.md`.
2. Implement the specifically requested scope and tests; do not invent question papers, answer keys, prediction results, topic counts, exams, or backtest scores.
3. Update README, PROJECT_CONTEXT, ROADMAP and DEVELOPMENT_LOG with what actually happened.
4. Commit source, tests, prompt and documentation; push to this repository if authenticated. Never force push. Report branch, commit SHA, tests and push success/failure.
5. Keep official/memory-based/coaching/LLM-generated question sources distinct. No invented PYQs.
6. Maintain blind held-out-year backtests and reproducible source IDs.
7. Prepare only a *future* versioned schema/approved data export for the independent simulator; do not change sibling repo as a side effect.
8. Do not publish secrets, personal information, restricted papers or redistribution-prohibited data.

Notion is the research and planning reference, GitHub is implementation/research evidence, ChatGPT reconciles the two when asked. No automatic real-time three-way synchronization is implied.
