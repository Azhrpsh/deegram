import logging
import os
import sys
import time

import deethon
from dotenv import load_dotenv
from telethon import TelegramClient, functions, types
from telethon.events import NewMessage

formatter = logging.Formatter(
    '%(levelname)s %(asctime)s - %(name)s - %(message)s')

fh = logging.FileHandler(f'{__name__}.log', 'w')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)

telethon_logger = logging.getLogger("telethon")
telethon_logger.setLevel(logging.WARNING)
telethon_logger.addHandler(ch)
telethon_logger.addHandler(fh)

botStartTime = time.time()

load_dotenv()

try:
    API_ID = 6010987
    API_HASH = f0411fdf11c084312fef79c1cee66bd9
    BOT_TOKEN = 1865094377:AAFjQZOiBV1lHSgF4fAb3gX4PTK9RAgu6l8
    DEEZER_TOKEN = 11544763ea1d2586d36a44b7e329e00285d43839f2d3f72d9bffbe6a22b444c1b0902f83ec3efb4fa09ef0911c11b8d7135d1baaabeeec0749d8e5a0b609b46673d97a68e043fbd40fd13da099843bb3f397da37cac8afb61cd5eac7a23be58f
    OWNER_ID = 1150804862
except KeyError:
    logger.error("One or more environment variables are missing! Exiting now…")
    sys.exit(1)

deezer = deethon.Session(DEEZER_TOKEN)
logger.debug(f'Using deethon v{deethon.__version__}')

bot = TelegramClient(__name__, API_ID, API_HASH,
                     base_logger=telethon_logger).start(bot_token=BOT_TOKEN)
logger.info("Bot started")

# Saving user preferences locally
users = {}

bot.loop.run_until_complete(
    bot(functions.bots.SetBotCommandsRequest(
        commands=[
            types.BotCommand(
                command='start',
                description='Get the welcome message'),
            types.BotCommand(
                command='help',
                description='How to use the bot'),
            types.BotCommand(
                command='settings',
                description='Change your preferences'),
            types.BotCommand(
                command='info',
                description='Get some useful information about the bot'),
            types.BotCommand(
                command='stats',
                description='Get some statistics about the bot'),
        ]
    ))
)


@bot.on(NewMessage())
async def init_user(event: NewMessage.Event):
    if event.chat_id not in users.keys():
        users[event.chat_id] = {
            "quality": "FLAC"
        }
