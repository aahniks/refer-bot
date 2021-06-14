import json
import sys
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

stored: Dict[int, Dict[str, Any]] = {}
# key is user id and value is data dict


class UserData(BaseModel):
    user_id: int  # user id
    joined: bool = False  # whether the user has joined all channels
    coins: int = 0  # no of coins this user currently has
    referer: Optional[int] = None
    referals: List[int] = []  # list of users this user has referred


def check_integrity(_id: int, data: UserData):
    assert _id == data.user_id
    if not isinstance(data, UserData):
        raise ValueError("Data is not of type UserData")


def insert(_id: int, data: UserData):
    check_integrity(_id, data)
    assert _id not in stored.keys()
    stored[_id] = data.dict()


def update(_id: int, data: UserData):
    check_integrity(_id, data)
    assert _id in stored.keys()
    stored[_id] = data.dict()
    # add a new record or update a record in the data


def fetch(_id: int) -> Union[UserData, None]:
    data_dict = stored.get(_id)
    if data_dict:
        return UserData(**data_dict)
    return None

    # fetch the data of a particular user


def dump():
    with open("data/data.json", "w") as file:
        json.dump(stored, file)


def get_mbs(obj):
    # return amount of MBs a python object consumes
    return sys.getsizeof(obj) * 0.000001
