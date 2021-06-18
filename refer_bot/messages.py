import logging

stats_text = """
Your profile stats

**ℹ️ ID**: `{uid}`

**✅ Joined All**: {joined}

**🎉 Coins**: {coins}

**💰 Wallet**: {wallet}

**🔀 Referals**: {ref_count}
"""

started_with_own_link = """
⚠️ You cant use your own link! Please share this with your friends.
"""

new_user_start = """
😃 Hello Welcome to refer and earn 🙏
"""

existing_user_start = """
I am alive 🔥
"""

referal_link_msg = """
Share this link 🔗 with your friends

`{referal_link}`

When your friend clicks on the link you shared and joins all the channels, you will earn one coin."
"""

user_not_found = """
❌ Internal Error! User not found.

Please report this incident to admins.

Please click /start
"""

help_text = """
Please contact @aahnikdaw to get this bot for your self!
"""

user_not_authorized = """
⚠️ You are not authorized
"""

join_channels_text = """
👋 You need to join the following channels to continue

{channels}
"""

get_cash_text = """
Contact admin to withdraw your coins!
Your ID is {uid}

Forward this message to {admin}
"""

not_sufficient_coins = """
You do not have sufficient coins in your wallet.
You need to have minimum {min_limit} coins to withdraw cash.
"""

wallet_set_failed = """
❗Failed to set wallet!

Reason: {reason}

Please try again.
"""

refresh_btn = "↺ Refresh"
profile_btn = "🎨 Profile"
my_referals_btn = "💡 My Referals"
get_link_btn = "🔗 Get Referal Link"
get_cash_btn = "💵 Get cash"

user_kbd_matrix = [[profile_btn], [my_referals_btn, get_link_btn], [get_cash_btn]]

wallet_options = ["paytm", "phonepe"]

try:
    from m2 import *

    logging.info(
        "m2 loaded! If any variabe exists with same name, it will override default message "
    )
    logging.critical(
        "m2 must not contain anything else, other than message vars \
        \nBad m2 can corrupt the bot, or lead to bugs \
        \nm2 is not checked, it is directly imported. So you must be careful to use a valid m2.py file"
    )

except ModuleNotFoundError:
    logging.info("Using default messages")
