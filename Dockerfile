FROM python:3.7.3

WORKDIR /app

ADD . /app

RUN git clone https://github.com/v-v-vishnevskiy/aio-telegram-bot.git
WORKDIR aio-telegram-bot
RUN git checkout 29c1ccf8fe97880d86d237b80ea32196b6a2188c
RUN pip install ./
WORKDIR /app

CMD ["python", "bot.py"]
