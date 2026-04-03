# Python Playwright UI Automation

Python Playwright UI automation framework for `LocalAutomationApp`.

## Scope

This repository targets the highest-value UI routes in `LocalAutomationApp`, starting with dashboard and auth smoke coverage, then expanding into forms, tables, dynamic behavior, and files.

## Stack

- Python
- pytest
- Playwright sync API

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

If your shell has old pytest plugin variables set, clear them before running this repo:

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
```
HEADLESS=false pytest 
```

Run smoke test with browser:
```
HEADLESS=false pytest tests/smoke -m smoke

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

Phase 1 foundation currently includes:

- framework configuration
- Playwright browser/context/page fixtures
- artifact capture on failure
- dashboard navigation/header page objects
- first home smoke test

## GitHub CI Setup

This repository's GitHub Actions workflow checks out `LocalAutomationApp`, starts the SUT, waits for it to be healthy, and then runs layered test stages.

Current CI split:

- every branch push and pull request: compile + smoke suite
- push to `main`: compile + smoke suite + regression suite + UI suite + browser performance checks

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
