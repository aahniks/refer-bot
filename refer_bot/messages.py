import logging

user_profile = """
{heading}

**ℹ️ ID**: `{user.uid}`

**✅ Joined All**: {user.joined}

**🎉 Coins**: {user.coins}

**💰 Wallet**: {user.wallet_str}

**🔀 Referals**: {user.ref_count}
"""

admin_config = """
List of **Force Channel** Links :

{cfg.force_channels_repr}

**Minimum Limit** for withdrawals: `{cfg.min_lim}`

**Value** of one **coin**: `{cfg.coin_val}`
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

When your friend clicks on the link you shared and joins all the channels, you will earn one coin.
"""

user_not_found = """
❌ Internal Error! User not found.

Please report this incident to admins.

Please click /start
"""

help_text = """
🙏 Please contact {admin} for support!
"""

user_not_authorized = """
⚠️ You are not authorized
"""

join_channels_text = """
👋 You need to join the following channels to continue

{channels}
"""

my_referals_text = """
No of referals **{user.ref_count}**
That means {user.ref_count} people clicked on you link and started the bot.

**Note**: You will only earn coin after your friend **joins all channels** after starting the bot.
"""

my_coins_text = """
You have **{user.coins}** coins in your balance.
"""

get_cash_text = """
Contact admin to withdraw your coins!
Your ID is {uid}

Forward this message to {admin}
"""

not_sufficient_coins = """
You do not have sufficient coins in your account.
You need to have minimum {min_limit} coins to withdraw cash.
"""

wallet_set_failed = """
❗Failed to set wallet!

Reason: {reason}

Please try again.
"""

ban_due_to_reusing_phn = """
The phone number you used is already set as wallet by another person.

❗ You are banned, as this is against our policy.
"""

user_banned_msg = """
❌ You are banned for violating our policy.

Contact {admin} for help.
"""

veri_failed = """
⚠️ Verification failed as you **did not send your own number**. Please press /start to try again!
"""

switch_private = """
⚠️ You must use this bot {username} in a direct/private chat.

Using this bot within groups or channels is not allowed!
"""

refresh_btn = "↺ Refresh"
profile_btn = "🎨 Profile"
my_referals_btn = "💡 My Referals"
my_coins_btn = "🤑 My Coins"
get_link_btn = "🔗 Get Referal Link"
get_cash_btn = "💵 Get cash"

user_kbd_matrix = [
    [profile_btn, my_coins_btn],
    [my_referals_btn, get_link_btn],
    [get_cash_btn],
]

wallet_options = ["paytm", "phonepe"]

configure_btn = "🛠️ Configure"
edit_user_btn = "✏️ Edit User"
stats_btn = "📊 View Statistics"
contact_dev_btn = "🧑‍💻 Contact Developer"

admin_kbd_matrix = [[configure_btn, edit_user_btn], [stats_btn], [contact_dev_btn]]

cut_coins_btn = "✂️ Cut Coins"
reset_wallet_btn = "⚙️ Reset Wallet"
ban_user_btn = "🚫 Ban User"
unban_user_btn = "👍 Unban User"

edit_channels_btn = "Force Channels"
edit_min_lim_btn = "Minimum Limit"
edit_coin_val = "Coin Value"

admin_config_kbd_matrix = [
    [edit_channels_btn],
    [edit_min_lim_btn, edit_coin_val],
]


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
