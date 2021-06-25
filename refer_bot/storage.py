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
    verified: StrictBool = False

    @property
    def ref_count(self):
        return len(self.referals)

    @property
    def wallet_str(self):
        return (self.wallet + "(" + str(self.phone) + ")") if self.wallet else "Not set"


class AdminConfig(Model):
    force_channels: List[str]
    min_limit: int
    coin_val: int
    brodcast_channel: str
    withdrawals_channel: str
