"""Event handlers for different keyboard buttons for users"""

import logging

from telethon import Button, TelegramClient, events

from refer_bot import conf, messages
from refer_bot import storage as st
from refer_bot.handlers._utils import build_keyboard, join_protect
from refer_bot.handlers.const import main_kbd
from refer_bot.types import EventLike


@events.register(events.NewMessage(pattern="/help"))
@join_protect
async def help_handler(event: EventLike, user):
    await event.respond(messages.help_text.format(admin=conf.CONTACT_ADMIN))
    raise events.StopPropagation


@events.register(events.CallbackQuery(data="refresh"))
@join_protect
async def refresh_button_click_handler(event: events.CallbackQuery.Event, user):
    logging.info("User clicked refresh button")
    await event.answer("Refreshed!")
    if user.joined:
        await event.edit(
            "Thank you for joining the channels!",
            buttons=build_keyboard(messages.user_kbd_matrix),
        )


@events.register(events.NewMessage(pattern=messages.profile_btn))
@join_protect
async def profile_handler(event: EventLike, user):
    if not user.wallet:
        wallet_btn = Button.inline("Set your wallet", data=b"wallet")
    else:
        wallet_btn = None

    await event.respond(
        messages.user_profile.format(
            uid=user.uid,
            joined=user.joined,
            coins=user.coins,
            ref_count=len(user.referals),
            wallet=(user.wallet + "(" + str(user.phone) + ")")
            if user.wallet
            else "Not set",
        ),
        buttons=wallet_btn,
    )
    raise events.StopPropagation


@events.register(events.CallbackQuery(data="wallet"))
@join_protect
async def wallet_button_click_handler(
    event: events.CallbackQuery.Event, user: st.Person
):
    logging.info("User clicked wallet button")

    await event.answer("Click on wallet button recieved")

    if user.wallet:
        await event.edit("Your wallet is already set.")
        raise events.StopPropagation

    await event.edit("You must be INDIAN to get cash!")

    client: TelegramClient = event.client

    async with client.conversation(event.sender_id) as conv:
        message = await conv.send_message(
            "Please Choose your wallet",
            buttons=build_keyboard([messages.wallet_options]),
        )
        wallet_reply = await conv.get_response(message)
        wallet = wallet_reply.text
        if not (wallet in messages.wallet_options):
            await conv.send_message(
                messages.wallet_set_failed.format(reason="Invalid Wallet type"),
                buttons=main_kbd,
            )
            raise events.StopPropagation

        diff_no = "Send a different number"
        only_ind = "Only Indian Numbers allowed"
        ask_phone = await conv.send_message(
            f"Send your {wallet} number",
            buttons=[
                [
                    Button.request_phone(
                        f"Send my Telegram number", resize=True, single_use=True
                    )
                ],
                [Button.text(diff_no)],
            ],
        )
        phn_reply = await conv.get_response(ask_phone)

        if phn_reply.contact:
            phone: str = phn_reply.contact.phone_number
            if not phone.startswith("91"):
                await conv.send_message(
                    messages.wallet_set_failed.format(reason=only_ind),
                    buttons=main_kbd,
                )
            phone = int(phone[2:])
        elif phn_reply.text == diff_no:

            ask_phn_manual = await conv.send_message(
                f"Type and send your {wallet} number.\n\
                \n(Must be 10 Digit Indian Phone number)",
                buttons=Button.clear(),
            )
            reply_phn = await conv.get_response(ask_phn_manual)
            phone: str = reply_phn.text
        else:
            phone = ""

        try:
            if isinstance(phone, int):
                pass
            elif phone.startswith("91") and len(phone) == 12:
                phone = int(phone[2:])
            elif len(phone) == 10:
                phone = int(phone)
            else:
                raise ValueError
        except:
            await conv.send_message(
                messages.wallet_set_failed.format(
                    reason=f"Invalid phone number format. Give 10 digit number. {only_ind}"
                ),
                buttons=main_kbd,
            )
            conv.cancel()
            raise events.StopPropagation

        if not phone:
            raise events.StopPropagation

        existing_person = await st.engine.find_one(st.Person, st.Person.phone == phone)
        if not existing_person:
            user.phone = phone
            user.wallet = wallet
            await st.engine.save(user)
            await conv.send_message(
                f"Your {wallet} number is set as {phone} 🎉",
                buttons=main_kbd,
            )
        else:
            user.banned = True
            await st.engine.save(user)
            await client.send_message(
                existing_person.uid,
                "⚠️ Warning! \nDont use same wallet with another Telegram account.",
            )
            await conv.send_message(messages.ban_due_to_reusing_phn)


@events.register(events.NewMessage(pattern=messages.my_referals_btn))
@join_protect
async def my_referals_handler(event: EventLike, user: st.Person):
    ref_count = len(user.referals)
    await event.respond(
        f"No of Sucessful referals **{ref_count}**\n\
        \nThat means {ref_count} people started the bot from the link you shared."
    )


@events.register(events.NewMessage(pattern=messages.get_link_btn))
@join_protect
async def get_link_handler(event: EventLike, user):
    referal_link = f"https://t.me/{conf.BOT_USERNAME}?start={event.sender_id}"
    await event.respond(messages.referal_link_msg.format(referal_link=referal_link))


@events.register(events.NewMessage(pattern=messages.get_cash_btn))
@join_protect
async def get_cash_handler(event: EventLike, user: st.Person):
    min_limit = 100
    if user.coins < min_limit:
        msg = messages.not_sufficient_coins
    else:
        msg = messages.get_cash_text
    await event.respond(
        msg.format(min_limit=min_limit, admin=conf.CONTACT_ADMIN, uid=user.uid)
    )
