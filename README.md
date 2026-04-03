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

Run quality checks:

```bash
./scripts/run_quality_checks.sh
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

- PR smoke workflow uploads `python-playwright-smoke-allure-report`
- main full-suite workflow uploads `python-playwright-full-suite-allure-report`

That HTML artifact is the intended report for non-technical stakeholders to review. The raw `allure-results` artifact is also uploaded for debugging or reprocessing.

## BDD

This repo also supports BDD on top of the existing pytest + Playwright architecture using `pytest-bdd`.

Design rules for BDD in this repo:

- feature files live in `features/`
- BDD test entry points live in `tests/bdd/`
- step definitions must stay thin and call page objects, flows, and fixtures
- shared route-level BDD steps are backed by a page registry rather than route-specific selector code in step files
- when a workflow is covered by BDD, the repo should avoid keeping an equivalent classic pytest test for the same scenario
- Gherkin is intended for business-readable workflows, not every low-level widget check

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
- failure diagnostics for console errors, page errors, and failed network requests
- quality gates through `ruff`, `black`, `mypy`, and `pre-commit`
- parallel execution through `pytest-xdist`

## GitHub CI Setup

This repository's GitHub Actions workflow checks out `LocalAutomationApp`, starts the SUT, waits for it to be healthy, and then runs layered test stages.

Current CI split:

- pull requests: compile + smoke suite + Allure report artifact
- push to `main`: full suite + performance checks + Allure report artifact

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
