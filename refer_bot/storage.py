from typing import List, Optional

from odmantic import AIOEngine, Field, Model
from pydantic import StrictBool, validator

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
    one_id: int = Field(primary_field=True)
    force_channels: List[str] = []
    min_lim: int = 0
    coin_val: int = 0

    @validator("force_channels")
    def validate_delay(cls, val: List[str]):
        for item in val:
            if not item.startswith("https://t.me/"):
                raise ValueError(f"`{item}` is an invalid link!")
        return val

    @property
    def force_channels_repr(self):
        if len(self.force_channels) == 0:
            return "No channels set!"
        string = "```"
        for item in self.force_channels:
            string += str(item) + "\n"
        string += "```"
        return string


admin_cfg: AdminConfig = None
