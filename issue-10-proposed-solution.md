# Proposed Solution for Issue #10: Test Isolation - Gate Live/E2E Tests

## Investigation Summary

After reviewing the codebase, I've confirmed the current state:

1. **Python Tests**:
   - Live tests in `tests/live/` directory with `@pytest.mark.live` marker
   - E2E tests in `tests/e2e/` directory with `@pytest.mark.e2e` marker
   - No environment variable gating - tests run if executed
   - No VCR/Betamax for HTTP fixture recording

2. **PHP Tests**:
   - Live tests in `tests/Live/` with `@group live` annotation
   - E2E tests in `tests/E2E/` with `@group e2e` annotation
   - Can be run separately via `composer test-live` and `composer test-e2e`
   - No environment variable gating

3. **Current CI/Default Behavior**:
   - Default test runs may include live tests if not properly excluded
   - No clear separation between deterministic and non-deterministic tests

## Proposed Solution

### 1. Python Test Isolation
- Add `pytest.skipif` decorator to all live/E2E tests that checks for `CL_RUN_LIVE` environment variable
- Update `pytest.ini` to exclude live/e2e markers by default
- Add option to run live tests: `CL_RUN_LIVE=1 pytest -m live`
- For VCR/Betamax: This is a larger enhancement that can be done separately, but we can add a note about it

### 2. PHP Test Isolation
- Add environment variable check in PHPUnit bootstrap or test base class
- Skip live/E2E tests unless `CL_RUN_LIVE=1` is set
- Update `phpunit.xml` to exclude live/e2e groups by default
- Update `composer.json` scripts to respect the env var

### 3. Default Test Behavior
- Default `pytest` and `composer test` should exclude live/e2e tests
- Only run deterministic tests (unit, integration, mock) by default
- Live/E2E tests require explicit opt-in via `CL_RUN_LIVE=1`

## Implementation Details

### Files to Modify
- `python/tests/conftest.py`: Add skipif logic for live/e2e tests
- `python/pytest.ini`: Add default marker exclusion
- `php/phpunit.xml`: Add group exclusion for live/e2e by default
- `php/tests/Live/*.php`: Add skip condition checks
- `php/tests/E2E/*.php`: Add skip condition checks
- `Makefile`: Update test targets to respect isolation

### Changes
1. Python: Add `skipif` to conftest.py that checks `CL_RUN_LIVE` env var
2. Python: Update pytest.ini to exclude live/e2e markers by default
3. PHP: Add environment check in test base class or bootstrap
4. PHP: Update phpunit.xml to exclude live/e2e groups by default
5. Update documentation to explain the isolation

## Note on VCR/Betamax

The issue mentions using VCR/Betamax to record HTTP fixtures. This is a larger enhancement that would require:
- Installing vcrpy or betamax
- Configuring cassette storage
- Recording initial fixtures
- Updating test infrastructure

For this issue, I'll focus on the environment variable gating. VCR/Betamax can be a follow-up enhancement.

