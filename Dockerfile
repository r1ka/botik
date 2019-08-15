FROM python:3.7.3

WORKDIR /app

RUN pip install git+https://github.com/v-v-vishnevskiy/aio-telegram-bot.git@bd30ba20cfbd2a5297d383b5c4099060d86db879
WORKDIR /app

ADD *.py /app

CMD ["python", "bot.py"]
