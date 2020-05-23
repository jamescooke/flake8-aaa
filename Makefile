lint_files=setup.py src/flake8_aaa tests
rst_files=README.rst CHANGELOG.rst
good_examples = $(wildcard examples/good/*.py examples/good/noqa/test_cmd.py examples/good/black/noqa/test_cmd.py)
bad_examples = $(wildcard examples/bad/*.py)


venv:
	virtualenv venv --python=python3
	venv/bin/pip install -U pip

venv/bin/pip-sync: venv
	venv/bin/pip install pip-tools

# Local dev: Install requirements
.PHONY: dev
dev: venv venv/bin/pip-sync
	venv/bin/pip-sync requirements/base.txt requirements/test.txt requirements/dev.txt

# Local dev: Run all tests for available Python versions
.PHONY: tox
tox:
	tox --skip-missing-interpreters true

# --- Tox recipes ---

# Tox: -e "py3{6,7,8}-lint"
.PHONY: lint
lint:
	@echo "=== flake8 ==="
	flake8 $(lint_files)
	@echo "=== mypy ==="
	mypy src/flake8_aaa tests --ignore-missing-imports
	@echo "=== isort ==="
	isort --quiet --recursive --diff $(lint_files) > isort.out
	if [ "$$(wc -l isort.out)" != "0 isort.out" ]; then cat isort.out; exit 1; fi
	@echo "=== yapf ==="
	yapf --recursive --diff $(lint_files)
	@echo "=== rst ==="
	restructuredtext-lint $(rst_files)
	@echo "=== setup.py ==="
	python setup.py check --metadata --strict


.PHONY: fixlint
fixlint:
	@echo "=== fixing isort ==="
	isort --quiet --recursive $(lint_files)
	@echo "=== fixing yapf ==="
	yapf --recursive --in-place $(lint_files)

# Tox: -e "py3{6,7,8}-lintexamples"
.PHONY: lintexamples
lintexamples:
	@echo "=== flake8 ==="
	flake8 examples | sort > flake8.out
	diff examples/bad/flake8_expected.out flake8.out
	@echo "=== mypy ==="
	mypy examples examples/good --ignore-missing-imports
	mypy examples/bad --ignore-missing-imports
	@echo "=== black ==="
	black --check --diff --verbose examples/good/black

.PHONY: fixlintexamples
fixlintexamples:
	@echo "=== black ==="
	black examples/good/black

# Tox: -e "py36-doc"
.PHONY: doc
doc:
	$(MAKE) -C docs html

# Tox: -e "py3{6,7,8}-cmd"
.PHONY: cmd
cmd:
	for i in $(good_examples); do \
		echo "\n=== $$i ==="; \
		python -m flake8_aaa "$$i" || break -1; \
	done

# Tox: -e "py3{6,7,8}-cmdbad"
# NOTE: Checks that all bad example files give at least 1 error and all return
# an error code greater than 0. The `echo;` is used to wipe the error code from
# the last test, or the for loop fails.
.PHONY: cmdbad
cmdbad:
	for i in $(bad_examples); do \
		echo "\n=== $$i ==="; \
		python -m flake8_aaa "$$i" && break -1; \
		echo; \
	done


# --- Local dev: Building / Publishing ---

.PHONY: clean
clean:
	rm -rf dist build .tox .pytest_cache src/flake8_aaa.egg-info
	find . -name '*.pyc' -delete

.PHONY: sdist
sdist: tox
	python setup.py sdist

.PHONY: bdist_wheel
bdist_wheel: tox
	python setup.py bdist_wheel

.PHONY: testpypi
testpypi: clean sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: pypi
pypi: sdist bdist_wheel
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

.PHONY: on_master
on_master:
	./on_master.sh

.PHONY: tag
tag: on_master
	git tag -a $$(python -c 'from src.flake8_aaa.__about__ import __version__; print("v{}".format(__version__))')
