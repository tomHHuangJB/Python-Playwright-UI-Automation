.PHONY: help setup validate quality validate-catalog test-core test-perf test-full test-quarantined suite-catalog suite-catalog-json suite-catalog-csv quarantine-report quarantine-report-json quarantine-report-csv ci-summary ci-summary-json

VENV_ACTIVATE = . .venv/bin/activate

help:
	@printf "%s\n" \
		"Available targets:" \
		"  make setup              Create .venv, install Python deps, install Chromium" \
		"  make validate           Run local environment preflight checks" \
		"  make quality            Run lint, format-check, types, and suite catalog validation" \
		"  make validate-catalog   Validate suite catalog governance directly" \
		"  make test-core          Run smoke, regression, UI, and BDD coverage" \
		"  make test-perf          Run browser performance guardrails" \
		"  make test-full          Run the full local suite shape" \
		"  make test-quarantined   Run quarantined tests explicitly" \
		"  make suite-catalog      Render the suite catalog markdown" \
		"  make suite-catalog-json Render the suite catalog JSON" \
		"  make suite-catalog-csv  Render the suite catalog CSV" \
		"  make quarantine-report  Render the quarantine debt report" \
		"  make quarantine-report-json Render the quarantine debt report JSON" \
		"  make quarantine-report-csv  Render the quarantine debt report CSV" \
		"  make ci-summary         Render a local sample CI summary" \
		"  make ci-summary-json    Render a local sample CI summary as JSON"

setup:
	python3 -m venv .venv
	@$(VENV_ACTIVATE) && pip install -r requirements.txt
	@$(VENV_ACTIVATE) && python -m playwright install chromium

validate:
	@bash ./scripts/validate_local_env.sh

quality:
	@bash ./scripts/run_quality_checks.sh

validate-catalog:
	@$(VENV_ACTIVATE) && python scripts/validate_suite_catalog.py

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

suite-catalog-json:
	@$(VENV_ACTIVATE) && python scripts/render_suite_catalog.py --format json

suite-catalog-csv:
	@$(VENV_ACTIVATE) && python scripts/render_suite_catalog.py --format csv

quarantine-report:
	@$(VENV_ACTIVATE) && python scripts/render_quarantine_report.py

quarantine-report-json:
	@$(VENV_ACTIVATE) && python scripts/render_quarantine_report.py --format json

quarantine-report-csv:
	@$(VENV_ACTIVATE) && python scripts/render_quarantine_report.py --format csv

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

ci-summary-json:
	@$(VENV_ACTIVATE) && python scripts/render_suite_catalog.py --format json > /tmp/suite-catalog.json
	@$(VENV_ACTIVATE) && python scripts/render_quarantine_report.py --format json > /tmp/quarantine-report.json
	@$(VENV_ACTIVATE) && python scripts/render_ci_summary.py \
		--format json \
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
