import asyncio
import aiohttp
import logging
import os
from aiohttp.client_exceptions import ClientError
from telegrambot import Client, Bot, Handlers, Message, MessageType
from telegrambot.rules import Contains, RegExp

logger = logging.getLogger(__name__)
handlers = Handlers()


class MyClient(Client):
    def __init__(self, token: str, proxy: str, **kwargs):
        super().__init__(token, **kwargs)
        self._proxy = proxy

    async def request(self, method: str, api: str, **kwargs) -> dict:
        if self._proxy:
            kwargs["proxy"] = self._proxy
            kwargs["verify_ssl"] = False
        try:
            return await super().request(method, api, **kwargs)
        except asyncio.TimeoutError:
            logger.exception("Timeout")
        except ClientError:
            logger.exception("Can't connect to telegram API. Waiting 10 seconds...")
            await asyncio.sleep(10)
        except Exception:
            logger.exception("Error")


@handlers(MessageType.COMMAND, "/help")
async def command(message: Message):
    await message.bot.send_message("Звоните в полицию!")


@handlers(MessageType.NEW_CHAT_MEMBERS)
async def new_member(message: Message):
    await message.bot.send_message("Приветствуем новичка! Шаурмы и донатов ему!)")


@handlers(MessageType.TEXT, Contains("конструктор"))
async def text(message: Message):
    await message.bot.send_message("Конструктор для m365 http://сяокат.рф/ru/konstruktor-proshivok конструктор для PRO http://сяокат.рф/ru/konstruktor-proshivok-pro")

@handlers(MessageType.TEXT, Contains("шаурма"))
async def text(message: Message):
    await message.bot.send_message("Лучшая шаурма в сокольниках!")

@handlers(MessageType.TEXT, Contains("донаты"))
async def text(message: Message):
    await message.bot.send_message("Главный по донатам - @Afader")

@handlers(MessageType.TEXT, Contains("сокольники"))
async def text(message: Message):
    await message.bot.send_message("32 павильон фарева")

@handlers(MessageType.TEXT, RegExp(".*(?i)(хуй|хуев|хуёв|пизда|пизде|ебат|ебан|джигурд).*"))
async def text(message: Message):
    await message.bot.send_message("У нас не матерятся!")


async def run(token: str, proxy: str):
    client = MyClient(token, proxy, timeout=aiohttp.ClientTimeout(total=5))

    bot = Bot(client, handlers)
    await bot.start()

    while True:
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(run(
        os.environ["TOKEN"],
        os.environ.get("PROXY")
    ))
