import functools
import logging
from typing import List

from telethon import Button, TelegramClient, events, functions
from telethon.errors import UserNotParticipantError

from refer_bot import conf, messages
from refer_bot import storage as st
from refer_bot.types import EventLike
from refer_bot.utils import get_username_str


def admin_protect(org_func):
    """Decorate to restrict non admins from accessing the bot."""

    @functools.wraps(org_func)
    async def wrapper_func(event):
        """Wrap the original function."""
        logging.info(f"Applying admin protection! Admins are {conf.ADMINS}")
        if event.sender_id not in conf.ADMINS:
            await event.respond(messages.user_not_authorized)
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
        except Exception as err:
            logging.exception(f"Could not check joined for channel {channel}")
            continue
    return True


def join_protect(org_func):
    @functools.wraps(org_func)
    async def wrapper_func(event: EventLike):
        """Wrap the original function."""

        # logging.info(f"Recieved update {event}")

        event_type = type(event)

        if not event.is_private:
            await event.respond(
                messages.switch_private.format(username=f"@{conf.BOT_USERNAME}")
            )
            raise events.StopPropagation

        if event_type == events.NewMessage.Event:
            logging.info(f"New message [dim]{event.text}[/dim] from {event.sender_id}")
        elif event_type == events.CallbackQuery.Event:
            logging.info(
                f"Callback Query [dim]{event.data}[/dim] from {event.sender_id}"
            )
        else:
            logging.info(f"Unknown event{event_type}")

        logging.info(f"Applying join protection!")

        this_user: st.Person = await st.engine.find_one(
            st.Person, st.Person.uid == event.sender_id
        )

        logging.info(this_user)

        if not this_user:
            await event.respond(messages.user_not_found)
            raise events.StopPropagation

        if this_user.banned:
            await event.respond(
                messages.user_banned_msg.format(admin=conf.CONTACT_ADMIN)
            )
            raise events.StopPropagation

        if not this_user.verified:
            await event.respond(
                "⚠️ Your account is not yet verified! \nClick /start to verify."
            )
            raise events.StopPropagation

        referer_id = this_user.referer
        if not await check_joined(event.client, event.sender_id):
            if this_user.joined is True:
                this_user.coins -= 1
                this_user.joined = False
                if referer_id:
                    referer = await st.engine.find_one(
                        st.Person, st.Person.uid == referer_id
                    )
                    referer.coins -= 1
                    await st.engine.save(referer)
                await st.engine.save(this_user)
            await show_channels(event)
            raise events.StopPropagation

        if this_user.joined is False:
            this_user.coins += 1

            if referer_id:
                referer = await st.engine.find_one(
                    st.Person, st.Person.uid == referer_id
                )
                referer.coins += 1
                await st.engine.save(referer)
                person = await get_username_str(event.client, this_user.uid)
                await event.client.send_message(
                    referer.uid,
                    f"You earned a coin as {person} started the bot and joined all channels after clicking your referal link.",
                )
            this_user.joined = True
            await st.engine.save(this_user)

        return await org_func(event, this_user)

    return wrapper_func


async def show_channels(event: EventLike):
    channels = ""
    for c in conf.CHANNELS:
        channels += f"➟ {c}\n"
    await event.respond(
        messages.join_channels_text.format(channels=channels),
        buttons=[
            [Button.inline(messages.refresh_btn, data=b"refresh")],
        ],
        link_preview=False,
    )


def build_keyboard(matrix: List[List[str]], resize=True, single_use=False):
    bm = []
    for row in matrix:
        this_col = []
        for col in row:
            this_col.append(Button.text(col, resize=resize, single_use=single_use))
        bm.append(this_col)

    return bm
