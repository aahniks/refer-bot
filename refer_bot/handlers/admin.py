import logging
import os

from telethon import Button, TelegramClient, events

from refer_bot import messages
from refer_bot import storage as st
from refer_bot.handlers._utils import admin_protect, build_keyboard, join_protect
from refer_bot.types import EventLike

configure_btn = "🛠️ Configure"
edit_user_btn = "✏️ Edit User"
stats_btn = "📊 View Statistics"
contact_dev_btn = "🧑‍💻 Contact Developer"

admin_btns = build_keyboard(
    [[configure_btn, edit_user_btn], [stats_btn], [contact_dev_btn]]
)


@events.register(events.NewMessage(pattern="/admin"))
@admin_protect
async def admin_cmd_handler(event: EventLike):

    await event.respond("Click any keyboard button to continue", buttons=admin_btns)


@events.register(events.NewMessage(pattern=configure_btn))
@admin_protect
async def configure_btn_handler(event: EventLike):
    await event.respond("This feature is coming in the next release!")


@events.register(events.NewMessage(pattern=edit_user_btn))
@admin_protect
async def edit_user_btn_handler(event: EventLike):
    client: TelegramClient = event.client
    async with client.conversation(event.sender_id) as conv:
        ask_id = await conv.send_message("Enter the ID of the user",buttons=Button.clear())
        id_reply = await conv.get_response(ask_id)
        try:
            int_id = int(id_reply.text)
            user = await st.engine.find_one(st.Person, st.Person.uid == int_id)
            if not user:
                await conv.send_message("No user found with that ID")
        except ValueError:
            await conv.send_message("Invalid ID")
        except Exception as err:
            await conv.send_message(
                f"Unknown Error occured. Please report to @aahnikdaw\n {str(err)}"
            )
        print(user.banned)
        if user.banned:
            ban_unban = messages.unban_user_btn
        else:
            ban_unban = messages.ban_user_btn

        matrix = [
            [messages.cut_coins_btn, messages.reset_wallet_btn],
            [ban_unban],
        ]

        ask_choice = await conv.send_message(
            messages.user_profile.format(heading="User Profile", user=user),
            buttons=build_keyboard(matrix),
        )

        user_choice_reply = await conv.get_response(ask_choice)
        ch = user_choice_reply.text
        try:
            if ch == messages.cut_coins_btn:
                ask_no_of_coins = await conv.send_message(
                    "Enter the number of coins to cut", buttons=Button.clear()
                )
                no_of_coins_reply = await conv.get_response(ask_no_of_coins)
                dc = int(no_of_coins_reply.text)
                user.coins -= dc

            elif ch == messages.reset_wallet_btn:
                user.wallet = ""
                user.phone = None
            elif ch == ban_unban:
                user.banned = not (user.banned)
            else:
                raise ValueError("Invalid Choice")

        except Exception as err:
            await conv.send_message(f"Error occured {err}", buttons=admin_btns)
            raise events.StopPropagation
        else:
            await st.engine.save(user)
            await conv.send_message(
                messages.user_profile.format(heading="User Updated!", user=user),
                buttons=admin_btns,
            )


@events.register(events.NewMessage(pattern=stats_btn))
@admin_protect
async def stats_btn_handler(event: EventLike):
    total = await st.engine.count(st.Person)
    await event.respond(f"Total Number of Bot Users {total}")


@events.register(events.NewMessage(pattern=contact_dev_btn))
@admin_protect
async def contact_dev_btn_handler(event: EventLike):
    await event.respond("Talk to @aahnikdaw for any issue.")
