"""Event handlers for different keyboard buttons for users"""

import logging

from telethon import Button, events

from refer_bot import conf, messages
from refer_bot import storage as st
from refer_bot.handlers._utils import build_keyboard, join_protect
from refer_bot.types import EventLike


@events.register(events.NewMessage(pattern="/help"))
@join_protect
async def help_handler(event: EventLike, user):
    await event.respond(messages.help_text)
    raise events.StopPropagation


@events.register(events.CallbackQuery(data="refresh"))
@join_protect
async def refresh_button_click_handler(event: events.CallbackQuery.Event, user):
    logging.info("User clicked refresh button")
    await event.answer("Refreshed!")
    if user.joined:
        await event.edit(
            "Thank you for joining the channels!",
            buttons=build_keyboard(messages.user_kbd),
        )


@events.register(events.NewMessage(pattern=messages.profile_btn))
@join_protect
async def profile_handler(event: EventLike, user):
    if not user.wallet:
        wallet_btn = Button.inline("Set your wallet", data=b"wallet")
    else:
        wallet_btn = None

    await event.respond(
        messages.stats_text.format(
            uid=user.uid,
            joined=user.joined,
            coins=user.coins,
            ref_count=len(user.referals),
            wallet=user.wallet or "Not set",
        ),
        buttons=wallet_btn,
    )
    raise events.StopPropagation


@events.register(events.CallbackQuery(data="wallet"))
@join_protect
async def wallet_button_click_handler(event: events.CallbackQuery.Event, user):
    logging.info("User clicked wallet button")

    await event.answer("Click on wallet button recieved")

    if not user.wallet:
        await event.edit("This feature is coming soon!")
        # conversation to get wallet info
    else:
        await event.edit("Your wallet is already set.")


@events.register(events.NewMessage(pattern=messages.my_referals_btn))
@join_protect
async def my_referals_handler(event: EventLike, user: st.Person):
    ref_count = len(user.referals)
    await event.respond(
        f"No of Sucessful referals **{ref_count}**\n\
        \nThat means {ref_count} people started the bot from the link you shared."
    )
    # TODO: paginated list of referals username str


@events.register(events.NewMessage(pattern=messages.get_link_btn))
@join_protect
async def get_link_handler(event: EventLike, user):
    referal_link = f"https://t.me/{conf.BOT_USERNAME}?start={event.sender_id}"
    await event.respond(messages.referal_link_msg.format(referal_link=referal_link))


@events.register(events.NewMessage(pattern=messages.get_cash_btn))
@join_protect
async def get_cash_handler(event: EventLike, user: st.Person):
    min_limit = 100
    if user.coins < 100:
        msg = messages.not_sufficient_coins
    else:
        msg = messages.get_cash_text
    await event.respond(
        msg.format(min_limit=min_limit, admin=conf.CONTACT_ADMIN, uid=user.uid)
    )
