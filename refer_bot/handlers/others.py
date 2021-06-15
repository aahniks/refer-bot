import logging

from telethon import events

from refer_bot import storage as st
from refer_bot.handlers._utils import join_protect
from refer_bot.types import EventLike


@events.register(events.NewMessage(pattern="/help"))
@join_protect
async def help_handler(event: EventLike):
    await event.respond("This is help! For support contact @help621")
    raise events.StopPropagation


@events.register(events.NewMessage(pattern="/stats"))
@join_protect
async def stats_handler(event: EventLike):
    this_user = st.fetch(event.sender_id)

    await event.respond(
        f"Your profile stats\
        \nID: {this_user.user_id}\
        \nJoined All channels: {this_user.joined}\
        \nCoins in your wallet: {this_user.coins}\
        \nNo. of sucessful referals you made: {len(this_user.referals)}"
    )
    raise events.StopPropagation
