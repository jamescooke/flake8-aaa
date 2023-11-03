lint_files=setup.py src/flake8_aaa tests
rst_files=README.rst CHANGELOG.rst

# --- Tox recipes ---

.PHONY: lint
lint:
	@echo "=== flake8 ==="
	flake8 $(lint_files)
	@echo "=== mypy ==="
	mypy src/flake8_aaa tests
	@echo "=== isort ==="
	isort --check --diff $(lint_files)
	@echo "=== yapf ==="
	yapf --recursive --diff $(lint_files)
	@echo "=== rst ==="
	restructuredtext-lint $(rst_files)
	# --- Disabling for now, will move to pyproject.toml in #228
	# @echo "=== setup.py ==="
	# python setup.py check --metadata --strict

.PHONY: lintexamples
lintexamples:
	@echo "=== flake8 ==="
	flake8 examples/good examples/bad | sort > flake8.out
	diff examples/bad/flake8_expected.out flake8.out
	@echo "=== mypy ==="
	mypy examples/conftest.py examples/good --ignore-missing-imports --exclude examples/black/ --no-incremental
	mypy examples/bad --ignore-missing-imports
	@echo "=== black ==="
	black --check --diff --verbose examples/black

.PHONY: docs
docs:
	tox run -e py310-docs

# --- Local dev: Building / Publishing ---

# Generate version signature used in README.rst
.PHONY: signature
signature:
	tox exec -e py312-meta_plugin_dogfood -- flake8 --version

.PHONY: clean
clean:
	rm -rf dist build .tox .pytest_cache src/flake8_aaa.egg-info docs/_build/
	find . -name '*.pyc' -delete
	find src/ examples/ tests/ -name __pycache__ -type d -delete

.PHONY: sdist
sdist:
	python setup.py sdist

.PHONY: bdist_wheel
bdist_wheel:
	pip install wheel
	python setup.py bdist_wheel

.PHONY: testpypi
testpypi: clean sdist bdist_wheel
	twine upload --username=__token__ --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: pypi
pypi: sdist bdist_wheel
	twine upload --username=__token__ --repository-url https://upload.pypi.org/legacy/ dist/*

.PHONY: on_master
on_master:
	./on_master.sh

.PHONY: tag
tag: on_master
	git tag -a v$$(grep -E "^__version__ = .*" -- src/flake8_aaa/__about__.py | grep -Eo '[0-9\.]*')

.PHONY: fixlint
fixlint:
	@echo "=== fixing isort ==="
	isort --quiet --recursive $(lint_files)
	@echo "=== fixing yapf ==="
	yapf --recursive --in-place $(lint_files)

.PHONY: fixlintexamples
fixlintexamples:
	@echo "=== Fixing black using tox env ==="
	tox e -e py38-lint_examples -- black examples/black

# Trigger a new copy of Black-formatted examples to be generated
.PHONY: black_examples
black_examples:
	$(MAKE) -C examples clean all
