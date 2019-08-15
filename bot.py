import asyncio
import aiohttp
import logging
import random
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


@handlers.add(message_type=MessageType.COMMAND, rule="/help")
async def command(message: Message):
    await message.bot.send_message("Вот такие команды есть у бота:\n/rules - правила\n/links - полезные ссылки\n/help - список команд")

@handlers.add(message_type=MessageType.COMMAND, rule="/links")
async def command(message: Message):
    await message.bot.send_message("Полезные ссылки:\nhttps://ru.aliexpress.com/item/32792513237.html?spm=a2g0v.search0604.3.2.6f297762FPjzfv - STLink программатор\nhttps://ru.nkon.nl/ - Магазин с качественными аккумуляторами 18650\nhttps://www.lithiumbatterypcb.com/product/13s-48v-li-ion-battery-pcb-board-54-6v-lithium-bms-with-60a-discharge-current-for-electric-motorcycle-and-e-scooter-protection-2-2-3-2-2-2-2-2/ - Совместимая мощная BMS")

@handlers.add(message_type=MessageType.COMMAND, rule="/rules")
async def command(message: Message):
    await message.bot.send_message("1) Запрещается публикация порноматериалов и любой информации, распространение которой запрещено законами РФ, рекламы не связанной с электротранспортом, обсуждение политики.\n\n2) Мат - это прекрасно. Но постарайтесь, пожалуйста, использовать его безадресно чтобы кого-то случайно не оскорбить.")

@handlers.add(message_type=MessageType.NEW_CHAT_MEMBERS)
async def new_member(message: Message):
    user = message.raw["message"]["new_chat_members"][0]
    username = user.get("username")
    name = " ".join([user[key] for key in ("first_name", "last_name") if key in user])
    if username:
        name = f"{name} (@{username})"
    await message.bot.send_message(f"Привет, {name}! Шаурмы и донатов тебе! Если у тебя есть вопрос по самокату, то сначала воспользуйся поиском по чату, большинство вопросов уже обсуждалось. Если поиск не помог, то постарайся задать свой вопрос грамотно и указать максимальное количество подробностей (напр. какая версия прошивки сейчас стоит, что уже пробовал делать и т.п.)\n\nДоступные команды бота:\n/rules - правила\n/links - полезные ссылки\n/help - список команд")

@handlers.add(
    message_type=MessageType.TEXT,
    rule=Contains("конструктор"),
    #pause=10*60  # 10 minutes
)
async def text(message: Message):
    await message.bot.send_text("Конструктор для m365 http://сяокат.рф/ru/konstruktor-proshivok конструктор для PRO http://сяокат.рф/ru/konstruktor-proshivok-pro")


@handlers.add(
    message_type=MessageType.TEXT,
    rule=Contains("шаурм"),
    #pause=60*60  # 1 hour
)
async def text(message: Message):
    await message.bot.send_text("Лучшая шаурма в сокольниках!")


@handlers.add(message_type=MessageType.TEXT, rule=Contains("донат"))
async def text(message: Message):
    await message.bot.send_text("Главный по донатам – @Afader")


@handlers.add(
    message_type=MessageType.TEXT,
    rule=Contains("сокольники"),
    #pause=30*60  # 30 minutes
)
async def text(message: Message):
    await message.bot.send_text("32 павильон фарева")


@handlers.add(
    message_type=MessageType.TEXT,
    rule=RegExp(".*(?i)(хуй|хуев|хуёв|хуен|охуе|пизда|пиздя|пиздо|пизде|ебат|ебан|ебал|гандон|джигурд|дроч|пидор|пидр|бля).*"),
    #pause=15*60  # 15 minutes
)
async def text(message: Message):
    await message.bot.send_text(random.choice([
        "У нас не матерятся!",
        "Можно было бы и культурнее сказать)"
    ]))


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
