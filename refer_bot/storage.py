from typing import List, Optional

from odmantic import AIOEngine, Field, Model
from pydantic import StrictBool

engine: AIOEngine = None


class Person(Model):
    uid: int = Field(primary_field=True)
    referer: Optional[int] = None
    joined: StrictBool = False
    referals: Optional[List[int]] = []
    coins: int = 0
    wallet: str = ""
    phone: Optional[int] = None
    banned: StrictBool = False
