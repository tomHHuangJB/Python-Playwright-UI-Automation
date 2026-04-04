# Python Playwright UI Automation

Python Playwright UI automation framework for `LocalAutomationApp`.

## Scope

This repository targets the highest-value UI routes in `LocalAutomationApp`, starting with dashboard and auth smoke coverage, then expanding into forms, tables, dynamic behavior, and files.

## Stack

- Python
- pytest
- pytest-bdd
- Allure
- Playwright sync API

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

Equivalent one-command bootstrap:

```bash
make setup
```

If your shell has inherited pytest plugin variables set from another repo or shell profile, clear them before running this repo:

```bash
unset PYTEST_PLUGINS
unset PYTEST_ADDOPTS
```

## Run

Default target:

- UI: `http://localhost:5173`
- API: `http://localhost:3001`

Run smoke tests:

```bash
pytest tests/smoke -m smoke
```

Run a single test file:

```bash
pytest tests/smoke/test_home_smoke.py -m smoke
```

If you want to run against a non-default app location:

```bash
BASE_UI_URL=http://localhost:5173 BASE_API_URL=http://localhost:3001 pytest tests/smoke -m smoke
```

Run all test with browser:

```bash
HEADLESS=false pytest 
```

Run smoke test with browser:

```bash
HEADLESS=false pytest tests/smoke -m smoke
```

Run BDD scenarios:

```bash
pytest tests/bdd -m bdd
```

Generate local Allure results for a run:

```bash
pytest tests/bdd -m bdd --alluredir=allure-results
```

Run the local layered suite script:

```bash
./scripts/run_all_local_tests.sh
```

That script now mirrors the CI suite shape locally:

- quality checks
- smoke + regression + UI + BDD tests
- performance tests

Validate the local environment before a run:

```bash
bash ./scripts/validate_local_env.sh
```

Run a single named suite layer:

```bash
bash ./scripts/run_pytest_layer.sh [smoke|core|perf|full|quarantined]
```

Render the current suite catalog as a markdown coverage matrix:

```bash
python scripts/render_suite_catalog.py
```

Render the machine-readable route manifest:

```bash
python scripts/render_suite_catalog.py --format json
```

Render the suite catalog as CSV:

```bash
python scripts/render_suite_catalog.py --format csv
```

Render the quarantine debt report:

```bash
python scripts/render_quarantine_report.py
```

Render the quarantine debt report as CSV:

```bash
python scripts/render_quarantine_report.py --format csv
```

Run quality checks:

```bash
./scripts/run_quality_checks.sh
```

Top-level shortcuts:

```bash
make quality
make validate-catalog
make test-core
make test-perf
make test-full
make suite-catalog
make suite-catalog-json
make suite-catalog-csv
make quarantine-report
make quarantine-report-json
make quarantine-report-csv
make route-gap-report
make route-gap-report-json
make route-gap-report-csv
make ci-summary-json
```

Validate suite catalog governance directly:

```bash
python scripts/validate_suite_catalog.py
```

Useful env vars:

- `BASE_UI_URL`
- `BASE_API_URL`
- `BROWSER`
- `HEADLESS`
- `SLOW_MO_MS`
- `TRACE`
- `VIDEO`
- `SCREENSHOT`
- `ARTIFACTS_DIR`
- `PERF_NAVIGATION_MAX_MS`
- `PERF_DOM_CONTENT_LOADED_MAX_MS`

## Allure Reporting

This repo supports Allure reporting for both local runs and GitHub Actions.

Local usage:

```bash
pytest tests/bdd -m bdd --alluredir=allure-results
```

If you have the Allure CLI installed locally, generate HTML with:

```bash
allure generate allure-results --clean -o allure-report
```

In GitHub Actions:

- PR workflow uploads separate `core-suite` and `perf-suite` Allure/JUnit/artifact bundles
- `main` workflow uploads separate `core-suite` and `perf-suite` Allure/JUnit/artifact bundles
- both workflows upload shared suite catalog artifacts in markdown, JSON, and CSV form
- both workflows upload shared quarantine report artifacts in markdown, JSON, and CSV form
- both workflows upload shared route gap report artifacts in markdown, JSON, and CSV form
- both workflows upload CI summary JSON artifacts for each job
- both workflows also write a GitHub job summary that shows real suite, route, owner, quarantine, and uncovered-route counts alongside artifact links

CI execution model:

- PR and `main` workflows now split the test run into parallel `core-suite` and `perf-suite` jobs
- `core-suite` runs smoke, regression, UI, and BDD coverage
- `perf-suite` runs the browser performance guardrail layer
- workflow concurrency cancels superseded runs on the same PR or branch
- this keeps coverage unchanged while reducing end-to-end workflow wall-clock time

That HTML artifact is the intended report for non-technical stakeholders to review. The raw `allure-results` artifact is also uploaded for debugging or reprocessing.

On failed UI-facing tests, the Playwright artifact bundle also includes the API baseline context used for the test run in `baseline-state.json`, and the same seed/layer metadata is attached to Allure.
The same failure context is attached directly in Allure as screenshot, trace, retained video, console events, request failures, page errors, and baseline state.

Route governance is enforced against the real app registry in `pages/page_registry.py`, not just against the suite catalog itself.
Use `python scripts/render_route_gap_report.py` or the `make route-gap-report*` targets to inspect route coverage gaps directly.

Allure metadata is enriched centrally from repo conventions, including:

- suite layer such as smoke, BDD, regression, or performance
- business feature grouping such as Authentication or Files
- owner labels for accountable platform areas
- risk tags such as `critical-path` or `business-critical`

## BDD

This repo also supports BDD on top of the existing pytest + Playwright architecture using `pytest-bdd`.

Design rules for BDD in this repo:

- feature files live in `features/`
- BDD test entry points live in `tests/bdd/`
- step definitions must stay thin and call page objects, flows, and fixtures
- shared route-level BDD steps are backed by a page registry rather than route-specific selector code in step files
- when a workflow is covered by BDD, the repo should avoid keeping an equivalent classic pytest test for the same scenario
- Gherkin is intended for business-readable workflows, not every low-level widget check

Selector contract:

- prefer `data-testid` selectors first in page objects and shared components
- use role-based selectors when the role/name pair is an intentional accessibility contract
- use raw CSS or text selectors only when the app does not expose a stable contract, and keep them inside page objects
- avoid putting selectors directly in tests or BDD step files

Scenario data contract:

- keep typed scenario models in `test_data/scenarios.py`
- register scenario names and file paths centrally in the scenario loader
- load scenario files through `DataFactory` instead of ad hoc JSON reads in tests

Current BDD coverage includes:

- auth workflow scenarios
- forms workflow scenarios
- tables workflow scenarios
- dynamic behavior scenarios
- file workflow scenarios

If you hit local collection issues caused by inherited shell settings, run:

```bash
env -u PYTEST_PLUGINS -u PYTEST_ADDOPTS pytest tests/bdd -m bdd
```

Example:

```gherkin
Scenario: Demo user signs in successfully
  Given the user opens the "auth" page
  When the user signs in with the demo account
  Then the auth page shows a signed-in token
```

## Browser Performance Checks

This repo includes a small browser-side performance layer for lightweight guardrails.

What it is:

- Playwright checks against browser navigation timing and other in-browser signals
- useful for catching obvious page-level regressions in local runs and CI
- appropriate for route-level budgets such as DOM content loaded and load event timing

What it is not:

- not load testing
- not throughput or concurrency testing
- not backend capacity benchmarking
- not a substitute for k6, JMeter, or Gatling

Run only the browser performance checks:

```bash
pytest tests/perf -m perf
```

Example with explicit budgets:

```bash
PERF_DOM_CONTENT_LOADED_MAX_MS=2500 PERF_NAVIGATION_MAX_MS=4000 pytest tests/perf -m perf
```

The first performance check currently covers navigation timing on the home route. The budgets are intentionally conservative so the suite stays stable across developer machines and CI runners.

## Current Coverage

Current framework coverage includes:

- smoke coverage for home and auth
- regression coverage across a11y, i18n, system, integrations, performance, errors, experiments, mobile, components, and grpc-oriented pages
- UI workflow coverage for navigation, debug panel, advanced selectors, and mobile navigation
- browser-side performance guardrails
- BDD coverage for auth, forms, tables, dynamic behavior, and file workflows
- Playwright trace, screenshot, and video artifact capture
- baseline reset/seed context captured into failure artifacts for replayable debugging
- failure diagnostics for console errors, page errors, and failed network requests
- quality gates through `ruff`, `black`, `mypy`, and `pre-commit`
- strict pytest governance through registered markers, strict config, and strict xfail handling
- parallel execution through `pytest-xdist`
- explicit quarantine support for unstable tests instead of hiding flakiness behind global retries
- an explicit suite catalog that maps test entry files to layer, feature, owner, and risk
- route-level manifest data that maps coverage to concrete app paths and scenario counts
- suite catalog validation enforced in the quality-check gate

## GitHub CI Setup

This repository's GitHub Actions workflow checks out `LocalAutomationApp`, starts the SUT, waits for it to be healthy, and then runs layered test stages.

Current CI behavior:

- pull requests: smoke + regression + UI + BDD + performance suite + Allure report artifact
- push to `main`: smoke + regression + UI + BDD + performance suite + Allure report artifact
- shared bootstrap logic lives in `.github/actions/bootstrap-localautomationapp` so the PR and main workflows stay aligned instead of duplicating environment setup

Flaky-test policy:

- mark unstable tests with `@pytest.mark.quarantined("reason")`
- quarantined tests are skipped by default
- include them only when explicitly requested with `INCLUDE_QUARANTINED=1`
- prefer fixing or removing quarantine quickly rather than adding global retries

This keeps PR feedback fast while still validating the broader framework on the integration branch.

The workflow expects this GitHub Actions repository secret:

- `LOCAL_AUTOMATION_APP_SSH_KEY`

That secret must contain an SSH private key that matches a read-only deploy key installed on the `LocalAutomationApp` GitHub repository.

### Existing setup on this machine

An existing matching key pair already exists locally in:

- `/Users/tomhuang/prog/playwrightTypeScriptFramework/local_automation_app_ci`
- `/Users/tomhuang/prog/playwrightTypeScriptFramework/local_automation_app_ci.pub`

The public key fingerprint is:

- `SHA256:HzUN7cPzCLm3cImoNVk4Uy+WeIbFLodGiVZuTEdFutA`

If you control both repos and want to reuse that key:

1. Open this repository on GitHub.
2. Go to `Settings` > `Secrets and variables` > `Actions`.
3. Create a repository secret named `LOCAL_AUTOMATION_APP_SSH_KEY`.
4. Paste the contents of:
   `/Users/tomhuang/prog/playwrightTypeScriptFramework/local_automation_app_ci`

Do not commit that private key into this repository.

### Fresh setup for another machine or another contributor

If someone else checks out this code and does not already have a working deploy key, create a new one locally:

```bash
ssh-keygen -t ed25519 -C "python-playwright-ci-localautomationapp" -f ./local_automation_app_ci
```

This creates:

- `./local_automation_app_ci` for the private key
- `./local_automation_app_ci.pub` for the public key

### Configure LocalAutomationApp GitHub repo

In `tomHHuangJB/LocalAutomationApp`:

1. Go to `Settings` > `Deploy keys`.
2. Click `Add deploy key`.
3. Use a clear title such as `python-playwright-ui-automation-ci`.
4. Paste the contents of `./local_automation_app_ci.pub`.
5. Leave `Allow write access` unchecked.

### Configure this Python repo on GitHub

In `tomHHuangJB/-Python-Playwright-UI-Automation`:

1. Go to `Settings` > `Secrets and variables` > `Actions`.
2. Create a repository secret named `LOCAL_AUTOMATION_APP_SSH_KEY`.
3. Paste the contents of `./local_automation_app_ci`.

### Verify the key pair

To confirm the public key fingerprint before uploading it:

```bash
ssh-keygen -lf ./local_automation_app_ci.pub
```

To print the private key for GitHub secret entry:

```bash
cat ./local_automation_app_ci
```

### Optional cleanup

If you created a temporary key pair only for CI setup, remove it after the GitHub secret and deploy key are configured:

```bash
rm -f ./local_automation_app_ci ./local_automation_app_ci.pub
```
