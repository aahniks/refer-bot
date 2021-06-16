from telethon import events

from refer_bot import messages
from refer_bot import storage as st
from refer_bot.handlers._utils import join_protect
from refer_bot.types import EventLike


@events.register(events.NewMessage(pattern="/help"))
@join_protect
async def help_handler(event: EventLike):
    await event.respond(messages.help_text)
    raise events.StopPropagation


@events.register(events.NewMessage(pattern="/stats"))
@join_protect
async def stats_handler(event: EventLike):
    user = await st.engine.find_one(st.Person, st.Person.uid == event.sender_id)
    if not user:
        await event.respond(messages.user_not_found)
    await event.respond(
        messages.stats_text.format(
            uid=user.uid,
            joined=user.joined,
            coins=user.coins,
            ref_count=len(user.referals),
            wallet=user.wallet,
        )
    )
    raise events.StopPropagation
