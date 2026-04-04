.PHONY: help setup validate quality test-core test-perf test-full test-quarantined suite-catalog quarantine-report ci-summary

VENV_ACTIVATE = . .venv/bin/activate

help:
	@printf "%s\n" \
		"Available targets:" \
		"  make setup              Create .venv, install Python deps, install Chromium" \
		"  make validate           Run local environment preflight checks" \
		"  make quality            Run lint, format-check, types, and suite catalog validation" \
		"  make test-core          Run smoke, regression, UI, and BDD coverage" \
		"  make test-perf          Run browser performance guardrails" \
		"  make test-full          Run the full local suite shape" \
		"  make test-quarantined   Run quarantined tests explicitly" \
		"  make suite-catalog      Render the suite catalog markdown" \
		"  make quarantine-report  Render the quarantine debt report" \
		"  make ci-summary         Render a local sample CI summary"

setup:
	python3 -m venv .venv
	@$(VENV_ACTIVATE) && pip install -r requirements.txt
	@$(VENV_ACTIVATE) && python -m playwright install chromium

validate:
	@bash ./scripts/validate_local_env.sh

quality:
	@bash ./scripts/run_quality_checks.sh

test-core:
	@bash ./scripts/run_pytest_layer.sh core

test-perf:
	@bash ./scripts/run_pytest_layer.sh perf

test-full:
	@bash ./scripts/run_all_local_tests.sh

test-quarantined:
	@bash ./scripts/run_pytest_layer.sh quarantined

suite-catalog:
	@$(VENV_ACTIVATE) && python scripts/render_suite_catalog.py

quarantine-report:
	@$(VENV_ACTIVATE) && python scripts/render_quarantine_report.py

ci-summary:
	@$(VENV_ACTIVATE) && python scripts/render_suite_catalog.py --format json > /tmp/suite-catalog.json
	@$(VENV_ACTIVATE) && python scripts/render_quarantine_report.py --format json > /tmp/quarantine-report.json
	@$(VENV_ACTIVATE) && python scripts/render_ci_summary.py \
		--title "Local CI Summary Preview" \
		--ui-url "http://localhost:5173" \
		--api-url "http://localhost:3001" \
		--suite-catalog-json /tmp/suite-catalog.json \
		--quarantine-report-json /tmp/quarantine-report.json \
		--allure-report-artifact local-allure-report \
		--allure-results-artifact local-allure-results \
		--junit-artifact local-junit-results \
		--suite-catalog-artifact local-suite-catalog \
		--quarantine-report-artifact local-quarantine-report \
		--playwright-artifact local-playwright-artifacts
