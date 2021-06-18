import logging

from telethon import TelegramClient, events

from refer_bot import messages
from refer_bot import storage as st
from refer_bot.handlers._utils import build_keyboard, get_args
from refer_bot.handlers.const import main_kbd
from refer_bot.types import EventLike


@events.register(events.NewMessage(pattern="/start"))
async def start_handler(event: EventLike):
    logging.info(f"Recieved /start command from {event.sender_id}")
    args = get_args(event.text)
    if args:
        logging.info(f"this user has been refered by {args}")
        client: TelegramClient = event.client
        referer_id = await client.get_peer_id(int(args))
        if referer_id == event.sender_id:
            logging.info("User used own link")
            await event.respond(messages.started_with_own_link)
            raise events.StopPropagation
        logging.info(f"referer id {referer_id}")
        referer = await st.engine.find_one(st.Person, st.Person.uid == referer_id)
        referer.referals.append(event.sender_id)
        await st.engine.save(referer)
    else:
        referer_id = None

    this_user = st.Person(uid=event.sender_id, referer=referer_id)
    fetched_user = await st.engine.find_one(st.Person, st.Person.uid == event.sender_id)
    if fetched_user:
        await event.respond(messages.existing_user_start)
        logging.info("This user is already stored, and data cant be changed.")
    else:
        await event.respond(messages.new_user_start)
        await st.engine.save(this_user)

    await event.respond(
        "Click on any keyboard button to proceed!",
        buttons=main_kbd,
    )
    raise events.StopPropagation
