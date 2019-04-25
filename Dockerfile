FROM python:3.7.3

WORKDIR /app

RUN git clone https://github.com/v-v-vishnevskiy/aio-telegram-bot.git
WORKDIR aio-telegram-bot
RUN git checkout bd30ba20cfbd2a5297d383b5c4099060d86db879
RUN pip install ./
WORKDIR /app

ADD *.py /app

CMD ["python", "bot.py"]
