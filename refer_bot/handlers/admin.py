import logging
import os

from telethon import events

from refer_bot.handlers._utils import admin_protect, build_keyboard, join_protect
from refer_bot.types import EventLike

set_channels = "🎨 Set Channels"
manage_btn = "⚙️ Manage Users"
stats_btn = "📈 View Statistics"
contact_dev_btn = "🧑‍💻 Contact Developer"


@events.register(events.NewMessage(pattern="/admin"))
@admin_protect
async def admin_cmd_handler(event: EventLike):
    buttons = build_keyboard(
        [[set_channels, manage_btn], [stats_btn], [contact_dev_btn]]
    )

    await event.respond("Click any keyboard button to continue", buttons=buttons)


@events.register(events.NewMessage(pattern=manage_btn))
@admin_protect
async def manage_btn_handler(event: EventLike):
    pass


@events.register(events.NewMessage(pattern=stats_btn))
@admin_protect
async def stats_btn_handler(event: EventLike):
    await event.respond()


@events.register(events.NewMessage(pattern=contact_dev_btn))
@admin_protect
async def contact_dev_btn_handler(event: EventLike):
    await event.respond("Talk to @aahnikdaw for any issue.")
