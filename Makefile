venv:
	virtualenv venv --python=python3
	venv/bin/pip install -U pip

venv/bin/pip-sync: venv
	venv/bin/pip install pip-tools

.PHONY: install
install: venv venv/bin/pip-sync
	venv/bin/pip-sync requirements.txt

requirements.txt: requirements.in
	venv/bin/pip-compile requirements.in
