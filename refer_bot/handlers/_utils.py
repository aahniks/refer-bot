import functools
import logging

from telethon import TelegramClient, events, functions
from telethon.errors import UserNotParticipantError

from refer_bot import conf
from refer_bot.types import EventLike
from refer_bot import storage as st


def admin_protect(org_func):
    """Decorate to restrict non admins from accessing the bot."""

    @functools.wraps(org_func)
    async def wrapper_func(event):
        """Wrap the original function."""
        logging.info(f"Applying admin protection! Admins are {conf.ADMINS}")
        if event.sender_id not in conf.ADMINS:
            await event.respond("You are not authorized.")
            raise events.StopPropagation
        return await org_func(event)

    return wrapper_func


def get_args(text: str) -> str:
    """Return the part of message following the command."""
    splitted = text.split(" ", 1)

    if not len(splitted) == 2:
        splitted = text.split("\n", 1)
        if not len(splitted) == 2:
            return ""

    prefix, args = splitted
    args = args.strip()
    logging.info(f"Got command {prefix} with args {args}")
    return args


async def check_joined(client: TelegramClient, user: int):
    for channel in conf.CHANNELS:
        try:
            await client(functions.channels.GetParticipantRequest(channel, user))
        except UserNotParticipantError:
            return False
    return True


def join_protect(org_func):
    @functools.wraps(org_func)
    async def wrapper_func(event: EventLike):
        """Wrap the original function."""
        logging.info(f"Recieved {event.text} from {event.sender_id}")
        logging.info(f"Applying join protection!")
        this_user = st.fetch(event.sender_id)
        if not await check_joined(event.client, event.sender_id):
            await event.respond(
                f"You need to first join the channels \
                \n {[c for c in conf.CHANNELS]} before you can do anything else."
            )
            this_user.joined = False
            st.update(event.sender_id, this_user)
            raise events.StopPropagation
        this_user.joined = True
        st.update(event.sender_id, this_user)
        return await org_func(event)

    return wrapper_func
