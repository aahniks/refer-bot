import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv(".env")

API_ID = os.getenv("TG_API_ID")
API_HASH = os.getenv("TG_API_HASH")
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
BOT_ADMINS = os.getenv("TG_BOT_ADMINS")  # comma seperated usernames of admins

COMMANDS = {
    "start": "Check if I am alive",
    "help": "Learn usage of the bot",
    "refresh": "Refresh after joining all the channels",
    "upi": "Set your UPI ID where you want to recieve Rupees",
    "coins": "See the no of coins you have in your wallet",
    "referals": "See who have joined using your link",
}

ADMINS = []  # user id of admins

CHANNELS = ["@aahniks_code", "@aahnikd"]

BOT_USERNAME = ""


def checks():
    if not API_ID:
        logging.warning("Please set your [r]TG_API_ID[/r] env var")
    if not API_HASH:
        logging.warning("Please set your [r]TG_API_HASH[/r] env var")
    if not BOT_TOKEN:
        logging.warning("Please set your [r]TG_BOT_TOKEN[/r] env var")

    try:
        assert API_HASH and API_ID and BOT_TOKEN
    except AssertionError:
        logging.critical(
            "Make sure to set your environment variables!\nIf you running this on your own computer or a VPS, you can write them in a [dim].env[/dim] file in the following format\
            \n\t[dim]<ENV_VAR_NAME>=<ENV_VAR_VALUE>[/dim]\
            \nIf you are deploying to a cloud platform like Heroku or Digital Ocean App Platform,\
            \nyou can set the values of the env vars from the UI of the platform"
        )
        sys.exit(1)

    logging.info("All required environment variables loaded successfully")


checks()
