venv:
	virtualenv venv --python=python3
	venv/bin/pip install -U pip

venv/bin/pip-sync: venv
	venv/bin/pip install pip-tools

.PHONY: dev
dev: venv venv/bin/pip-sync
	venv/bin/pip-sync requirements/dev.txt

.PHONY: build
build:
	venv/bin/python setup.py build

lint_files=setup.py flake8_aaa tests
.PHONY: lint
lint:
	@echo "=== flake8 ==="
	flake8 $(lint_files)
	@echo "=== isort ==="
	isort --quiet --recursive --diff $(lint_files) > isort.out
	if [ "$$(wc -l isort.out)" != "0 isort.out" ]; then cat isort.out; exit 1; fi
	@echo "=== yapf ==="
	yapf --recursive --diff $(lint_files)
