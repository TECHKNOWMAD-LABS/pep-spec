.PHONY: test lint format security clean install

install:
	pip install -e ".[dev]"

test:
	python3 -m pytest conformance/ -v --tb=short --cov=stubs --cov-report=term-missing

lint:
	python3 -m ruff check stubs/ conformance/

format:
	python3 -m ruff check --fix stubs/ conformance/
	python3 -m ruff format stubs/ conformance/

security:
	@echo "=== Security scan ==="
	@echo "Checking for hardcoded secrets..."
	@grep -rn "api[_-]*key\|secret\|token\|password" stubs/ --include="*.py" || echo "  No secrets found"
	@echo "Checking for dangerous functions..."
	@grep -rn "eval(\|exec(\|__import__\|subprocess\|os.system" stubs/ --include="*.py" || echo "  No dangerous functions found"
	@echo "=== Scan complete ==="

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov dist build *.egg-info .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

all: lint test security
