# refer-bot

Notice:: 

I developed this project as per requirements of a client. It was initially a closed souce project, and now I made it open source with permission from my client for whom I developed this.

This bot counts how many people joined(started using the bot) using a persons referal link. My client used this for marketing and advertisement of online services. The administrator of the bot(the deployer) has access to the usernames of all users and their referal count.

Some features of this bot:
- ask for user phone no and verify if person is from India (The marketer was targetting only Indian users)
- user can see how many people joined using their link and how many coins they have in wallet. coin count gets substracted after payout.
- the admin can see various stats like no of users, or info about a user (phone no submitted by them, referal count, coins etc). admin can substract coin count after paying a user.

This bot was in production in past, and had reached a peak of more than 5k users. A free mongo db atlas account was enough for that. I used to run this bot on a Digital Ocean Ubuntu Droplet.

This project can serve as a guide for junior developers and help them build such a telegram bot that has multiple components:
- business logic
- connection with database
- bot ui aka bot commands, buttons and conversations in telegram bot

I am archiving this project because I no longer intend to work on it. If you are looking to have such a bot or similar solution customly implemented for you, you may contact me to find if I am interested. daw at aahnik dot dev.


## Environment Variables

"TG_API_ID"

"TG_API_HASH"

"TG_BOT_TOKEN"

"TG_BOT_ADMINS"  # comma seperated usernames of admins

"TG_BOT_CONTACT_ADMIN"

"MONGO_DB_CON_STR", "mongodb://localhost:27017/"

"MONGO_DB_DATABASE", "test"

"WITHDRAWALS_CHANNEL"

"BRODCASTER_CHANNEL"
