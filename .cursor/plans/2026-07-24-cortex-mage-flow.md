# CORTEX Mage Flow integration

## Approved goal

Merge upstream PR #483 into the Stevesanchl fork, repair its known correctness
issues, and expose a narrower CORTEX policy profile before integrating the fork
through Steelo Gateway.

## Constraints

- Preserve the upstream Microsoft content-policy profile as the default.
- CORTEX mode keeps only the minor, age-ambiguity, and non-consent sexual-content
  boundaries.
- Bound long-running prompt caches.
- Reject invalid edit dimensions before resize.
- Keep Gateway and APP_CORTEX changes separate from this fork commit.

## Verification

- Focused Mage Flow tests.
- `make test-fast`.
- `make lint`.
- `git diff --check`.
- Real M5 Max text-to-image and image-edit generation after isolated installation.
