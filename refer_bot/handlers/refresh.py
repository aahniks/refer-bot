import logging

from telethon import TelegramClient, events

from refer_bot import conf
from refer_bot import storage as st
from refer_bot.handlers._utils import join_protect
from refer_bot.types import EventLike


@events.register(events.NewMessage(pattern="/refresh"))
@join_protect
async def refresh_handler(event: EventLike):
    logging.info(f"Recieved /refresh command from {event.sender_id}")
    referal_link = f"https://t.me/{conf.BOT_USERNAME}?start={event.sender_id}"
    await event.respond(
        f"Good! You have joined all channels. Share this link with your friends {referal_link}\
        \n You will not get any coins if you change your username.\
        \n When your friend clicks on this link and joins all the channels, you will earn one coin."
    )
    raise events.StopPropagation
