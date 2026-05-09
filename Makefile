ALIAS_NAME = its
SHELL = /bin/bash

install:
	python -m venv venv
	venv/bin/pip install -r requirements.txt
	@echo "alias $(ALIAS_NAME)='make -C $(CURDIR) run'" >> ~/.bashrc
	@echo "alias $(ALIAS_NAME)='make -C $(CURDIR) run'" >> ~/.zshrc 2>/dev/null || true
	@echo "Alias '$(ALIAS_NAME)' added — restart terminal or run: source ~/.bashrc"

install-dev:
	python -m venv venv
	venv/bin/pip install -r requirements-dev.txt

reinstall:
	rm -rf venv
	$(MAKE) install

reinstall-dev:
	rm -rf venv
	$(MAKE) install-dev

run:
	venv/bin/python -m main

restart:
	systemctl --user restart journal-timestamps
