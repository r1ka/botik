import asyncio
import aiohttp
import logging
import os
from aiohttp.client_exceptions import ClientError
from telegrambot import Client, Bot, Handlers, Message, MessageType
from telegrambot.rules import Contains

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
    await message.bot.send_message("Бог тебе поможет")


@handlers(MessageType.NEW_CHAT_MEMBERS)
async def new_member(message: Message):
    await message.bot.send_message("Смотрите кто к нам колёса катит)")


@handlers(MessageType.TEXT, Contains("привет"))
async def text(message: Message):
    await message.bot.send_message("Здарова!")


@handlers(MessageType.TEXT, Contains("хуй"))
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
