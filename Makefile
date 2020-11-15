lint_files=setup.py src/flake8_aaa tests
rst_files=README.rst CHANGELOG.rst

# Lists of examples to pass through command line checks
# NOQA examples in /examples/good will fail because CMD does not respect noqa
# comments in the same way that flake8 does.
good_examples = $(wildcard examples/good/*.py examples/good/black/*.py) examples/good/noqa/test_cmd.py
bad_examples = $(wildcard examples/good/noqa/test_0*.py examples/good/black/noqa/test_0*.py examples/bad/*.py)


# Local dev: Install requirements
.PHONY: dev
dev:
	pip-sync requirements/base.txt requirements/test.txt requirements/dev.txt

# Local dev: Run all tests for available Python versions
.PHONY: test
test:
	tox --skip-missing-interpreters true

# --- Tox recipes ---

.PHONY: lint
lint:
	@echo "=== flake8 ==="
	flake8 $(lint_files)
	@echo "=== mypy ==="
	MYPYPATH=stubs mypy src/flake8_aaa tests
	@echo "=== isort ==="
	isort --check --diff $(lint_files)
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

.PHONY: lintexamples
lintexamples:
	@echo "=== flake8 ==="
	flake8 examples/good examples/bad | sort > flake8.out
	diff examples/bad/flake8_expected.out flake8.out
	@echo "=== mypy ==="
	mypy examples examples/good --ignore-missing-imports
	mypy examples/bad --ignore-missing-imports
	@echo "=== black ==="
	black --check --diff --verbose examples/good/black

.PHONY: lintexamplespy38
lintexamplespy38:
	@echo "=== flake8 ==="
	flake8 examples/good_py38
	@echo "=== mypy ==="
	mypy examples/good_py38

.PHONY: fixlintexamples
fixlintexamples:
	@echo "=== black ==="
	black examples/good/black

.PHONY: doc
doc:
	$(MAKE) -C docs html

.PHONY: cmd
cmd:
	for i in $(good_examples); do \
		echo "\n=== $$i ==="; \
		python -m flake8_aaa "$$i" || break -1; \
	done

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

.PHONY: black_examples
black_examples:
	$(MAKE) -C examples clean all
