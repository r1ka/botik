PYTHON?=python3.7
VENV_PATH?="venv"
TOKEN?=""
PROXY?=""


venv:
	$(PYTHON) -m venv $(VENV_PATH)


framework:
	@git clone https://github.com/v-v-vishnevskiy/aio-telegram-bot.git
	@cd aio-telegram-bot && git checkout 29c1ccf8fe97880d86d237b80ea32196b6a2188c

.PHONY: install
install: venv framework
	@$(VENV_PATH)/bin/pip install ./aio-telegram-bot

run:
	$(VENV_PATH)/bin/python bot.py --token=$(TOKEN) --proxy=$(PROXY)
