lint_files=setup.py flake8_aaa tests
rst_files=README.rst CHANGELOG.rst docs/discovery.rst docs/rules.rst

venv:
	virtualenv venv --python=python3
	venv/bin/pip install -U pip

venv2:
	virtualenv venv2 --python=python2
	venv/bin/pip install -U pip

venv/bin/pip-sync: venv
	venv/bin/pip install pip-tools

.PHONY: dev
dev: venv venv/bin/pip-sync
	venv/bin/pip-sync requirements/dev.txt

.PHONY: tox
tox:
	tox


.PHONY: lint
lint:
	@echo "=== flake8 ==="
	flake8 $(lint_files) examples
	@echo "=== mypy ==="
	mypy flake8_aaa --ignore-missing-imports
	@echo "=== pylint ==="
	./run_pylint.sh flake8_aaa
	@echo "=== isort ==="
	isort --quiet --recursive --diff $(lint_files) > isort.out
	if [ "$$(wc -l isort.out)" != "0 isort.out" ]; then cat isort.out; exit 1; fi
	@echo "=== yapf ==="
	yapf --recursive --diff $(lint_files)
	@echo "=== rst ==="
	restructuredtext-lint $(rst_files)
	@echo "=== setup.py ==="
	python setup.py check --metadata --strict

.PHONY: test
test:
	pytest tests


.PHONY: fixlint
fixlint:
	@echo "=== fixing isort ==="
	isort --quiet --recursive $(lint_files)
	@echo "=== fixing yapf ==="
	yapf --recursive --in-place $(lint_files)


.PHONY: doc
doc:
	$(MAKE) -C docs html


# --- Building / Publishing ---

.PHONY: clean
clean:
	rm -rf dist build .tox .pytest_cache flake8_aaa.egg-info
	find . -name '*.pyc' -delete

.PHONY: sdist
sdist: clean tox
	python setup.py sdist

.PHONY: bdist_wheel
bdist_wheel: clean tox
	python setup.py bdist_wheel

.PHONY: testpypi
testpypi: clean sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: pypi
pypi: clean sdist bdist_wheel
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

.PHONY: on_master
on_master:
	./on_master.sh

.PHONY: tag
tag: on_master
	git tag -a $$(python -c 'from flake8_aaa.__about__ import __version__; print("v{}".format(__version__))')
