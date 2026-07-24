# Codex Session Log

## 2026-07-24

- repo: `/Users/stevens/STEELO/30_AI/Runtimes/MFLUX_MAGE_FLOW_SOURCE`
- branch: `main`
- goal: Merge upstream mflux PR #483 into the Stevesanchl fork, repair known Mage Flow defects, and add the narrower CORTEX policy profile.
- files changed: Mage Flow CLI, initializer, generation/edit pipelines, content-policy prompts, cache helper, tests, README, and the approved plan under `.cursor/plans`.
- commands/checks run: focused Mage Flow pytest; `make test-fast`; `make lint`; `git diff --check`.
- verification results: focused suite passed 79/79; fast suite passed 571 with 3 skipped; lint and whitespace checks passed.
- decisions made: upstream Microsoft policy remains the default; `--content-policy cortex` allows broad lawful creative work while retaining minor/age-ambiguity and non-consent sexual-content blocks; prompt caching is bounded to 16 entries.
- blockers or risks: real model generation and Gateway/app integration still require the isolated runtime, weights, and live M5 Max proof.
- next steps: publish the fork commit, install it in a dedicated runtime, prove text-to-image and editing, then wire exact Gateway and CORTEX routes.

## 2026-07-24

- repo: `/Users/stevens/STEELO/30_AI/Runtimes/MFLUX_MAGE_FLOW_SOURCE`
- branch: `main`
- goal: Remove the unrequested CORTEX content classifier from the live Mage Flow routes.
- files changed: Mage Flow CLI parser, initializer validation, text/edit pipelines, focused tests, Mage Flow README, integration plan, and this log.
- commands/checks run: focused Mage Flow parser/initializer/pipeline/policy suite, Ruff, and `git diff --check`.
- verification results: 72/72 tests passed; `--content-policy none` bypasses prompt and source-image classification before denoising.
- decisions made: the upstream Microsoft profile remains available as the library default, but CORTEX wrappers use `none`; technical route, integrity, reference, dimension, and no-fallback validation remain unchanged.
- blockers or risks: none.
- next steps: reinstall the fork commit into the pinned runtime and refresh the Gateway wrapper hashes.
