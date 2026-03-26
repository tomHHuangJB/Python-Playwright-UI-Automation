# Python Playwright UI Automation Framework Plan

## Goal

Build a new Python Playwright UI automation framework for `LocalAutomationApp` that is maintainable, scalable, stable, data-driven, parallel-ready, deterministic, debuggable, CI-friendly, configurable, isolated, reusable, extensible, and aligned with risk-based UI coverage.

Primary references used:

- Python sample: `/Users/tomhuang/prog/practice/playwright/playwright-python-tutorial`
- Existing SUT-targeted framework: `/Users/tomhuang/prog/playwrightTypeScriptFramework`
- SUT: `/Users/tomhuang/prog/LocalAutomationApp`

## SUT Scope

The initial framework should target the highest-value routes and patterns exposed by `LocalAutomationApp`:

- `/` home and navigation smoke coverage
- `/auth` login and MFA flows
- `/forms` advanced inputs and conditional UI
- `/tables` grid interactions
- `/dynamic` asynchronous and flaky-state handling
- `/files` upload and download coverage
- `/a11y`, `/i18n`, `/system`, `/integrations`, `/performance`, `/errors`, `/experiments` as phase-2 and phase-3 expansion

## Design Principles

- Use `pytest` as the test runner and framework backbone.
- Use Playwright sync Python API for readability and easier onboarding.
- Keep tests focused on business behavior, not locator plumbing.
- Standardize on `data-testid` selectors wherever the app provides them.
- Use Playwright auto-waiting and assertion-based readiness checks, not sleeps.
- Keep page objects thin and use flow objects only for multi-page business workflows.
- Make the framework parallel-safe from the beginning.
- Prefer API-backed setup and cleanup when UI setup would be slow or brittle.
- Capture trace, screenshot, and video artifacts on failure.

## Proposed Repo Structure

```text
Python-Playwright-UI-Automation/
  config/
  docs/
    implementation_plan.md
  pages/
  components/
  flows/
  fixtures/
  clients/
  utils/
  assertions/
  test_data/
    ui/
  tests/
    smoke/
    regression/
    ui/
  scripts/
```

## Planned File Layout

This is the target tracked structure after the first implementation phase:

```text
Python-Playwright-UI-Automation/
  .gitignore
  README.md
  requirements.txt
  pytest.ini
  conftest.py
  config/
    settings.py
  pages/
    base_page.py
    home_page.py
    auth_page.py
    forms_page.py
    tables_page.py
    dynamic_page.py
    files_page.py
  components/
    header.py
    debug_panel.py
  flows/
    auth_flow.py
    navigation_flow.py
  fixtures/
    data_factory.py
    sut.py
  clients/
    api_client.py
  utils/
    wait_utils.py
    artifact_utils.py
  assertions/
    ui_assertions.py
  test_data/
    ui/
      auth_cases.json
      forms_cases.json
  tests/
    smoke/
      test_home_smoke.py
      test_auth_smoke.py
    regression/
      test_forms.py
      test_tables.py
      test_dynamic.py
      test_files.py
    ui/
      test_auth_mfa.py
      test_navigation.py
  scripts/
    run_local_app.sh
```

## Architecture Decisions

### 1. Test organization

- `tests/smoke/` for fast PR-path coverage
- `tests/regression/` for broader feature coverage
- `tests/ui/` for focused workflow and cross-page scenarios

This keeps execution intent clear and supports selective CI layers.

### 2. Page objects

- One page object per major route
- No heavy inheritance tree
- Shared UI widgets go into `components/`

This follows the useful parts of the TypeScript repo without copying its structure mechanically.

### 3. Flows

- Use flow objects only when the behavior spans multiple pages or repeated business steps
- Example: auth login + MFA, top-nav route traversal

### 4. Fixtures and data

- Root `conftest.py` owns browser, context, page, base URL, and artifact hooks
- `fixtures/data_factory.py` creates unique and parallel-safe test data
- `test_data/ui/` stores larger externalized datasets when parameterization becomes too large for inline tables

### 5. API support

- `clients/api_client.py` will support fast setup, reset, or verification against the backend where appropriate
- The UI framework should not force every scenario through slow UI setup

### 6. Stability

- Wait on visible business signals
- Use deterministic selectors
- Use per-test browser context isolation
- Avoid hidden waits and utility-layer sleeps

### 7. Parallel execution

- Use `pytest-xdist`
- Design tests so they can run with `pytest -n auto`
- Avoid shared accounts, shared mutable data, and execution-order assumptions

## One-File-At-A-Time Implementation Sequence

To respect the requirement that each commit should contain one file at a time, tracked files should be added in this order:

1. `docs/implementation_plan.md`
2. `.gitignore`
3. `README.md`
4. `requirements.txt`
5. `pytest.ini`
6. `conftest.py`
7. `config/settings.py`
8. `pages/base_page.py`
9. `components/header.py`
10. `pages/home_page.py`
11. `tests/smoke/test_home_smoke.py`
12. `pages/auth_page.py`
13. `flows/auth_flow.py`
14. `tests/smoke/test_auth_smoke.py`
15. `tests/ui/test_auth_mfa.py`
16. `pages/forms_page.py`
17. `test_data/ui/forms_cases.json`
18. `tests/regression/test_forms.py`
19. `pages/tables_page.py`
20. `tests/regression/test_tables.py`
21. `pages/dynamic_page.py`
22. `tests/regression/test_dynamic.py`
23. `pages/files_page.py`
24. `tests/regression/test_files.py`
25. `clients/api_client.py`
26. `fixtures/data_factory.py`
27. `utils/wait_utils.py`
28. `assertions/ui_assertions.py`
29. `scripts/run_local_app.sh`

## Immediate Next Step

After this plan is accepted, the first tracked implementation file should be `.gitignore`, followed by `README.md`, so the repo has clean boundaries and a reproducible setup story before tests are added.
