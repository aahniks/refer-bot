from typing import Union

from telethon import events
from telethon.tl.custom.message import Message

EventLike = Union[Message, events.NewMessage]
