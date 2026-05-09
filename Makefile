install:
	python -m venv venv
	venv/bin/pip install -r requirements.txt

install-dev:
	python -m venv venv
	venv/bin/pip install -r requirements-dev.txt

run:
	make -C . venv/bin/python -m main

restart:
	systemctl --user restart journal-timestamps