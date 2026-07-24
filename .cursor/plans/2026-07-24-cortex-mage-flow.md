# CORTEX Mage Flow integration

## Approved goal

Merge upstream PR #483 into the Stevesanchl fork, repair its known correctness
issues, then integrate the fork through Steelo Gateway without a CORTEX
prompt/source-image classifier.

## Constraints

- Preserve the upstream Microsoft content-policy profile as the default for
  callers that do not choose a policy.
- CORTEX routes explicitly use `--content-policy none` and do not run prompt or
  source-image classification.
- Bound long-running prompt caches.
- Reject invalid edit dimensions before resize.
- Keep Gateway and APP_CORTEX changes separate from this fork commit.

## Verification

- Focused Mage Flow tests.
- `make test-fast`.
- `make lint`.
- `git diff --check`.
- Real M5 Max text-to-image and image-edit generation after isolated installation.
