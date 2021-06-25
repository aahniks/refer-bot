from telethon import Button, TelegramClient, events

from refer_bot import __version__, messages
from refer_bot import storage as st
from refer_bot.handlers._utils import admin_protect, build_keyboard, get_args
from refer_bot.types import EventLike

admin_btns = build_keyboard(messages.admin_kbd_matrix)


@events.register(events.NewMessage(pattern="/admin"))
@admin_protect
async def admin_cmd_handler(event: EventLike):

    await event.respond(
        f"Running **refer-bot** version {__version__}.\nClick any keyboard button to continue",
        buttons=admin_btns,
    )


@events.register(events.NewMessage(pattern=messages.configure_btn))
@admin_protect
async def configure_btn_handler(event: EventLike):
    button_data = {}
    await event.respond("Choose the option to configure")


@events.register(events.NewMessage(pattern=messages.edit_user_btn))
@admin_protect
async def edit_user_btn_handler(event: EventLike):
    client: TelegramClient = event.client
    async with client.conversation(event.sender_id) as conv:
        ask_id = await conv.send_message(
            "Enter the ID of the user", buttons=Button.clear()
        )
        id_reply = await conv.get_response(ask_id)
        try:
            int_id = int(id_reply.raw_text)
            user = await st.engine.find_one(st.Person, st.Person.uid == int_id)
            if not user:
                await conv.send_message("No user found with that ID")
                raise ValueError
        except ValueError:
            await conv.send_message("Invalid ID", buttons=admin_btns)
            conv.cancel()
            raise events.StopPropagation
        except Exception as err:
            await conv.send_message(
                f"Unknown Error occured. Please report to @aahnikdaw\n {str(err)}",
                buttons=admin_btns,
            )
            conv.cancel()
            raise events.StopPropagation
        if user.banned:
            ban_unban = messages.unban_user_btn
        else:
            ban_unban = messages.ban_user_btn

        edit_user_kbd_matrix = [
            [messages.cut_coins_btn, messages.reset_wallet_btn],
            [ban_unban],
        ]

        ask_choice = await conv.send_message(
            messages.user_profile.format(heading="User Profile", user=user),
            buttons=build_keyboard(edit_user_kbd_matrix),
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
            conv.cancel()
            raise events.StopPropagation
        else:
            await st.engine.save(user)
            await conv.send_message(
                messages.user_profile.format(heading="User Updated!", user=user),
                buttons=admin_btns,
            )


@events.register(events.NewMessage(pattern=messages.stats_btn))
@admin_protect
async def stats_btn_handler(event: EventLike):
    total = await st.engine.count(st.Person)
    await event.respond(f"Total Number of Bot Users {total}")


@events.register(events.NewMessage(pattern=messages.contact_dev_btn))
@admin_protect
async def contact_dev_btn_handler(event: EventLike):
    await event.respond("Talk to @aahnikdaw for any issue.")
