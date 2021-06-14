import logging

from telethon import events

from refer_bot.handlers._utils import join_protect
from refer_bot.types import EventLike


@events.register(events.NewMessage(pattern="/help"))
@join_protect
async def help_handler(event: EventLike):
    await event.respond("This is help!")
    raise events.StopPropagation


@events.register(events.NewMessage(pattern="/upi"))
@join_protect
async def upi_handler(event: EventLike):
    await event.respond("This is upi!")
    raise events.StopPropagation


@events.register(events.NewMessage(pattern="/coins"))
@join_protect
async def coins_handler(event: EventLike):
    await event.respond("This is coins!")
    raise events.StopPropagation
