FROM python:3.7.3

ENV TOKEN ${TOKEN}
ENV PROXY ${PROXY}

WORKDIR /app

ADD . /app

RUN pip install /app/aio-telegram-bot

CMD ["python", "bot.py"]
