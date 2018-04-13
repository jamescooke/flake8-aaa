lint_files=setup.py flake8_aaa tests
rst_files=README.rst CHANGELOG.rst

venv:
	virtualenv venv --python=python3
	venv/bin/pip install -U "pip<10"

venv/bin/pip-sync: venv
	venv/bin/pip install pip-tools

.PHONY: dev
dev: venv venv/bin/pip-sync
	venv/bin/pip install -U "pip<10"
	venv/bin/pip-sync requirements/dev.txt

.PHONY: build
build:
	venv/bin/python setup.py build

.PHONY: lint
lint:
	@echo "=== flake8 ==="
	flake8 $(lint_files)
	@echo "=== isort ==="
	isort --quiet --recursive --diff $(lint_files) > isort.out
	if [ "$$(wc -l isort.out)" != "0 isort.out" ]; then cat isort.out; exit 1; fi
	@echo "=== yapf ==="
	yapf --recursive --diff $(lint_files)
	@echo "=== rst ==="
	$(bin_prefix)restructuredtext-lint $(rst_files)
	@echo "=== setup.py ==="
	$(bin_prefix)python setup.py check --metadata --strict

.PHONY: fixlint
fixlint:
	@echo "=== fixing isort ==="
	isort --quiet --recursive $(lint_files)
	@echo "=== fixing yapf ==="
	yapf --recursive --in-place $(lint_files)

.PHONY: clean
clean:
	rm -rf dist build .tox .pytest_cache flake8_aaa.egg-info
	find . -name '*.pyc' -delete
