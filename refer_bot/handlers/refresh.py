import logging

from telethon import events

from refer_bot import conf, messages
from refer_bot.handlers._utils import join_protect
from refer_bot.types import EventLike


@events.register(events.NewMessage(pattern="/refresh"))
@join_protect
async def refresh_handler(event: EventLike):
    logging.info(f"Recieved /refresh command from {event.sender_id}")
    referal_link = f"https://t.me/{conf.BOT_USERNAME}?start={event.sender_id}"
    await event.respond(
        messages.refresh_success_message.format(referal_link=referal_link)
    )
    raise events.StopPropagation
