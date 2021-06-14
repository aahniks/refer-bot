import logging

from telethon import events

from telethon_bot.types import EventLike


@events.register(events.NewMessage(pattern="/start"))
async def start_handler(event: EventLike):
    sender = await event.get_sender()
    logging.info(f"Recieved /start command from @{sender.username}")
    await event.respond(f"Hello @{sender.username}")
    raise events.StopPropagation


@events.register(events.NewMessage(pattern="/help"))
async def help_handler(event: EventLike):
    sender = await event.get_sender()
    logging.info(f"Recieved /help command from @{sender.username}")
    await event.respond("This is help!")
    raise events.StopPropagation
