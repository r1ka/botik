PYTHON?=python3.7
VENV_PATH?="venv"
TOKEN?=""
PROXY?=""


venv:
	$(PYTHON) -m venv $(VENV_PATH)


framework:
	@git clone https://github.com/v-v-vishnevskiy/aio-telegram-bot.git
	@cd aio-telegram-bot && git checkout bd30ba20cfbd2a5297d383b5c4099060d86db879

.PHONY: install
install: venv framework
	@$(VENV_PATH)/bin/pip install ./aio-telegram-bot

run:
	$(VENV_PATH)/bin/python bot.py

docker:
	docker build -t botik  .

docker-run:
	docker run -d --restart=always -e TOKEN=$(TOKEN) -e PROXY=$(PROXY) botik
