from telethon import Button, TelegramClient, events

from refer_bot import __version__, messages
from refer_bot import storage as st
from refer_bot.handlers._utils import admin_protect, build_keyboard, check_joined
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
    button_data = {
        messages.edit_channels_btn: "force_channels",
        messages.edit_min_lim_btn: "min_lim",
        messages.edit_coin_val: "coin_val",
    }
    admin_config_kbd = build_keyboard(messages.admin_config_kbd_matrix)

    client: TelegramClient = event.client

    admin_cfg = await st.engine.find_one(st.AdminConfig, st.AdminConfig.one_id == 1)
    if not admin_cfg:
        admin_cfg = await st.engine.save(st.AdminConfig(one_id=1))

    async with client.conversation(event.sender_id) as conv:
        ask_optn = await conv.send_message(
            messages.admin_config.format(cfg=st.admin_cfg), buttons=admin_config_kbd
        )
        user_optn = await conv.get_response(ask_optn)
        ch = button_data.get(user_optn.text)
        if not ch:
            await conv.send_message("Invalid Choice", buttons=admin_btns)
            raise events.StopPropagation
        ask_val = await conv.send_message(
            f"Enter the value of {ch}", buttons=Button.clear()
        )
        user_ans = await conv.get_response(ask_val)
        val: str = user_ans.raw_text
        if ch == "force_channels":
            val = val.strip().split("\n")
        try:
            setattr(admin_cfg, ch, val)
            await check_joined(
                client,
                event.sender_id,
                channels=admin_cfg.force_channels,
                raise_err=True,
            )
        except Exception as err:
            await conv.send_message("❌ " + str(err))
        else:
            st.admin_cfg = await st.engine.save(admin_cfg)
            await conv.send_message("✅ Success!")
        finally:
            await conv.send_message(
                messages.admin_config.format(cfg=st.admin_cfg), buttons=admin_btns
            )
            conv.cancel()
            raise events.StopPropagation


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
