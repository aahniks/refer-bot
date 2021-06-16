from inspect import getmembers, isfunction, ismodule

from telethon import TelegramClient, events

from refer_bot import handlers


def get_functions(module):
    """Yield all user defined functions in a module."""
    if not ismodule(module):
        raise ValueError("The argument to get_functions is not a module.")
    for _, value in getmembers(module):
        if isfunction(value):
            yield value


def handler_modules():
    """Yield all modules in handlers subpackage which are exposed in handlers/__init__.py."""
    for _, value in getmembers(handlers):
        if ismodule(value):
            yield value


def handler_functions():
    """Yield all valid event handlers defined in modules yield by handler_modules()."""
    for module in handler_modules():
        for function in get_functions(module):
            if events.is_handler(function):
                yield function


async def get_id(client: TelegramClient, peer):
    return await client.get_peer_id(peer)


async def get_username_str(client: TelegramClient, user_id: int):
    entity = await client.get_entity(user_id)
    name_str = (
        f"{entity.first_name or ''} {entity.last_name or ''} {entity.username or ''}"
    )
    return name_str
