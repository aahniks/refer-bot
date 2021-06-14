import asyncio
import logging

from rich import traceback
from rich.logging import RichHandler
from telethon import TelegramClient, functions, types

traceback.install()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            markup=True,
        )
    ],
)


async def start_bot():
    from telethon_bot import conf
    from telethon_bot.utils import handler_functions

    client = TelegramClient("bot", conf.API_ID, conf.API_HASH)
    await client.start(bot_token=conf.BOT_TOKEN)

    for handler in handler_functions():
        logging.info(f"Added event handler {handler.__name__}")
        client.add_event_handler(handler)

    await client(
        functions.bots.SetBotCommandsRequest(
            commands=[
                types.BotCommand(command=key, description=value)
                for key, value in conf.COMMANDS.items()
            ]
        )
    )
    logging.info(f"Set bot commands {conf.COMMANDS}")
    logging.info("Bot is up and running!")
    await client.run_until_disconnected()


def main():
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logging.critical("Aborted!")
