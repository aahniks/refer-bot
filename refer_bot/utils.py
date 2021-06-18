from telethon import TelegramClient


async def get_id(client: TelegramClient, peer):
    return await client.get_peer_id(peer)


async def get_username_str(client: TelegramClient, user_id: int):
    entity = await client.get_entity(user_id)
    name_str = (
        f"{entity.first_name or ''} {entity.last_name or ''} {entity.username or ''}"
    )
    return name_str
