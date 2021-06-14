import logging

from telethon import TelegramClient, events

from refer_bot import conf
from refer_bot import storage as st
from refer_bot.handlers._utils import get_args
from refer_bot.types import EventLike


@events.register(events.NewMessage(pattern="/start"))
async def start_handler(event: EventLike):
    logging.info(f"Recieved /start command from {event.sender_id}")
    args = get_args(event.text)
    if args:
        logging.info(f"this user has been refered by {args}")
        client: TelegramClient = event.client
        referer_id = await client.get_peer_id(args)
        logging.info(f"referer id {referer_id}")
        referer = st.fetch(referer_id)
        referer.referals.append(event.sender_id)
        st.update(referer_id, referer)
    else:
        referer_id = None

    this_user = st.UserData(user_id=event.sender_id, referer=referer_id)
    if this_user.user_id in st.stored:
        logging.info("This user is already stored, and data cant be changed.")
    else:
        st.insert(event.sender_id, this_user)
        st.dump()
    await event.respond(
        f"Hello \
        \nYou must join these channels to continue. \
            \n{[c for c in conf.CHANNELS]}\
        \nOnce done, send me /refresh"
    )
    raise events.StopPropagation
